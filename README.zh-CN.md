<div align="center">
  <h1>OpenMV AprilTag</h1>
  <p>面向 Mother-Ship 对接系统近距离视觉定位的 OpenMV AprilTag 位姿估计仓库。</p>

  <p>
    <a href="README.md">English</a>
    &middot;
    <a href="#快速开始">快速开始</a>
    &middot;
    <a href="#技术栈">技术栈</a>
    &middot;
    <a href="https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System">主项目</a>
    &middot;
    <a href="https://github.com/Ha22yX/UWB-Project">UWB 模块</a>
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

UWB 适合中距离相对定位，但末端对接还需要可见目标后的视觉位姿信号。本仓库把 OpenMV + AprilTag 这条路径独立出来验证。

## 快速开始

```bash
git clone https://github.com/Ha22yX/OpenMV-AprilTag.git
cd OpenMV-AprilTag
pip install -r tools/requirements.txt
# 在 OpenMV IDE 中运行 openmv/apriltag_pose_uart.py
python tools/serial_reader.py
```

请根据实际硬件修改相机内参、标签尺寸、串口和波特率。

## 核心功能

- OpenMV 脚本用于 AprilTag 检测和位姿输出。
- 支持 USB VCP 与 UART 位姿行输出，便于下游控制器接入。
- 提供 PC 串口监视器、matplotlib 和 pyqtgraph 可视化工具。
- 作为对接项目的末端视觉定位模块。

## 技术栈

| Layer | Technology | Role |
| --- | --- | --- |
| 相机 | OpenMV | 在嵌入式相机上运行 AprilTag 检测。 |
| 标记 | AprilTag TAG25H9 | 提供末端位姿参考。 |
| 工具 | Python, pyserial, matplotlib, PyQtGraph | 读取并可视化位姿流。 |
| 集成 | UART / USB VCP | 把位姿行发送给 ESP32 或伴随计算机。 |


## 项目说明

这是 [Mother-Ship-Docking-Drone-System](https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System) 的附属仓库，与 [UWB-Project](https://github.com/Ha22yX/UWB-Project) 互补：UWB 负责中距离相对位置，AprilTag 视觉负责末端对准。


## 项目结构

```text
openmv/    OpenMV camera scripts
tools/     PC serial and 3D visualization tools
archive/   older experiments
```
