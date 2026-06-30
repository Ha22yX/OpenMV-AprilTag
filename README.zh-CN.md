# OpenMV-AprilTag

[English](README.md)

OpenMV-AprilTag 是无人机空中对接项目中的 AprilTag 视觉定位实验仓库。它的定位是一个冗余定位系统：当 UWB 测距噪声较大、暂时不可用，或者需要在对接目标附近进行交叉验证时，OpenMV 相机可以通过识别 AprilTag 估计相对位姿，并把位姿数据输出给后续控制系统。

这个仓库包含 OpenMV 端 AprilTag 检测与位姿输出脚本，也包含 PC 端串口读取和 3D 可视化工具。项目结构面向桌面调试、相机标定实验，以及子母无人机对接系统中的视觉定位集成。

## 项目用途

- 在 OpenMV 上检测 AprilTag 并估计 6DoF 相对位姿。
- 通过 USB VCP 或 UART 输出标签位姿，供飞控、ESP32 或伴随计算设备使用。
- 为近距离无人机对接提供视觉冗余定位方案。
- 在 PC 端实时可视化位姿数据，方便台架测试。
- 保留旧版 OpenMV 实验脚本，但与当前主线脚本分开。

## 项目结构

```text
openmv/
  apriltag_pose_uart.py   当前主用 OpenMV AprilTag 位姿检测与串口输出脚本。
  uart_test.py            OpenMV USB VCP + UART3 输出测试脚本。

tools/
  world_camera.py         pyqtgraph 3D 查看器：固定标签，显示相机位姿。
  matplotlib_pose_viewer.py
                          Matplotlib 3D 位姿查看器。
  serial_reader.py        最小串口监视器，用于查看位姿输出行。
  requirements.txt        PC 工具的 Python 依赖。

archive/
  openmv-experiments/     旧版或备选 OpenMV AprilTag 实验。
```

## 主 OpenMV 脚本

主脚本：

```text
openmv/apriltag_pose_uart.py
```

该脚本会：

- 使用 OpenMV AprilTag 检测，默认标签族为 `TAG25H9`。
- 根据相机内参和标签尺寸估计平移与旋转。
- 输出单行位姿数据：

```text
id=0,tx=12.34,ty=-5.67,tz=345.89,rx=0.012,ry=-0.034,rz=0.567,rx_deg=0.69,ry_deg=-1.95,rz_deg=32.50
```

- 看不到标签时输出 `none`。
- 使用简单的跳变过滤和指数滑动平均平滑数据。
- 同时支持 USB VCP 和 UART3 输出。
- 使用 LED 指示运行状态和标签检测状态。

默认串口输出：

```text
UART3 P4/P5 @ 19200 baud
USB VCP when connected
```

## PC 可视化工具

安装依赖：

```bash
pip install -r tools/requirements.txt
```

运行前根据本机串口修改脚本顶部的 `PORT` 和 `BAUD` 常量。

常用命令：

```bash
python tools/serial_reader.py
python tools/matplotlib_pose_viewer.py
python tools/world_camera.py
```

`world_camera.py` 会把 AprilTag 视为固定在世界坐标系中，并显示相机相对标签的位姿。这个工具很适合检查对接目标对准过程中的坐标方向和稳定性。

## 标定说明

OpenMV 脚本目前使用常见 OpenMV 相机/镜头组合的估算内参：

```text
focal_length_mm = 2.8
sensor_w_mm = 3.984
sensor_h_mm = 2.952
TAG_SIZE_MM = 100.0
```

如果要提高对接精度，建议对实际镜头和标签尺寸进行标定，然后更新主脚本中的焦距、传感器尺寸和 `TAG_SIZE_MM`。位姿质量会受到光照、标签打印质量、运动模糊、标签尺寸和相机安装刚性的明显影响。

## 集成说明

在无人机对接系统中，这一路视觉位姿可以作为：

- UWB 之外的冗余位置估计。
- 对接目标进入视野后的近距离对准辅助。
- 对 UWB 相对位置结果的交叉验证。
- 最终接近阶段实验中的 fallback 或置信度信号。

推荐数据流：

```text
AprilTag 目标 -> OpenMV 相机 -> USB/UART 位姿行 -> ESP32/伴随计算设备 -> 对接控制器
```

## OpenMV 使用流程

1. 在 OpenMV IDE 中打开 `openmv/apriltag_pose_uart.py`。
2. 检查 `TAG_SIZE_MM` 和相机内参常量。
3. 根据集成方式选择 USB VCP 或 UART3 输出。
4. 运行脚本，确认 OpenMV 串口终端中有位姿输出。
5. 使用 `tools/` 下的 PC 查看器确认坐标方向和稳定性。

## License

当前仓库暂未包含 license 文件。
