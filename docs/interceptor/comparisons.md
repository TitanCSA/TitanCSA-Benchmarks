---
title: Interception V2 and oblitum Interception — compatibility vs performance
description: Separate original Interception ABI compatibility, filter attachment and independent keyboard/mouse delivery measurements before comparing implementations.
published: 2026-11-17
updated: 2026-11-17
---
# Interception compatibility is not a latency result

oblitum/Interception supplies the original C API and a keyboard/mouse interception driver. TitanCSA Interception V2 exposes the original SDK ABI through a different implementation. The combined Interceptor product uses its own C++ API. A shared application ABI makes equivalent test applications possible; it does not establish identical filter positions or performance.

Pin both driver versions and the original DLL, restore clean installations, enumerate supported test devices and verify receive/forward behavior before timing. Classic class-filter installations may need a guest restart. If a generated virtual HID does not traverse a driver, that scenario must remain unmeasured for that driver.

[Pinned repositories](../comparisons/index.md) · [Method](../methodology/measurement.md)

