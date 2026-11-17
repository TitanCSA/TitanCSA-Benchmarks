---
title: KMDF vs UMDF virtual HID performance — what a fair test requires
description: Compare kernel and user-mode virtual HID architectures only with matched profiles, independent receivers and measured Windows paths.
published: 2026-11-17
updated: 2026-11-17
---
# KMDF vs UMDF: architecture is not a benchmark

KMDF and UMDF place different components in different execution environments. A framework label alone cannot predict latency: transport, batching, scheduling, SDK logic and receiver API matter.

Vdevice uses KMDF/UdeCx USB emulation. Microsoft's documented VHF HID source architecture uses a kernel-mode source driver and an inbox HID tree. The current libvirtualhid README describes Windows driver-backed UMDF paths; its exact implementation and required license must be evaluated before any numerical comparison. These descriptions should not be collapsed into one interchangeable HID stack.

An honest comparison needs the same functional HID profile, report sizes, source schedule, independent receiver, Windows build, security policy and measured endpoint. No KMDF-versus-UMDF performance ranking has been executed in this campaign. The current [results](../vdevice/latency.md) cover one UdeCx vendor-HID path.

References: [Microsoft VHF architecture](https://learn.microsoft.com/en-us/windows-hardware/drivers/hid/virtual-hid-framework--vhf-), [upstream libvirtualhid](https://github.com/LizardByte/libvirtualhid).

