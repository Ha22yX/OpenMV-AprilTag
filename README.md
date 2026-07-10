<div align="center">
  <h1>OpenMV AprilTag</h1>
  <p>AprilTag pose-estimation workspace for close-range visual localization in the Mother-Ship docking system.</p>

  <p>
    <a href="README.zh-CN.md">Chinese</a>
    &middot;
    <a href="#quickstart">Quickstart</a>
    &middot;
    <a href="#tech-stack">Tech Stack</a>
    &middot;
    <a href="https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System">Main Project</a>
    &middot;
    <a href="https://github.com/Ha22yX/UWB-Project">UWB Module</a>
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

UWB gives the docking system a mid-range relative position estimate, but the final approach needs a visual pose signal when the tag is in view. This repo isolates that OpenMV + AprilTag path.

## Quickstart

```bash
git clone https://github.com/Ha22yX/OpenMV-AprilTag.git
cd OpenMV-AprilTag
pip install -r tools/requirements.txt
# Run openmv/apriltag_pose_uart.py in OpenMV IDE
python tools/serial_reader.py
```

Update camera intrinsics, tag size, serial port, and baud rate for your hardware.

## Features

- OpenMV script for AprilTag detection and pose output.
- USB VCP and UART pose-line output for downstream controllers.
- PC serial monitor plus matplotlib and pyqtgraph viewers.
- Designed as the terminal visual localization module for the docking project.

## Tech Stack

| Layer | Technology | Role |
| --- | --- | --- |
| Camera | OpenMV | Runs AprilTag detection on embedded camera hardware. |
| Marker | AprilTag TAG25H9 | Provides terminal pose reference. |
| Tools | Python, pyserial, matplotlib, PyQtGraph | Read and visualize pose streams. |
| Integration | UART / USB VCP | Pass pose lines to ESP32 or a companion computer. |


## Project Notes

This is a companion repository for [Mother-Ship-Docking-Drone-System](https://github.com/Ha22yX/Mother-Ship-Docking-Drone-System). It complements [UWB-Project](https://github.com/Ha22yX/UWB-Project): UWB estimates mid-range relative position, AprilTag vision helps with final alignment.


## Project Map

```text
openmv/    OpenMV camera scripts
tools/     PC serial and 3D visualization tools
archive/   older experiments
```
