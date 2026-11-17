# Executed campaign report

Updated: 2026-11-17T13:23:05.876653+00:00

This is a partial, genuinely executed campaign, not completion of the full requested hardware/protocol/endurance matrix.

- Valid measured series: **89**.
- Invalid annotated series retained: **31**.
- Native error records retained: **22**.
- Real driver installation and tests ran only inside the owned Hyper-V VM.
- PnP snapshots and independent content checks gate filtered results.
- No simulated ranking, purchased review, real user-input capture, private key or commercial package is published.

## Remaining work and exact reasons

| Item | Status / reason |
|---|---|
| physical_hardware | No dedicated physical agent, USB assignment or external timing apparatus |
| oblitum_Interception | User confirmed no commercial-use license; excluded from commercial performance measurements |
| libvirtualhid_Windows | User confirmed no appropriate Windows license; no driver-backed performance score |
| Microsoft_VHF_UdeCx_samples | Reference architecture/source reviewed; existing Vdevice and ViGEm generators covered selected paths, no new sample driver qualification claimed |
| long_duration_soak | Multi-hour soak and fault injection not executed; any shorter monitored run is reported separately |
| full_protocol_matrix | No exhaustive DualSense/Bluetooth/physical/XInputHID matrix; see actual DS4, XUSB and GIP per-run results |
| driver_stability | Open WDF-001: Vdevice queue purge at STATUS_DELETE_PENDING caused a guest bugcheck during the controller campaign; initiating lifetime race not resolved |
| self_hosted_CI | Workflow prepared; no dedicated runner registered or dispatched |
| search_console | No verification token or account connection available |

## Inspect evidence

See `data/raw/`, `data/processed/`, `reports/artifacts.json`, `reports/repository-audit.json`, `reports/clean-baseline-v2.txt`, per-run `pnp-stack.txt` and the documentation. The initial image included historical Filter packages; the corrected clean baseline removes them. Pilot results retain their original provenance and limitations.

## Delivery checklist

1. **Executed actions:** audited pinned upstream repositories, provisioned an owned differencing-disk Hyper-V VM, compiled native C++17 tools, installed signed drivers, generated and independently received virtual reports, collected raw data and generated this site.
2. **Successful installations:** Microsoft-signed Vdevice 1.0.5.0, Interceptor 1.4.22.0, Keyboard-Mouse 1.0.5.0, Gamepad-Controller 1.0.13.0, ViGEmBus 1.22.0 and Brunner vJoy 2.2.2.0. See installation reports and per-run PnP stacks. Secure Boot remained on; guest HVCI was off.
3. **Failed setup/qualification:** inherited generic Filter packages initially contaminated the mouse fixture; they were removed in the owned guest and a corrected baseline created. Controller association required restarts. Extra protocol reports prevent one-to-one qualification of some GIP/ViGEm-filter series. These failures remain in the data.
4. **Executed tests:** vendor HID delivery, Raw Input keyboard/mouse forwarding, remapping and controlled blocking, XInput XUSB/GIP delivery, DS4 HID byte validation, selected controller modifications, WinMM joystick axes/buttons, upstream five-profile functional validation a five-minute monitored HID trial and a separate WPR GeneralProfile recording decoded for module-attributed DPC activity.
5. **Results:** quantitative tables are generated in `docs/vdevice/latency.md`, `docs/interceptor/results.md`, `docs/gamepad/results.md` and `docs/vdevice/joystick.md`. The counts above come from strict per-run validation; short monitoring is not multi-hour qualification.
6. **Competitors measured:** ViGEmBus XUSB/DS4 and Brunner vJoy WinMM. HidHide is a complementary hiding tool, not a rewriting-latency competitor. Other sources are audited without an invented runtime score.
7. **Demonstrated strengths:** selected Vdevice profiles and TitanCSA filter forwarding/modification/blocking are independently observed. These are functional capabilities, not evidence of a universal speed or stability advantage. The close XUSB medians do not establish a robust winner under uncontrolled host load.
8. **Weaknesses:** open WDF-001 guest crashes; vJoy and ViGEm DS4 have lower observed median visibility times than the corresponding Vdevice fixtures; filtered mouse runs have substantial end-to-end delay. SDK, polling, queuing and scheduling are included, so these figures do not isolate kernel execution cost.
9. **Unexecuted tests:** physical USB/Bluetooth, exhaustive protocols, multi-hour endurance, full fault injection, HLK/HVCI qualification and total driver CPU/kernel-hotspot attribution remain incomplete. One scoped whole-trace DPC attribution is published separately; it is not a complete CPU profile.
10. **Exact blockers:** see the table above. No commercial licenses were bypassed, no physical devices assigned and no dedicated privileged CI runner registered.
11. **Files created:** `benchmarks/` native tools, `automation/` owned-VM orchestration, `scripts/` validators/reporting, `tests/` numerical fixtures, `data/` raw/processed/environment/stability records, `reports/` audit/incidents, `docs/` site, `overrides/`, `mkdocs.yml` and separate GitHub workflows. Private dumps, ETLs, credentials and downloaded commercial installers are excluded.
12. **Commits:** the repository history is authoritative. A publication receipt records pushed source revisions and workflow URLs when available; local construction alone is not deployment evidence.
13. **Published pages:** target `https://titancsa.github.io/TitanCSA-Benchmarks/`. Actual deployment and HTTP verification are recorded separately in `reports/publication.json`; this generated report does not infer success from configuration.
14. **Priorities:** isolate and fix queue-lifetime teardown with normal signing/qualification; correlate extra GIP/DS4 protocol traffic; reproduce on dedicated physical hardware and controlled host load; perform multi-hour cancellation/removal/endurance tests; extend ETW attribution to controlled CPU/DPC/ISR hotspot comparisons and add version history.
