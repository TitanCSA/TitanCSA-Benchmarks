---
title: Windows input driver compatibility — observed vs documented
description: Compatibility matrix distinguishing independently received virtual profiles, source-reviewed examples and unexecuted physical controller tests.
published: 2026-11-17
updated: 2026-11-17
---
# Compatibility evidence

| Project / profile | Source/documentation | This lab's runtime status |
|---|---|---|
| Vdevice vendor-defined HID | Descriptor-driven UdeCx | Independently received through Windows HID |
| Vdevice virtual Xbox 360 | Published Xbox360 example | Independently received through XInput |
| ViGEmBus virtual Xbox 360 | Public X360 client API | Independently received through XInput |
| Vdevice keyboard/mouse | Published HID examples and lab descriptors | Inspect raw-input result records; no universal hardware claim |
| Vdevice DS4 / Xbox One GIP | Published examples | Independent HID/XInput delivery measured; see protocol-specific results |
| Interceptor controller HID/XUSB/GIP | Source and SDK paths | XUSB modification verified; the original DS4 campaign includes WDF-001. Teardown fix validation applies to signed demo 1.0.6.0 |
| HidHide | Device access/visibility control | Audited; not scored as interception |
| libvirtualhid Windows profiles | Backend-specific upstream documentation | Not installed; license required |
| vJoy (BrunnerInnovation 2.2.2.0) | Virtual joystick model | Independent WinMM X/Y/button comparison executed; not an XInput score |

No entry establishes physical controller compatibility or all-Windows-build support. See [environment](../methodology/environment.md) and [limitations](../methodology/limitations.md).

