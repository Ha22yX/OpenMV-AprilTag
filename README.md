<div align="center">
  <h1>OpenMV AprilTag</h1>
  <p>AprilTag pose-estimation workspace for close-range visual localization in the Mother-Ship docking system.</p>

  <p>
    <a href="README.zh-CN.md">Chinese</a>
    &middot;
    <a href="https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System">Main Project</a>
    &middot;
    <a href="https://github.com/Ha22yX/UWB-Project">UWB Module</a>
    &middot;
    <a href="#quickstart">Quickstart</a>
    &middot;
    <a href="#tech-stack">Tech Stack</a>
  </p>

  <p>
    <img alt="OpenMV: AprilTag" src="https://img.shields.io/badge/OpenMV-AprilTag-287866?style=for-the-badge" />
    <img alt="Python: tools" src="https://img.shields.io/badge/Python-tools-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="Vision: 6DoF pose" src="https://img.shields.io/badge/Vision-6DoF%20pose-7d73b7?style=for-the-badge" />
    <img alt="Status: bench tests" src="https://img.shields.io/badge/Status-bench%20tests-6b7f73?style=for-the-badge" />
  </p>
</div>

<p align="center">
  <img src=".github/assets/readme-hero.svg" alt="OpenMV AprilTag overview image" width="100%" />
</p>

## Why This Exists

UWB provides the mid-range position estimate, but final docking needs a short-range visual pose reference. This repo isolates the AprilTag path so the camera, serial output, and visualization tools can be tested independently.

## Workflow

- Run the AprilTag script on OpenMV.
- Detect the target tag and estimate translation/rotation from camera intrinsics and tag size.
- Output one-line pose messages through USB VCP or UART.
- Use PC tools to verify pose direction, stability, and alignment behavior.
- Feed the pose stream into the docking controller or ESP32 companion path.

## Features

- OpenMV AprilTag detection and pose-output script.
- USB VCP and UART3 output path.
- Serial reader plus matplotlib and pyqtgraph 3D viewers.
- Designed as the terminal visual localization module for the docking project.

## Quickstart

```bash
git clone https://github.com/Ha22yX/OpenMV-AprilTag.git
cd OpenMV-AprilTag
pip install -r tools/requirements.txt
# Run openmv/apriltag_pose_uart.py in OpenMV IDE
python tools/serial_reader.py
```

Calibrate camera intrinsics, tag size, serial port, and baud rate for your hardware.

## Tech Stack

| Layer | Technology | Role |
| --- | --- | --- |
| Camera | OpenMV | Runs embedded AprilTag detection. |
| Marker | AprilTag TAG25H9 | Provides the terminal pose reference. |
| Output | UART / USB VCP | Streams pose lines to downstream hardware. |
| Tools | Python, pyserial, matplotlib, PyQtGraph | Read and visualize pose streams. |

## Project Map

```text
openmv/                 OpenMV camera scripts
tools/                  PC serial and 3D visualization tools
archive/                older experiments
```

## Notes

This module complements UWB: UWB estimates mid-range position, AprilTag vision refines close-range alignment.
