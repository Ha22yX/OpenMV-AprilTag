<div align="center">
  <h1>OpenMV AprilTag</h1>
  <p>面向母机对接系统近距离视觉定位的 OpenMV AprilTag 位姿估计工作区。</p>

  <p>
    <a href="README.md">English</a>
    &middot;
    <a href="#快速开始">快速开始</a>
    &middot;
    <a href="#核心能力">核心能力</a>
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

## 项目概览

这个仓库隔离了 Mother-Ship 对接系统中的末端视觉模块。

UWB 负责中距离相对定位；当 OpenMV 能看到标签时，AprilTag 视觉用于进一步细化近距离对准。

## 核心能力

- OpenMV AprilTag 检测与位姿输出脚本。
- USB VCP 和 UART 输出路径，便于下游设备读取。
- PC 串口读取器和 3D 位姿查看器。
- 保留历史实验作为参考。
- 与 UWB 仓库和主对接项目互相引用。

## 工作方式

1. 在 OpenMV 上运行 AprilTag 脚本。
2. 使用相机内参和标签尺寸估计平移/旋转。
3. 通过 UART 或 USB VCP 输出位姿行。
4. 用 PC 工具检查方向、稳定性和对准行为。
5. 准备好后把位姿流接入对接控制链路。

## 快速开始

可以用下面的命令在本地运行项目。

```bash
git clone https://github.com/Ha22yX/OpenMV-AprilTag.git
cd OpenMV-AprilTag
pip install -r tools/requirements.txt
# Run openmv/apriltag_pose_uart.py in OpenMV IDE
python tools/serial_reader.py
```

请根据实际硬件校准相机内参、标签尺寸、串口和波特率。

## 配置项

| 项目 | 作用 |
| --- | --- |
| 相机内参 | 位姿估计可信的前提。 |
| 标签族/尺寸 | 必须与打印的 AprilTag 标记一致。 |
| 串口输出 | 设置 UART/USB 模式、端口和波特率。 |
| 坐标约定 | 接入控制前必须确认轴向。 |

## 技术栈

| 层级 | 技术 | 作用 |
| --- | --- | --- |
| 相机 | OpenMV | 嵌入式 AprilTag 检测。 |
| 标记 | AprilTag TAG25H9 | 末端视觉参考。 |
| 输出 | UART / USB VCP | 向下游硬件输出位姿流。 |
| 工具 | Python, pyserial, matplotlib, PyQtGraph | 读取并可视化位姿流。 |

## 项目结构

```text
openmv/                 OpenMV 相机脚本
tools/                  PC 串口和 3D 可视化工具
archive/                历史实验
.github/assets/         README 概览图
```

## 项目状态

台架测试定位模块。它与 UWB 互补，接入飞行/控制前必须独立验证。

## 相关项目

- [Mother-Ship-Docking-Drone-System](https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System) - 主对接项目。
- [UWB-Project](https://github.com/Ha22yX/UWB-Project) - 中距离相对定位模块。

## 许可证

当前仓库尚未声明项目级开源许可证；公开复用或分发前建议先补充 License。
