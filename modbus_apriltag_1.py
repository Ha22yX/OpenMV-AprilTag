import sensor, image
import time
from machine import UART, LED
from modbus import ModbusRTU

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)

# 蓝色 LED 指示运行状态
led = LED("LED_BLUE")
led.on()

uart = UART(3, 115200, parity=None, stop=2, timeout=1, timeout_char=4)
modbus = ModbusRTU(uart, register_num=9999)

sensor.skip_frames(time=2000)
clock = time.clock()

# 相机内参（按 2.8mm 镜头估算，可按实际标定修改）
f_x = (2.8 / 3.984) * 160
f_y = (2.8 / 2.952) * 120
c_x = 160 * 0.5
c_y = 120 * 0.5
TAG_SIZE_MM = 100.0

# 缩放系数（将浮点映射到 16-bit 寄存器）
POS_SCALE = 100    # mm * 100 -> 0.01mm
ROT_SCALE = 1000   # rad * 1000

while True:
    if modbus.any():
        modbus.handle(debug=True)
    else:
        clock.tick()
        img = sensor.snapshot()
        tags = img.find_apriltags(families=image.TAG36H11,
                                  fx=f_x, fy=f_y, cx=c_x, cy=c_y,
                                  tag_size=TAG_SIZE_MM)
        modbus.clear()
        modbus.REGISTER[0] = len(tags)
        if tags:
            i = 1
            for tag in tags:
                img.draw_rectangle(tag.rect(), color=127)
                modbus.REGISTER[i] = tag.family(); i += 1
                modbus.REGISTER[i] = tag.id();     i += 1
                modbus.REGISTER[i] = tag.cx();     i += 1
                modbus.REGISTER[i] = tag.cy();     i += 1
                # 3D 位姿（相机坐标系）
                modbus.REGISTER[i] = int(tag.x_translation() * POS_SCALE); i += 1
                modbus.REGISTER[i] = int(tag.y_translation() * POS_SCALE); i += 1
                modbus.REGISTER[i] = int(tag.z_translation() * POS_SCALE); i += 1
                modbus.REGISTER[i] = int(tag.x_rotation() * ROT_SCALE);    i += 1
                modbus.REGISTER[i] = int(tag.y_rotation() * ROT_SCALE);    i += 1
                modbus.REGISTER[i] = int(tag.z_rotation() * ROT_SCALE);    i += 1
