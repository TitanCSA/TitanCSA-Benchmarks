---
title: Windows kernel input latency measurement methodology
description: How the TitanCSA laboratory correlates QPC timestamps, validates event contents and distinguishes software delivery from physical USB latency.
---
# What the benchmark measures

**Submission-to-observation** starts immediately before the producer's public SDK call and ends when a separate receiver observes the matching content through a Windows API. Both processes run in the same guest and use QueryPerformanceCounter. QPC frequency is checked before correlating timestamps. No host/guest timestamp subtraction is used.

For vendor HID, the report contains a sequence, submission timestamp, seed-derived payload and checksum. A separate executable links only Windows HID APIs. For Xbox 360, a separate executable links only XInput. One state is outstanding at a time: the producer waits for a receiver acknowledgement before submitting another. This is a **closed-loop state visibility** benchmark, not a loss-rate benchmark or independent maximum-throughput experiment.

Raw Input keyboard/mouse scenarios use a receiver on the guest's interactive desktop. It ignores every device except the laboratory VID/PID. Mouse motion carries a bounded sequence in X/Y. Keyboard sequences are validated in order; missing or malformed sequences invalidate correlation rather than silently shifting timestamps.

## Timing and statistics

Each run warms up for 100 reports. Individual reports and all outliers remain in CSV. Per-run statistics include mean, sample standard deviation, min/max, P50/P90/P95/P99, observed submission rate, submission errors and unmatched/duplicate/reordered reports. Quantiles use NumPy's linear interpolation. Headline summaries use the median of per-run quantiles. They are not pooled percentiles.

The seeded bootstrap resamples run medians 10,000 times for a descriptive 95% interval. Repeated runs share a host and guest; they do not establish population-level hardware confidence. Small numbers of repetitions and changing background load can dominate differences.

## Fair comparisons

Restore the same clean checkpoint or a separately prepared driver-specific checkpoint. Keep CPU, fixed RAM, binary hashes, Windows build, profile and receiver unchanged. Alternate driver sessions when possible. Never compare a HID vendor report against an Xbox controller and call the difference a driver advantage. Do not rank device hiding, interception and device creation as if they served the same purpose.

API call duration includes the SDK and kernel boundary. Observation time additionally includes Windows stacks, queues, polling and scheduling. ETW can help diagnose those components; no kernel-only cost is inferred from the end-to-end number.

Reference: [Microsoft QPC guidance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps), [XInputGetState](https://learn.microsoft.com/en-us/windows/win32/api/xinput/nf-xinput-xinputgetstate).
