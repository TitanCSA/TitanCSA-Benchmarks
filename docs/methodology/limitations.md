---
title: Benchmark limitations, failed runs and untested paths
description: Explicit boundaries for the TitanCSA benchmark campaign, including virtual-only inputs, disabled guest HVCI and unexecuted hardware and endurance tests.
---
# Limits are part of the result

- This is a **publisher-operated laboratory**, not an independent certification. TitanCSA develops some of the tested drivers.
- Measurements use one Windows 11 Hyper-V guest and one host. Host workloads were not frozen. Results do not generalize to every PC, Windows build, controller or driver version.
- Secure Boot is enabled, but guest HVCI is not enabled. Passing these tests does not establish HVCI qualification, HLK compliance, absence of memory leaks or production stability.
- No physical keyboard, mouse, USB gamepad, USB analyzer or external timing apparatus was used. No physical input latency or Bluetooth transport latency is measured.
- XInput exposes state. The closed-loop benchmark waits for observation; unobserved intermediate states in a free-running test would not automatically prove report loss.
- USB emulation, VHF, joystick creation, device hiding and input filtering are different architectures. A global best-driver ranking would be misleading.
- Windows `libvirtualhid` driver-backed profiles require a license according to upstream documentation. No license was purchased or bypassed. Source review is not a runtime performance result.
- oblitum/Interception documents separate commercial-use terms. No commercial license was identified for this publisher's promotional comparison, so its driver is not installed or scored. Its public source and ABI are audited.
- Microsoft VHF/UdeCx samples were identified as reference architectures; no newly compiled unsigned sample driver was treated as a signed, working competitor.
- DS4 and Xbox One/GIP have selected virtual delivery results, not exhaustive protocol coverage. GIP-filter and ViGEm-filter attempts with extra uncorrelated captured reports remain excluded from the latency table.
- Multi-hour soak, crash-injection, physical reconnect, DualSense, physical-device protocol coverage and total driver CPU attribution require additional campaigns. A five-minute monitored HID trial and one separately instrumented WPR/DPC trial are available; neither establishes long-term stability.
- WDF-001 recorded a guest bugcheck in DS4 and GIP runs using Vdevice demo 1.0.5.0. The signed 1.0.6.0 demo includes the fix and passed separate teardown tests. The [signed Release 1.0.4.1 record](https://titancsa.github.io/assets/vdevice-signed-versions-2026-11-25.json) covers upgrade, removal and readiness before activation. See the [incident and test scope](incident-wdf-001.md).

Failed runs are listed in the processed results and retained with their diagnostics. No simulation enters the measured charts. No superiority claim is made from a feature checklist or from an unverified filter path.
