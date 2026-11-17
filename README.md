# TitanCSA Benchmarks

Measured Windows input paths, independent receivers, and the raw data behind every chart.

**[Read the benchmark site](https://titancsa.github.io/TitanCSA-Benchmarks/)** · [Methodology](docs/methodology/measurement.md) · [Reproduce](docs/methodology/reproducibility.md) · [Raw data](data/raw/) · [Source audit](reports/repository-audit.json)

This publisher-operated lab uses a dedicated Windows 11 Hyper-V VM. Results describe the tested virtual-device software paths. They are not physical USB latency, universal hardware compatibility, independent certification or proof that one vendor always wins.

**Open stability finding:** a controller campaign produced a guest WDF bugcheck at Vdevice queue purge. The WDF log reports `STATUS_DELETE_PENDING`. See the [incident](docs/methodology/incident-wdf-001.md); successful timings do not establish teardown stability.

| Component | Implementation |
|---|---|
| Producer | C++17, JSON scenarios, bounded deterministic sequences and QPC timestamps |
| Independent receivers | Windows HID `ReadFile`, Raw Input on the guest desktop, and XInput in a separate executable |
| Measured profiles | Vendor-defined HID, keyboard/mouse, XUSB, DS4, Xbox One/GIP and generic joystick; filters require per-run qualification |
| Competitor adapters | ViGEmClient/Xbox 360 and DS4; Brunner vJoy/WinMM axes and buttons; separate restored installations |
| Data pipeline | CSV validation, quantiles, descriptive bootstrap intervals, charts, raw archive and file hashes |
| Isolation | Owned VM ID checks, fixed 2 vCPU/3 GiB, Secure Boot, dedicated VHDX and checkpoints |
| Publication | MkDocs Material, public GitHub Pages, canonical URLs, sitemap, Dataset metadata and raw downloads |

## Build and measure

Run `python scripts/prepare-sources.py` to fetch the audited SDK commits, then `cmake -S . -B build -A x64` and `cmake --build build --config Release`. The C++ tools require Windows/MSVC. Python report tools run on Windows or Linux.

The native tools refuse to generate or receive test inputs without the dedicated guest marker. **Never put that marker on your workstation or install the benchmark drivers on the host.** Provision only a disposable lab VM. See [reproduction](docs/methodology/reproducibility.md) for setup, installation, run and reset commands.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python scripts\report.py
.venv\Scripts\python scripts\xinput_report.py
.venv\Scripts\python -m mkdocs build --strict
.venv\Scripts\python scripts\validate_site.py
```

CI compiles native tools, parses PowerShell, validates numerical fixtures, regenerates reports and checks the built site's local links. Privileged measurements are separate, manual-only and restricted to the main branch on an explicitly labelled dedicated self-hosted runner. This project does not register a workstation as a runner or run privileged code from pull requests.

## Evidence and incomplete scope

Every completed run retains its raw records. Invalid runs and failed setup attempts remain visible. Repeats get new IDs; data are not silently replaced. Pilots that predate full executable-hash capture remain labelled by their available provenance.

Physical USB/Bluetooth timing, DualSense, exhaustive protocol qualification, multi-hour soak tests, HLK qualification, kernel CPU/DPC attribution and a scored KMDF-versus-UMDF comparison are not implied by the measurements. A five-minute monitored vendor-HID run is reported separately. DS4 and GIP controller/filter campaigns reproduced an open WDF queue-purge bugcheck; completed rows do not close that finding. Driver-backed Windows libvirtualhid profiles require an upstream license; none was bypassed. Read the exact [limitations](docs/methodology/limitations.md).

Benchmark code: MIT. Numerical datasets: [CC BY 4.0](data/LICENSE). Upstream SDKs, samples and drivers retain their own licenses. No commercial binaries, activation keys, passwords or private signing material are published here.
