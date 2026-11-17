---
title: Windows keyboard and mouse filter performance — verified Raw Input paths
description: Measured source-to-Raw Input delivery with capture, forwarding, remapping and controlled blocking, backed by per-run PnP evidence.
---
# Keyboard and mouse: verified paths

These are virtual HID fixtures in Windows 11 Hyper-V. The receiver uses Raw Input on the guest desktop and accepts only laboratory VID/PIDs. Mouse sequences use one outstanding report to avoid motion coalescing; an event acknowledgement occurs after the receive timestamp. The requested rate is a ceiling, not physical USB polling.

| Profile | Filter | Operation | Runs | Received post-warmup | Median run P50 (µs) | Median run P99 (µs) |
|---|---|---|---:|---:|---:|---:|
| keyboard | Combined | forward | 1 | 1000 | 433.90 | 1778.74 |
| keyboard | Keyboard-Mouse | forward | 1 | 1000 | 487.90 | 1392.52 |
| keyboard | baseline | forward | 4 | 4000 | 327.00 | 1174.78 |
| mouse | Combined | modify | 3 | 3000 | 25746.80 | 65335.46 |
| mouse | Keyboard-Mouse | block | 1 | 500 | 436.10 | 1020.81 |
| mouse | Keyboard-Mouse | forward | 1 | 1000 | 25580.15 | 64744.35 |
| mouse | Keyboard-Mouse | modify | 3 | 3000 | 25789.75 | 64607.92 |
| mouse | baseline | forward | 3 | 3000 | 435.90 | 64627.38 |

## Qualification rules

A filtered series is accepted only if the adapter captured every generated test event, the per-run PnP snapshot shows the target filter, and independent reception validates content. Modification negates mouse X while preserving the sequence encoded in its magnitude. Blocking removes odd X values; the receiver must see only the expected even values. Intentional blocks are not counted as missing reports. Keyboard correlation requires a complete validated sequence.

An inherited historical `Filter` driver initially owned the mouse mapper; those attempted filter runs did not demonstrate capture and are invalid. It was removed only from the owned guest, the VM restarted, and a corrected clean baseline was made. Early free-running mouse trials showed Windows motion coalescing and remain invalid for one-to-one latency correlation. A baseline repetition overlapped installer startup and was explicitly invalidated. All records remain in the raw archive.

Latency includes the Vdevice producer, Windows stack, filter/SDK when present and Raw Input scheduling. It does not isolate kernel-only overhead. Do not subtract unrelated run medians and call the difference an exact driver cost. Source commits, executable hashes where captured, CPU-load snapshots and raw results remain available.

[Per-run statistics](../assets/results.json) · [Raw archive](../assets/raw-results.zip) · [Methodology](../methodology/measurement.md)
