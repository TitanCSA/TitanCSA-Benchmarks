---
title: Vdevice vs vJoy — virtual joystick state visibility through WinMM
description: Matched X/Y axes and eight buttons measured through an independent WinMM receiver, with raw observed states and per-run PnP evidence.
---
# Vdevice vs vJoy: a joystick comparison

This compares a shared subset of joystick functionality: two axes and eight selected buttons. Vdevice uses a descriptor-driven USB HID joystick; vJoy 2.2.2.0 (BrunnerInnovation distribution) uses its own virtual HID driver and SDK. A separate executable observes each state through Windows `joyGetPosEx`. This is not an XInput or Xbox-controller benchmark.

| Backend | Release | Runs | States | Median run P50 (µs) | Median run P99 (µs) |
|---|---|---:|---:|---:|---:|
| vdevice | 1.0.5.0 | 3 | 3000 | 34.35 | 238.64 |
| vjoy | 2.2.2.0 | 3 | 3000 | 7.20 | 40.82 |

The producer waits for acknowledgement after independent observation; only one state is outstanding. WinMM normalization is checked against the declared logical axis range and Windows capability ranges, with a three-unit tolerance for integer scaling. Consecutive states are separated by much more than that tolerance and use distinct button bits. Raw CSV includes observed X/Y/buttons, sequence and QPC timestamps.

The two devices expose more capabilities than this shared subset. vJoy force feedback, additional axes/buttons, USB control handling and other transports are not scored here. WinMM polling, SDK work and scheduling are included. These are software-path measurements in one Hyper-V VM, not physical latency or a universal driver ranking.

[Per-run joystick data](../assets/joystick-results.json) · [Raw archive](../assets/raw-results.zip) · [Methodology](../methodology/measurement.md)
