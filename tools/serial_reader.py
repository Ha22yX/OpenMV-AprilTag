# read_com20.py
# 读取 COM20 串口并实时打印
# 依赖：pip install pyserial

import serial

PORT = "COM20"
BAUD = 115200


def main():
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print(f"Opened {PORT} @ {BAUD}")
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                print(line)


if __name__ == "__main__":
    main()

