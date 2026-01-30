import sensor, image, time, math, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

f_x = (2.8 / 3.984) * 160
f_y = (2.8 / 2.952) * 120
c_x = 160 * 0.5
c_y = 120 * 0.5
TAG_SIZE_MM = 100.0

# 蓝灯呼吸指示（程序运行中）
led = pyb.LED(3)  # 3 = 蓝灯
breath = 0
breath_dir = 5

# 串口输出：USB 虚拟串口优先（直连电脑）
USE_USB_VCP = True
if USE_USB_VCP:
    uart = pyb.USB_VCP()
    # 不阻塞等待，上位机连接后再输出
    if uart.isconnected():
        uart.write("APRILTAG VCP READY\n")
else:
    uart = pyb.UART(3, 115200, timeout_char=1000)
    uart.write("APRILTAG UART READY\n")

last_heartbeat = pyb.millis()

def degrees(radians):
    return (180 * radians) / math.pi

def normalize_deg(d):
    # 归一化到 [-180, 180]
    while d > 180:
        d -= 360
    while d < -180:
        d += 360
    return d

while True:
    clock.tick()
    # 呼吸灯（非阻塞）
    breath += breath_dir
    if breath >= 255:
        breath = 255
        breath_dir = -5
    elif breath <= 0:
        breath = 0
        breath_dir = 5
    led.intensity(breath)

    img = sensor.snapshot()
    found = False
    for tag in img.find_apriltags(families=image.TAG25H9, fx=f_x, fy=f_y, cx=c_x, cy=c_y, tag_size=TAG_SIZE_MM):
        found = True
        img.draw_rectangle(tag.rect(), color=(255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
        tx = tag.x_translation()
        ty = tag.y_translation()
        tz = tag.z_translation()
        rx_deg = normalize_deg(degrees(tag.x_rotation()))
        ry_deg = normalize_deg(degrees(tag.y_rotation()))
        rz_deg = normalize_deg(degrees(tag.z_rotation()))
        rx = math.radians(rx_deg)
        ry = math.radians(ry_deg)
        rz = math.radians(rz_deg)
        # 串口输出完整位姿信息（含角度与弧度）
        if (not USE_USB_VCP) or uart.isconnected():
            uart.write(
                "id=%d,tx=%.2f,ty=%.2f,tz=%.2f,rx=%.3f,ry=%.3f,rz=%.3f,rx_deg=%.2f,ry_deg=%.2f,rz_deg=%.2f\n"
                % (tag.id(), tx, ty, tz, rx, ry, rz, rx_deg, ry_deg, rz_deg)
            )
    # 心跳：1 秒输出一次，方便确认串口连通
    if not found:
        now = pyb.millis()
        if (now - last_heartbeat) > 1000:
            if (not USE_USB_VCP) or uart.isconnected():
                uart.write("none\n")
            last_heartbeat = now
    # print(clock.fps())
