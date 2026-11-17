---
title: Vdevice vs ViGEmBus — Windows Xbox 360 state visibility benchmark
description: Measured virtual Xbox 360 state visibility through an independent XInput receiver, with raw data and architecture-specific comparison limits.
---
# Vdevice vs ViGEmBus: Xbox 360 state visibility

Both backends create a virtual Xbox 360 controller in the same Windows 11 Hyper-V VM. A separate receiver uses Windows XInput only. The producer changes buttons, sticks and triggers; the receiver validates the complete expected state before acknowledging it. There is one outstanding state, so this measures **closed-loop submission-to-state visibility**, not physical input latency, free-running report loss or maximum throughput.

| Backend | Release | Runs | States observed | Median run P50 (µs) | Median run P99 (µs) |
|---|---|---:|---:|---:|---:|
| vdevice | 1.0.5.0 | 7 | 7000 | 51.70 | 123.96 |
| vigem | 1.22.0 | 6 | 6000 | 53.25 | 616.05 |

## Interpretation

These paths implement the same application-facing controller profile through different stacks. Vdevice emulates a USB function handled by Windows `xusb22`; ViGEmBus exposes its own virtual bus/target. Vdevice uses its published example session, including model translation and a control worker; ViGEm uses its public X360 client API. The measured cost includes those SDK layers and the receiver's XInput polling and scheduling. It is not an isolated comparison of kernel instruction costs.

Fresh producer/receiver processes are used for each run. Warm-up is 100 states. All raw timestamps remain available. Initial runs were performed in driver blocks; additional alternating restored sessions are recorded where available. Shared-host scheduling, small sample size and different device paths prevent a universal faster-driver conclusion. No overall ranking is inferred.

[Raw data](../assets/raw-results.zip) · [Per-run Xbox results](../assets/xinput-results.json) · [Measurement method](../methodology/measurement.md) · [Source audit](../comparisons/index.md)
