---
title: Windows gamepad interception driver benchmark — HID, XUSB and GIP
description: Why virtual controller creation and physical gamepad report interception require different tests, with protocol-specific measurement boundaries.
published: 2026-11-17
updated: 2026-11-17
---
# Gamepad interception: separate the protocols

The combined Interceptor and controller-only edition expose HID, XUSB/XInput, XInputHID and GIP paths under product-specific masks. Source paths and SDK types are inspected in the [audit](../comparisons/index.md). Runtime support must be demonstrated for each descriptor, connection and Windows path.

The [virtual Xbox 360 comparison](../vdevice/comparisons.md) measures device creation/state delivery, not interception of an external gamepad. No HID result is generalized to GIP, Bluetooth or physical USB controllers.

For a valid interception test, submit known virtual states, prove filter attachment and capture, modify a chosen button/stick/trigger, then verify the result with independent XInput or HID. Blocked-state checks must account for XInput polling: a state not observed by an application is not automatically a dropped kernel report. Protocol-specific physical-device and reconnect campaigns remain outside the currently measured dataset.

