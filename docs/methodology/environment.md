---
title: Windows 11 benchmark environment and toolchain
description: Exact host CPU, OS, fixed Hyper-V resources, guest build, security state and compiler used for the published software measurements.
published: 2026-11-17
updated: 2026-11-17
---
# Environment

```json
{
  "host": {
    "host": {
      "free_ram_bytes": 5838880768,
      "ram_bytes": 33952415744,
      "cpu": "Intel(R) Core(TM) Ultra 7 265KF",
      "load_percent": 88,
      "version": "10.0.19045",
      "os": "Microsoft Windows 10 Professionnel",
      "power_plan": "GUID du mode de gestion de l\u2019alimentation\u00a0: 381b4222-f694-41f0-9685-ff5bb260df2e  (Utilisation normale)",
      "logical_processors": 20
    },
    "compiler": {
      "cmake": "cmake version 4.1.2",
      "msvc": "19.32.31342.0",
      "windows_sdk": "10.0.26100.0"
    },
    "vm": {
      "clean_checkpoint": "Clean-Benchmark-Baseline",
      "secure_boot": "On",
      "memory_bytes": 3221225472,
      "disk": "dedicated differencing VHDX",
      "dynamic_memory": false,
      "generation": 2,
      "cpu_count": 2,
      "network": "Hyper-V Default Switch"
    },
    "limitations": [
      "Other host workloads were not suspended",
      "Physical USB passthrough not configured",
      "HVCI not enabled in this VM",
      "VM measurements do not represent physical USB latency"
    ],
    "captured_utc": "2026-11-17T11:08:07.0545987Z"
  },
  "guest": {
    "os": {
      "Caption": "Microsoft Windows 11 Enterprise LTSC Evaluation",
      "Version": "10.0.26100",
      "BuildNumber": "26100"
    },
    "secure_boot": true,
    "hvci": {
      "SecurityServicesRunning": [
        0
      ]
    },
    "powershell": "5.1.26100.1591",
    "wpr_version": "10.0.26100.1591 (WinBuild.160101.0800)",
    "network": true
  }
}
```

Python and report dependencies are pinned in `requirements.txt`. Compilers and build tools run on the host; native workloads, signed drivers and WPR run in the dedicated guest. No second guest WDK installation was needed for these signed binary evaluations.
