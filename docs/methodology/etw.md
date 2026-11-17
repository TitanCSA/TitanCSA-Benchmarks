---
title: WPR instrumented virtual HID trial — scoped DPC evidence
description: A real WPR GeneralProfile trace decoded with xperf, with event-loss checks and explicitly bounded module DPC attribution.
---
# Instrumented HID trial: DPC evidence

A separate trial used WPR GeneralProfile file mode in the dedicated Windows guest. The producer generated 100 warm-up and 1,000 measured vendor-HID reports at a requested 1,000 reports/s. Its purpose is `instrumented`, so it is excluded from primary latency charts.

| Recorded item | Value |
|---|---:|
| Whole trace duration (seconds) | 28.206191 |
| Lost events | 0 |
| Lost buffers | 0 |
| Vdevice module DPC calls | 2221 |
| CPU 0 Vdevice DPC duration (microseconds) | 20476 |
| CPU 1 Vdevice DPC duration (microseconds) | 25757 |

These are module-attributed DPC durations from `xperf -a dpcisr`, across the **whole trace**, including enumeration, warm-up, report generation, waiting and teardown. They are not total driver CPU, time per report, proof of ISR behavior or a competitor ranking. The instrumented trial and uncontrolled shared-host scheduling cannot be merged with the uninstrumented headline latency results.

## Reproduce and inspect

Use `automation/trace-scenario.ps1` only after restoring the owned Vdevice checkpoint. The script starts its own WPR recording and stops it without cancelling someone else's existing trace. `scripts/summarize_etw.py` decodes the local ETL and exports only aggregate measurements. The trace remains local because it contains broad guest system state.

ETL SHA-256: `7946d0ad8c70c1751c2171e53043e54c1e0769bded583173bc0375b69a876bdc`. The [raw archive](../assets/raw-results.zip) includes `reports/etw-validation.json`; the ETL itself is excluded.
