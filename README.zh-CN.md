<div align="center">
  <h1>OpenMV AprilTag</h1>
  <p>面向 Mother-Ship 对接系统近距离视觉定位的 OpenMV AprilTag 位姿估计仓库。</p>

  <p>
    <a href="README.md">English</a>
    &middot;
    <a href="https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System">主项目</a>
    &middot;
    <a href="https://github.com/Ha22yX/UWB-Project">UWB 模块</a>
    &middot;
    <a href="#快速开始">快速开始</a>
    &middot;
    <a href="#技术栈">技术栈</a>
  </p>

  <p>
    <img alt="OpenMV: AprilTag" src="https://img.shields.io/badge/OpenMV-AprilTag-287866?style=for-the-badge" />
    <img alt="Python: tools" src="https://img.shields.io/badge/Python-tools-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="Vision: 6DoF pose" src="https://img.shields.io/badge/Vision-6DoF%20pose-7d73b7?style=for-the-badge" />
    <img alt="Status: bench tests" src="https://img.shields.io/badge/Status-bench%20tests-6b7f73?style=for-the-badge" />
  </p>
</div>

<p align="center">
  <img src=".github/assets/readme-hero.svg" alt="OpenMV AprilTag 项目概览图" width="100%" />
</p>

## 项目价值

UWB 提供中距离位置估计，但最终对接还需要近距离视觉位姿参考。本仓库把 AprilTag 路径独立出来，便于单独测试相机、串口输出和可视化工具。

## 工作流

- 在 OpenMV 上运行 AprilTag 脚本。
- 根据相机内参和标签尺寸估计目标标签的平移/旋转。
- 通过 USB VCP 或 UART 输出单行位姿消息。
- 使用 PC 工具验证坐标方向、稳定性和对准表现。
- 把位姿流接入对接控制器或 ESP32 伴随链路。

## 核心功能

- OpenMV AprilTag 检测和位姿输出脚本。
- USB VCP 与 UART3 输出路径。
- 串口读取器、matplotlib 和 pyqtgraph 3D 查看器。
- 作为对接项目的末端视觉定位模块。

## 快速开始

```bash
git clone https://github.com/Ha22yX/OpenMV-AprilTag.git
cd OpenMV-AprilTag
pip install -r tools/requirements.txt
# Run openmv/apriltag_pose_uart.py in OpenMV IDE
python tools/serial_reader.py
```

请根据实际硬件校准相机内参、标签尺寸、串口和波特率。

## 技术栈

| 层级 | 技术 | 作用 |
| --- | --- | --- |
| 相机 | OpenMV | 运行嵌入式 AprilTag 检测。 |
| 标记 | AprilTag TAG25H9 | 提供末端位姿参考。 |
| 输出 | UART / USB VCP | 向下游硬件输出位姿行。 |
| 工具 | Python, pyserial, matplotlib, PyQtGraph | 读取并可视化位姿流。 |

## 项目结构

```text
openmv/                 OpenMV camera scripts
tools/                  PC serial and 3D visualization tools
archive/                older experiments
```

## 项目说明

该模块与 UWB 互补：UWB 负责中距离位置，AprilTag 视觉负责近距离对准。
