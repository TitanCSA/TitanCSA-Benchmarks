---
title: Windows virtual USB device performance — Vdevice architecture
description: Source-reviewed UdeCx virtual USB architecture, verified vendor HID and Xbox 360 profiles, and the boundaries of current Vdevice measurements.
published: 2026-11-17
updated: 2026-11-17
---
# Vdevice: virtual USB devices

Vdevice exposes descriptor-driven virtual USB functions through a C++17 SDK and a KMDF/UdeCx driver. The source defines bounded queues and a shared one-hour evaluation allowance; neither was patched for this campaign. HID vendor-defined reports and Xbox 360 state delivery were functionally received by independent Windows applications.

The source includes keyboard, mouse, Xbox 360, DS4 and Xbox One/GIP examples. Their presence is an integration starting point, not runtime qualification for every profile. Read the [audit](../comparisons/index.md), [measured vendor HID result](latency.md) and [Xbox 360 comparison](comparisons.md).

Creation-call time, Windows enumeration, first observed input and deletion-call time are separate milestones. A deletion API returning does not establish that every PnP node has disappeared. Queueing, delegated USB controls and Windows inbox drivers are part of the tested path.

