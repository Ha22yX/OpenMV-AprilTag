# pc_viewer.py
# 读取串口输出的 AprilTag 位姿，并用 matplotlib 3D 显示坐标系
# 依赖：pip install pyserial matplotlib

import serial
import time
import math
import threading
from collections import deque

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

PORT = "COM20"      # 修改为你的串口号
BAUD = 115200

# 可视化参数
AXIS_LEN = 50.0     # 坐标轴长度（与 tx/ty/tz 单位一致，这里是 mm）
AUTO_SCALE = True   # 根据当前数据自动缩放视图
SCALE_MARGIN = 50.0 # 自动缩放时的边距
HISTORY = 1         # 每个 ID 保留的历史帧数量（1=只显示最新）
STALE_SEC = 0.3     # 超过这个时间未更新的 tag 不显示

# 共享数据
lock = threading.Lock()
poses = {}  # id -> deque of pose dict
last_seen = {}  # id -> timestamp
last_line = ""

def parse_line(line):
    # 期望格式：
    # id=0,tx=12.34,ty=-5.67,tz=345.89,rx=0.012,ry=-0.034,rz=0.567,rx_deg=0.69,ry_deg=-1.95,rz_deg=32.50
    if not line or line == "none":
        return None
    try:
        parts = line.split(",")
        d = {}
        for p in parts:
            k, v = p.split("=")
            d[k.strip()] = float(v) if k != "id" else int(v)
        # 兼容没有 id 的输出
        if "id" not in d:
            d["id"] = 0
        # 若只有角度字段，转换为弧度
        if ("rx" not in d) and ("rx_deg" in d):
            d["rx"] = math.radians(d["rx_deg"])
            d["ry"] = math.radians(d["ry_deg"])
            d["rz"] = math.radians(d["rz_deg"])
        return d
    except Exception:
        return None

def rot_matrix(rx, ry, rz):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    Rx = [[1,0,0],[0,cx,-sx],[0,sx,cx]]
    Ry = [[cy,0,sy],[0,1,0],[-sy,0,cy]]
    Rz = [[cz,-sz,0],[sz,cz,0],[0,0,1]]

    # R = Rz @ Ry @ Rx
    def mm(a,b):
        return [
            [a[0][0]*b[0][0]+a[0][1]*b[1][0]+a[0][2]*b[2][0],
             a[0][0]*b[0][1]+a[0][1]*b[1][1]+a[0][2]*b[2][1],
             a[0][0]*b[0][2]+a[0][1]*b[1][2]+a[0][2]*b[2][2]],
            [a[1][0]*b[0][0]+a[1][1]*b[1][0]+a[1][2]*b[2][0],
             a[1][0]*b[0][1]+a[1][1]*b[1][1]+a[1][2]*b[2][1],
             a[1][0]*b[0][2]+a[1][1]*b[1][2]+a[1][2]*b[2][2]],
            [a[2][0]*b[0][0]+a[2][1]*b[1][0]+a[2][2]*b[2][0],
             a[2][0]*b[0][1]+a[2][1]*b[1][1]+a[2][2]*b[2][1],
             a[2][0]*b[0][2]+a[2][1]*b[1][2]+a[2][2]*b[2][2]],
        ]
    return mm(mm(Rz, Ry), Rx)

def apply_R(R, v):
    return (
        R[0][0]*v[0] + R[0][1]*v[1] + R[0][2]*v[2],
        R[1][0]*v[0] + R[1][1]*v[1] + R[1][2]*v[2],
        R[2][0]*v[0] + R[2][1]*v[1] + R[2][2]*v[2],
    )

def reader_thread():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(line)
            with lock:
                global last_line
                last_line = line
        d = parse_line(line)
        if not d:
            continue
        tid = d["id"]
        with lock:
            if tid not in poses:
                poses[tid] = deque(maxlen=HISTORY)
            poses[tid].append(d)
            last_seen[tid] = time.time()

def draw():
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title("AprilTag 3D Pose")

    while True:
        ax.cla()
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.set_zlabel("Z (mm)")
        # 默认范围（若无数据）
        x_min, x_max = -200, 200
        y_min, y_max = -200, 200
        z_min, z_max = 0, 600
        ax.set_title("AprilTag 3D Pose")

        with lock:
            items = list(poses.items())
            seen = dict(last_seen)
            line_copy = last_line

        now = time.time()
        points = []
        for tid, dq in items:
            if not dq:
                continue
            if (tid not in seen) or ((now - seen[tid]) > STALE_SEC):
                continue
            d = dq[-1]
            tx, ty, tz = d["tx"], d["ty"], d["tz"]
            R = rot_matrix(d["rx"], d["ry"], d["rz"])
            points.append((tx, ty, tz))

            # 坐标轴端点
            ex = apply_R(R, (AXIS_LEN, 0, 0))
            ey = apply_R(R, (0, AXIS_LEN, 0))
            ez = apply_R(R, (0, 0, AXIS_LEN))

            # 原点 + 端点
            ox, oy, oz = tx, ty, tz
            ax.plot([ox, ox+ex[0]], [oy, oy+ex[1]], [oz, oz+ex[2]], color="r")
            ax.plot([ox, ox+ey[0]], [oy, oy+ey[1]], [oz, oz+ey[2]], color="g")
            ax.plot([ox, ox+ez[0]], [oy, oy+ez[1]], [oz, oz+ez[2]], color="b")
            ax.text(ox, oy, oz, f"id:{tid}")

        if AUTO_SCALE and points:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            zs = [p[2] for p in points]
            x_min, x_max = min(xs) - SCALE_MARGIN, max(xs) + SCALE_MARGIN
            y_min, y_max = min(ys) - SCALE_MARGIN, max(ys) + SCALE_MARGIN
            z_min, z_max = min(zs) - SCALE_MARGIN, max(zs) + SCALE_MARGIN
            # 保证 Z 轴不为负
            if z_min < 0:
                z_min = 0

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)

        if line_copy:
            ax.text2D(0.02, 0.02, f"UART: {line_copy}", transform=ax.transAxes)
        plt.pause(0.02)

if __name__ == "__main__":
    t = threading.Thread(target=reader_thread, daemon=True)
    t.start()
    draw()