# uart_test.py
# OpenMV 串口测试：USB VCP + UART3(P4/P5)

import pyb, time

uart_vcp = pyb.USB_VCP()
uart_hw = pyb.UART(3, 19200, timeout_char=1000)

counter = 0
while True:
    msg = "TEST,%d\n" % counter
    if uart_vcp.isconnected():
        uart_vcp.write(msg)
    uart_hw.write(msg)
    counter += 1
    time.sleep_ms(500)
