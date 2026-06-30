# OpenMV-AprilTag

[中文说明](README.zh-CN.md)

OpenMV-AprilTag is the AprilTag visual positioning workspace for a UAV aerial docking project. It is intended as a redundant localization system: when UWB ranging is noisy, unavailable, or needs cross-checking near the docking target, an OpenMV camera can estimate relative pose from an AprilTag and stream that pose to the rest of the system.

The repository contains OpenMV scripts for AprilTag detection and pose output, plus desktop tools for serial reading and 3D visualization. The project is organized for quick bench testing, camera calibration experiments, and integration with a parent-child UAV docking pipeline.

## Purpose

- Detect AprilTags on OpenMV and estimate 6DoF relative pose.
- Output tag pose over USB VCP and/or UART for downstream flight-control or companion-controller use.
- Provide a redundant visual localization path for close-range UAV docking.
- Visualize pose streams on a PC during bench tests.
- Keep older OpenMV experiments available without mixing them with the active script.

## Repository Structure

```text
openmv/
  apriltag_pose_uart.py   Main OpenMV script for AprilTag pose detection and serial output.
  uart_test.py            OpenMV USB VCP + UART3 output test.

tools/
  world_camera.py         pyqtgraph 3D viewer: fixed tag, moving camera pose.
  matplotlib_pose_viewer.py
                          Matplotlib 3D viewer for AprilTag pose output.
  serial_reader.py        Minimal serial monitor for pose lines.
  requirements.txt        Python dependencies for PC tools.

archive/
  openmv-experiments/     Older or alternate OpenMV AprilTag experiments.
```

## Main OpenMV Script

Use:

```text
openmv/apriltag_pose_uart.py
```

The script:

- Uses OpenMV AprilTag detection with the `TAG25H9` family.
- Estimates translation and rotation from camera intrinsics and tag size.
- Outputs one-line pose messages:

```text
id=0,tx=12.34,ty=-5.67,tz=345.89,rx=0.012,ry=-0.034,rz=0.567,rx_deg=0.69,ry_deg=-1.95,rz_deg=32.50
```

- Sends `none` when no tag is visible.
- Applies simple jump rejection and exponential moving average smoothing.
- Writes to USB VCP and UART3.
- Uses LEDs as runtime/detection indicators.

Default UART output:

```text
UART3 P4/P5 @ 19200 baud
USB VCP when connected
```

## PC Visualization Tools

Install dependencies:

```bash
pip install -r tools/requirements.txt
```

Then edit the `PORT` and `BAUD` constants near the top of each script for your local serial device.

Common commands:

```bash
python tools/serial_reader.py
python tools/matplotlib_pose_viewer.py
python tools/world_camera.py
```

`world_camera.py` treats the AprilTag as fixed in the world and renders the camera pose relative to it, which is useful for docking-target alignment tests.

## Calibration Notes

The OpenMV scripts currently use estimated intrinsics for a common OpenMV camera/lens setup:

```text
focal_length_mm = 2.8
sensor_w_mm = 3.984
sensor_h_mm = 2.952
TAG_SIZE_MM = 100.0
```

For better docking accuracy, calibrate the actual lens and tag size, then update the focal length, sensor dimensions, and `TAG_SIZE_MM` in the active OpenMV script. Pose quality is strongly affected by lighting, tag print quality, motion blur, tag size, and camera mounting rigidity.

## Integration Notes

For the UAV docking system, this visual pose stream can be used as:

- A redundant position estimate alongside UWB.
- A short-range alignment aid when the docking target is in view.
- A sanity check for UWB-derived relative position.
- A fallback or confidence signal during final approach experiments.

Recommended data flow:

```text
AprilTag target -> OpenMV camera -> USB/UART pose line -> ESP32/companion computer -> docking controller
```

## OpenMV Setup

1. Open `openmv/apriltag_pose_uart.py` in OpenMV IDE.
2. Check `TAG_SIZE_MM` and camera intrinsic constants.
3. Choose USB VCP or UART3 output depending on your integration.
4. Run the script and verify that pose lines appear in the OpenMV serial terminal.
5. Use a PC viewer from `tools/` to confirm coordinate direction and stability.

## License

No license file is currently included.
