---
title: Reproduce TitanCSA input driver benchmarks
description: Build the pinned C++ producer and independent receivers, provision a dedicated Hyper-V lab and regenerate statistics from immutable raw runs.
---
# Reproduce a campaign

Use Windows with Hyper-V administration, Visual Studio C++17 tools, Windows SDK, Git, CMake and Python. Building user-mode benchmarks does not require changing the drivers or installing the WDK in the guest.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
python scripts\prepare-sources.py
python scripts\fetch_artifacts.py
cmake -S . -B build -A x64
cmake --build build --config Release
```

Inspect `reports/repository-audit.json` and `reports/artifacts.json`: they pin source commits and official release downloads. The SDK and driver licenses remain separate from the MIT benchmark code. Create a new dedicated VM with `automation/provision-vm.ps1`, supplying an already stopped lab parent VM/disk and a local encrypted PowerShell credential file. Do not use a personal VM or install input filters on your workstation.

```powershell
. .\automation\Lab.ps1
$lab = Get-BenchmarkLab
Checkpoint-VM -VM (Get-VM -Id $lab.vm_id) -SnapshotName Clean-Benchmark-Baseline
.\automation\install-titancsa.ps1
.\automation\run-virtual-device-tests.ps1 -Repetitions 5 -Samples 1000
.\automation\run-gamepad-tests.ps1 -Backend vdevice -Repetitions 3
.\automation\reset-vm.ps1
.\automation\install-competitors.ps1
.\automation\run-gamepad-tests.ps1 -Backend vigem -Repetitions 3
.venv\Scripts\python scripts\report.py
.venv\Scripts\python -m mkdocs build --strict
```

Keep the one-hour demo allowance intact. Do not edit trial constants, system clocks, signatures or activation code. Campaigns must fit within the permitted evaluation session. Retain failures, crash records and raw data; start new run IDs rather than overwriting a series.

The first pilot lacked an orchestration completion record and was invalidated. A subsequent file-handoff race produced an empty JSON read; the handoff was changed to atomic rename. Those failed records remain in the raw dataset.
