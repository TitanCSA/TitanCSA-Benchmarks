---
title: Windows keyboard and mouse interception benchmark — validation scope
description: Keyboard and mouse benchmark design, product-specific SDK boundaries, input-filter attachment requirements and available independent Raw Input checks.
published: 2026-11-17
updated: 2026-11-17
---
# Keyboard and mouse interception

Interceptor and its Keyboard & Mouse edition use product-specific C++17 APIs with capture batches and explicit forwarding. Interception V2 preserves the original C ABI through its own compatibility backend. These APIs and driver identities are not interchangeable.

The lab's keyboard/mouse scenarios create only authorized Vdevice HID fixtures. An independent Raw Input receiver on the guest desktop records their content and timestamps. Before interpreting a filter result, verify the PnP stack, captured-source identity, capture count and forwarding/modification/blocking outcome. A service being Running is insufficient.

The vendor-HID results on this site do not traverse these filters. They must not be advertised as keyboard/mouse filter overhead. The [measurement guide](../methodology/measurement.md) defines the correlation rules. [Raw runs](../data.md) distinguish completed, invalid and not-executed cases.

## Practical integration

Use a matching driver, SDK and example from one edition. Restore a clean VM before switching overlapping filters. Without a capture owner, input pass-through and emergency recovery are separate functional requirements that need testing. No real host input is captured by this lab.

