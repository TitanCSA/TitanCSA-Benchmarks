---
title: Gamepad report interception and delivery — protocol-specific results
description: Independently verified virtual Xbox 360, DS4 and GIP state delivery, including captured and modified states where the tested filter path is proven.
---
# Gamepad results by protocol

These are virtual source devices. HID ReadFile and XInput are different observation APIs; their numbers must not be pooled into a global ranking. Every filtered row additionally requires PnP attachment, the complete generated capture count and independently observed modified content.

| Profile | Receiver | Backend | Filter | Operation | Runs | States | Median run P50 (µs) | Median run P99 (µs) |
|---|---|---|---|---|---:|---:|---:|---:|
| ds4 | HID ReadFile | vdevice | Gamepad-Controller | modify | 2 | 2000 | 82.28 | 743.40 |
| ds4 | HID ReadFile | vdevice | baseline | forward | 3 | 3000 | 17.50 | 104.23 |
| ds4 | HID ReadFile | vigem | baseline | forward | 3 | 3000 | 5.70 | 44.60 |
| xbox-one-gip | XInput | vdevice | baseline | forward | 3 | 3000 | 101.30 | 64272.09 |
| xbox360 | XInput | vdevice | Combined | modify | 3 | 3000 | 51.10 | 267.25 |
| xbox360 | XInput | vdevice | Gamepad-Controller | modify | 3 | 3000 | 38.10 | 170.39 |
| xbox360 | XInput | vdevice | baseline | forward | 7 | 7000 | 51.70 | 123.96 |
| xbox360 | XInput | vigem | baseline | forward | 6 | 6000 | 53.25 | 616.05 |

DS4 reports record the observed thumb axes, twelve-button/D-pad field, triggers and report size in CSV. GIP uses a native virtual USB profile observed through XInput, with trigger conversion explicitly handled by the producer. Neither is a physical Bluetooth/USB measurement.

Initial filter association may require a guest restart. The fixture uses a stable USB serial so Windows can retain per-instance filter configuration. This is a descriptor-level fixture adaptation, not a driver or license modification. Failed pre-restart attempts remain in the dataset.

CPU figures in per-run JSON are producer/receiver process-lifetime milliseconds, including initialization and warm-up. Peak working set includes process pages and SDKs. Neither is isolated kernel CPU or driver pool usage.

[Per-run controller results](../assets/xinput-results.json) · [Raw data](../assets/raw-results.zip) · [Method](../methodology/measurement.md)
