import sensor, image, time
import pyb
from math import degrees

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
# 删除/注释这行：sensor.set_lens_correction(True)
sensor.skip_frames(time=2000)

sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()
tag_families = image.TAG25H9

# 颜色设置：在灰度图下用不同亮度保证轴可见
if sensor.get_pixformat() == sensor.GRAYSCALE:
    RED = 255
    GREEN = 200
    BLUE = 120
    YELLOW = 220
    WHITE = 255
else:
    RED=(255,0,0); GREEN=(0,255,0); BLUE=(0,0,255); YELLOW=(255,255,0); WHITE=(255,255,255)

# 相机内参（像素单位）。默认按 OpenMV H7 常见 2.8mm 镜头 + OV7725 传感器估算。
# 如你更换镜头或已标定，请据实修改 focal_length_mm / sensor_*_mm。
focal_length_mm = 2.8
sensor_w_mm = 3.984
sensor_h_mm = 2.952
f_x = (focal_length_mm / sensor_w_mm) * sensor.width()
f_y = (focal_length_mm / sensor_h_mm) * sensor.height()
c_x = sensor.width() * 0.5
c_y = sensor.height() * 0.5

# 标签边长（毫米），用于尺度恢复与更稳定的投影显示
TAG_SIZE_MM = 100.0

# 串口输出：默认使用 USB 虚拟串口（直接连电脑无需额外串口线）
# 如需使用外部串口模块，再改成 pyb.UART(3, 115200)
uart = pyb.USB_VCP()
uart.write("APRILTAG VCP READY\n")

def _matmul3(a, b):
    return [
        a[0][0]*b[0] + a[0][1]*b[1] + a[0][2]*b[2],
        a[1][0]*b[0] + a[1][1]*b[1] + a[1][2]*b[2],
        a[2][0]*b[0] + a[2][1]*b[1] + a[2][2]*b[2],
    ]

def _rot_matrix(rx, ry, rz):
    # 旋转顺序：Rz * Ry * Rx（常用 yaw-pitch-roll），与 OpenMV 返回角定义一致性足够用于可视化
    import math
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    Rx = [[1,0,0],[0,cx,-sx],[0,sx,cx]]
    Ry = [[cy,0,sy],[0,1,0],[-sy,0,cy]]
    Rz = [[cz,-sz,0],[sz,cz,0],[0,0,1]]
    # R = Rz @ Ry @ Rx
    # 先 Rtmp = Rz*Ry
    Rtmp = [
        [Rz[0][0]*Ry[0][0] + Rz[0][1]*Ry[1][0] + Rz[0][2]*Ry[2][0],
         Rz[0][0]*Ry[0][1] + Rz[0][1]*Ry[1][1] + Rz[0][2]*Ry[2][1],
         Rz[0][0]*Ry[0][2] + Rz[0][1]*Ry[1][2] + Rz[0][2]*Ry[2][2]],
        [Rz[1][0]*Ry[0][0] + Rz[1][1]*Ry[1][0] + Rz[1][2]*Ry[2][0],
         Rz[1][0]*Ry[0][1] + Rz[1][1]*Ry[1][1] + Rz[1][2]*Ry[2][1],
         Rz[1][0]*Ry[0][2] + Rz[1][1]*Ry[1][2] + Rz[1][2]*Ry[2][2]],
        [Rz[2][0]*Ry[0][0] + Rz[2][1]*Ry[1][0] + Rz[2][2]*Ry[2][0],
         Rz[2][0]*Ry[0][1] + Rz[2][1]*Ry[1][1] + Rz[2][2]*Ry[2][1],
         Rz[2][0]*Ry[0][2] + Rz[2][1]*Ry[1][2] + Rz[2][2]*Ry[2][2]],
    ]
    R = [
        [Rtmp[0][0]*Rx[0][0] + Rtmp[0][1]*Rx[1][0] + Rtmp[0][2]*Rx[2][0],
         Rtmp[0][0]*Rx[0][1] + Rtmp[0][1]*Rx[1][1] + Rtmp[0][2]*Rx[2][1],
         Rtmp[0][0]*Rx[0][2] + Rtmp[0][1]*Rx[1][2] + Rtmp[0][2]*Rx[2][2]],
        [Rtmp[1][0]*Rx[0][0] + Rtmp[1][1]*Rx[1][0] + Rtmp[1][2]*Rx[2][0],
         Rtmp[1][0]*Rx[0][1] + Rtmp[1][1]*Rx[1][1] + Rtmp[1][2]*Rx[2][1],
         Rtmp[1][0]*Rx[0][2] + Rtmp[1][1]*Rx[1][2] + Rtmp[1][2]*Rx[2][2]],
        [Rtmp[2][0]*Rx[0][0] + Rtmp[2][1]*Rx[1][0] + Rtmp[2][2]*Rx[2][0],
         Rtmp[2][0]*Rx[0][1] + Rtmp[2][1]*Rx[1][1] + Rtmp[2][2]*Rx[2][1],
         Rtmp[2][0]*Rx[0][2] + Rtmp[2][1]*Rx[1][2] + Rtmp[2][2]*Rx[2][2]],
    ]
    return R

def _project_point(X, Y, Z):
    # 透视投影，将 3D 相机坐标系点投影到像素坐标
    if Z <= 1e-6:
        return None
    u = int((f_x * (X / Z)) + c_x)
    v = int((f_y * (Y / Z)) + c_y)
    return (u, v)

while True:
    clock.tick()
    img = sensor.snapshot()
    # 可选：开启会更正桶形畸变，但会稍降 FPS
    # img.lens_corr(strength=1.8, zoom=1.0)

    # 用 4 个重叠 ROI 覆盖整帧（每块 <64K 像素；224x176=39,424）
    rois = [
        (0,   0, 224, 176),
        (96,  0, 224, 176),
        (0,  64, 224, 176),
        (96, 64, 224, 176),
    ]

    # 收集并去重（同一帧内，同ID且中心距离很近，保留margin更高的那个）
    detections = []
    for (rx, ry, rw, rh) in rois:
        for tag in img.find_apriltags(families=tag_families, roi=(rx, ry, rw, rh), fx=f_x, fy=f_y, cx=c_x, cy=c_y, tag_size=TAG_SIZE_MM):
            # 注意：在 OpenMV 中，当指定 roi 时，返回的坐标已是整帧坐标，无需再手动加 (rx, ry)
            r_x, r_y, r_w, r_h = tag.rect()
            g_rect = (r_x, r_y, r_w, r_h)
            g_cx = tag.cx()
            g_cy = tag.cy()
            margin = tag.decision_margin()
            rot_deg = degrees(tag.rotation())
            rx = tag.x_rotation()
            ry = tag.y_rotation()
            rz = tag.z_rotation()
            # 6DoF 位姿（单位尺度取决于镜头与标定；旋转为弧度需转角度）
            tx = tag.x_translation()
            ty = tag.y_translation()
            tz = tag.z_translation()
            rx_deg = degrees(tag.x_rotation())
            ry_deg = degrees(tag.y_rotation())
            rz_deg = degrees(tag.z_rotation())

            # 与已收集目标比对，按中心距离阈值去重
            merged = False
            for d in detections:
                if (d["id"] == tag.id()):
                    dx = abs(g_cx - d["cx"])
                    dy = abs(g_cy - d["cy"])
                    # 阈值：取较小宽高中25%作为合并半径
                    merge_radius = min(g_rect[2], g_rect[3], d["rect"][2], d["rect"][3]) * 0.25
                    if (dx <= merge_radius) and (dy <= merge_radius):
                        # 更新为更可靠的检测（margin更大）
                        if margin > d["margin"]:
                            d["rect"] = g_rect
                            d["cx"] = g_cx
                            d["cy"] = g_cy
                            d["margin"] = margin
                            d["rot_deg"] = rot_deg
                            d["corners"] = [(int(px), int(py)) for (px, py) in tag.corners()]
                            d["tx"] = tx; d["ty"] = ty; d["tz"] = tz
                            d["rx_deg"] = rx_deg; d["ry_deg"] = ry_deg; d["rz_deg"] = rz_deg
                            d["rx"] = rx; d["ry"] = ry; d["rz"] = rz
                        merged = True
                        break

            if not merged:
                detections.append({
                    "id": tag.id(),
                    "rect": g_rect,
                    "cx": g_cx,
                    "cy": g_cy,
                    "margin": margin,
                    "rot_deg": rot_deg,
                    "corners": [(int(px), int(py)) for (px, py) in tag.corners()],
                    "tx": tx, "ty": ty, "tz": tz,
                    "rx_deg": rx_deg, "ry_deg": ry_deg, "rz_deg": rz_deg,
                    "rx": rx, "ry": ry, "rz": rz
                })

    # 绘制去重后的结果
    for d in detections:
        img.draw_rectangle(d["rect"], color=RED, thickness=2)
        img.draw_cross(d["cx"], d["cy"], color=GREEN, size=10, thickness=2)
        for (px, py) in d["corners"]:
            img.draw_circle(px, py, 3, color=BLUE, thickness=2)
        label = "id:%d m:%.1f z:%.2f rx:%.1f ry:%.1f rz:%.1f" % (
            d["id"], d["margin"], d["tz"], d["rx_deg"], d["ry_deg"], d["rz_deg"]
        )
        tx, ty, tw, th = d["rect"]
        img.draw_string(tx, max(0, ty - 12), label, color=YELLOW, mono_space=False, scale=1)
        # 2D 模拟 3D：用真实尺度投影三轴（X=红, Y=绿, Z=蓝）
        # 轴长度取标签边长的一半，单位与 TAG_SIZE_MM 一致
        axis_len = TAG_SIZE_MM * 0.5
        R = _rot_matrix(d["rx"], d["ry"], d["rz"])
        # 相机坐标系中标签中心
        C = (d["tx"], d["ty"], d["tz"])
        # 三轴端点（世界到相机：先旋转再平移）
        ex = _matmul3(R, [axis_len, 0.0, 0.0])
        ey = _matmul3(R, [0.0, axis_len, 0.0])
        ez = _matmul3(R, [0.0, 0.0, axis_len])
        Px = (C[0] + ex[0], C[1] + ex[1], C[2] + ex[2])
        Py = (C[0] + ey[0], C[1] + ey[1], C[2] + ey[2])
        Pz = (C[0] + ez[0], C[1] + ez[1], C[2] + ez[2])
        # 投影中心与端点
        p0 = _project_point(C[0], C[1], C[2])
        px = _project_point(Px[0], Px[1], Px[2])
        py = _project_point(Py[0], Py[1], Py[2])
        pz = _project_point(Pz[0], Pz[1], Pz[2])
        # 用检测到的 2D 中心对齐投影中心，避免内参误差导致偏移
        if p0:
            dx = int(d["cx"] - p0[0])
            dy = int(d["cy"] - p0[1])
            p0 = (p0[0] + dx, p0[1] + dy)
            if px: px = (px[0] + dx, px[1] + dy)
            if py: py = (py[0] + dx, py[1] + dy)
            if pz: pz = (pz[0] + dx, pz[1] + dy)
        else:
            p0 = (int(d["cx"]), int(d["cy"]))

        if px: img.draw_line(p0[0], p0[1], px[0], px[1], color=RED, thickness=2)
        if py: img.draw_line(p0[0], p0[1], py[0], py[1], color=GREEN, thickness=2)
        if pz: img.draw_line(p0[0], p0[1], pz[0], pz[1], color=BLUE, thickness=2)

    # 串口实时输出相对位姿（单位：mm 与弧度/度）
    if detections:
        for d in detections:
            # 简洁单行输出，便于上位机解析
            uart.write("id=%d,tx=%.2f,ty=%.2f,tz=%.2f,rx=%.3f,ry=%.3f,rz=%.3f,rx_deg=%.2f,ry_deg=%.2f,rz_deg=%.2f\n" % (
                d["id"], d["tx"], d["ty"], d["tz"],
                d["rx"], d["ry"], d["rz"],
                d["rx_deg"], d["ry_deg"], d["rz_deg"]
            ))
    else:
        uart.write("none\n")

    img.draw_string(2, 2, "FPS: %.1f" % clock.fps(), color=WHITE, scale=1)
