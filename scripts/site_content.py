from pathlib import Path
import json,re
from analyze import ROOT
def write(name,title,description,text):
    p=ROOT/'docs'/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(f'---\ntitle: {title}\ndescription: {description}\npublished: 2026-11-17\nupdated: 2026-11-17\n---\n'+text+'\n',encoding='utf8')
def main():
    data=json.loads((ROOT/'data/processed/results.json').read_text());valid=[r for r in data if r['status']=='measured' and r['profile']=='vendor-hid'];audit=json.loads((ROOT/'reports/repository-audit.json').read_text())
    write('index.md','Windows input driver benchmarks — measured paths, open data','Real Windows 11 Hyper-V benchmarks for virtual HID and Xbox 360 devices, with independent receivers, exact versions, raw timestamps and source audits.',f'''<div class="hero" markdown>
<div class="eyebrow">TitanCSA · Windows driver laboratory</div>

# Measure the path. Keep the evidence.

<p class="lead">Reproducible input measurements, independent Windows receivers, and the raw data behind every chart.</p>

[Explore measured results](vdevice/latency.md){{ .md-button .md-button--primary }}
[Read the methodology](methodology/measurement.md){{ .md-button }}
</div>

<div class="metrics"><div><strong>{len(valid)}</strong><span>validated vendor-HID runs</span></div><div><strong>{sum(r['received'] for r in valid):,}</strong><span>post-warmup vendor-HID reports</span></div><div><strong>2 vCPU</strong><span>Windows 11 · Hyper-V · 3 GiB fixed RAM</span></div></div>

## Start with the question you need answered

| Question | Evidence |
|---|---|
| How long until a virtual HID report reaches an application? | [Vendor HID submission to Windows ReadFile](vdevice/latency.md) |
| How do Vdevice and ViGEmBus expose Xbox 360 states? | [Closed-loop XInput comparison](vdevice/comparisons.md) |
| Does the requested rate match delivered traffic? | [Submission cadence, queues and losses](vdevice/throughput.md) |
| Which driver fits interception, hiding or virtual-device creation? | [Source-backed project audit](comparisons/index.md) |
| Can I reproduce the result? | [Raw data](data.md), [environment](methodology/environment.md), [automation](methodology/reproducibility.md) |

<div class="scope" markdown>
**Read the boundary before the number.** These are virtual-device software-path measurements on one Windows 11 guest. They do not measure physical USB latency, prove compatibility with every controller, or establish that TitanCSA is universally faster. This laboratory is operated by TitanCSA, a developer of the tested products.
</div>

## Results you can inspect

![Virtual HID measurement](assets/hid-latency.svg)

The C++ producer records submission timestamps. A separate executable receives and validates content using Windows HID, Raw Input or XInput. Reports preserve sequence IDs, timing, seeds, configuration, failed runs and provenance. Tables and charts are generated from validated data rather than typed into pages.

## Projects covered by the audit

[Interceptor](interceptor/overview.md), [Interceptor Keyboard & Mouse](interceptor/overview.md), [Interceptor Gamepad & Controller](gamepad/overview.md), [Vdevice](vdevice/overview.md), and [Interception V2](interceptor/comparisons.md). The comparison inventory also covers oblitum/Interception, ViGEmBus, HidHide, vJoy, libvirtualhid and Microsoft samples. Source review and runtime measurements have distinct statuses.
''')
    home=ROOT/'docs/index.md'
    home.write_text(home.read_text(encoding='utf8').replace('## Start with the question you need answered','!!! note "Vdevice teardown fix status"\n    Microsoft-signed Vdevice demo 1.0.6.0 passed repeated controller teardown tests. The signed commercial Release passed setup and SDK readiness checks before activation. The [incident record](methodology/incident-wdf-001.md) lists the exact versions and original crashes.\n\n## Start with the question you need answered'),encoding='utf8')
    lines=['# Source-backed project and competitor audit','',f"Repository metadata checked: {audit['retrieved_utc']}. Source is pinned by commit; release artifacts have independent hashes. README claims are not automatically runtime-verified.",'','| Project | Latest audited release | Commit | Last commit date | Archived | Repository license metadata |','|---|---|---|---|---|---|']
    for r in audit['repositories']:
        if 'error' in r:lines.append(f"| {r['requested']} | unavailable | — | — | — | {r['error']} |");continue
        release=r.get('release') or {};lines.append(f"| [{r['requested']}]({r['url']}) | {release.get('tag_name','none')} | [{r['commit'][:10]}]({r['url']}/commit/{r['commit']}) | {r['commit_date'][:10]} | {r['archived']} | {r['license'] or 'Inspect file-level terms'} |")
    lines+=['','## Compare by purpose','','| Category | Relevant solutions | Boundary |','|---|---|---|','| Keyboard/mouse interception | TitanCSA combined/split, Interception V2, oblitum/Interception | Requires attachment and proof that generated events cross the filter |','| Gamepad interception | TitanCSA combined/controller-only | HID, XUSB, XInputHID and GIP are separate paths; creation is not interception |','| Virtual-device creation | Vdevice, ViGEmBus, libvirtualhid, vJoy, Microsoft VHF/UdeCx samples | Compare only equivalent functional profiles |','| Device hiding | HidHide | Complementary access control, not an interception/rewriting replacement |','','## Inspected source evidence','']
    patterns={'TitanCSA/Vdevice':['Udecx','VD_TRIAL_SECONDS','Send_Input'], 'TitanCSA/Interceptor':['WdfFdoInitSetFilter','IC_PRODUCT_INPUT_MASK','Get_Input_With_Timeout'], 'TitanCSA/Interceptor-Keyboard-Mouse':['WdfFdoInitSetFilter','IC_PRODUCT_CONTROLLER_MASK','Get_Input_With_Timeout'],'TitanCSA/Interceptor-Gamepad-Controller':['WdfFdoInitSetFilter','IC_PRODUCT_INPUT_MASK','Controller_GIP'], 'TitanCSA/Interception-V2':['interception_create_context','WdfFdoInitSetFilter']}
    for repo,terms in patterns.items():
        r=next(x for x in audit['repositories'] if x['requested']==repo);base=ROOT/'.local/sources'/repo.replace('/','--')
        if not base.exists():continue
        lines.append('### '+repo)
        for term in terms:
            match=None
            for p in sorted(base.rglob('*')):
                if p.suffix not in ['.c','.cpp','.h'] or '.git' in p.parts:continue
                for n,line in enumerate(p.read_text(encoding='utf8',errors='replace').splitlines(),1):
                    if term in line:match=(p.relative_to(base).as_posix(),n,line.strip()[:160]);break
                if match:break
            if match:
                path,n,line=match;lines.append(f"- `{term}`: [{path}:{n}]({r['url']}/blob/{r['commit']}/{path}#L{n}). Source presence is verified; build-time product masks determine which families are enabled.")
        lines.append('')
    lines+=['## Runtime status','','Executed paths include Vdevice vendor HID, keyboard/mouse, XUSB, DS4 and Xbox One/GIP; both Interceptor keyboard/mouse editions; combined and controller-only controller transformations; ViGEmBus XUSB/DS4; and Brunner vJoy WinMM axes/buttons. See the per-run result pages for valid repetitions, invalid runs and exact receiver APIs. The original DS4 and GIP filter campaigns recorded the WDF-001 guest crash. The signed demo 1.0.6.0 passed separate teardown tests. Source presence and successful latency rows do not certify stability or other device profiles. Windows libvirtualhid driver-backed profiles require a separate license; no runtime score is assigned without it.','','## Licenses and build observations','','TitanCSA SDK/application files use their published terms; driver evaluation-source restrictions and third-party MIT/MS-PL mappings must be read separately. Repository license metadata alone does not relicense a commercial driver. Signed release downloads are used; driver source was inspected without changing trial behavior.','','The Interceptor public SDK needs Windows IOCTL definitions when built with `WIN32_LEAN_AND_MEAN`; the benchmark target explicitly includes `windows.h` and `winioctl.h`. This integration requirement is recorded rather than changing the measured driver. All seven original Interception SDK examples and the new benchmark tools have their own source provenance.']
    write('comparisons/index.md','Windows input driver comparison — source audit and measured scope','Pinned source, release and license inventory for TitanCSA, Interception, ViGEmBus, HidHide, vJoy and libvirtualhid, separated by actual purpose.','\n'.join(lines))
    host=json.loads((ROOT/'data/environments/host.json').read_text(encoding='utf-8-sig'));guest=json.loads((ROOT/'data/environments/guest.json').read_text(encoding='utf-8-sig'))
    write('methodology/environment.md','Windows 11 benchmark environment and toolchain','Exact host CPU, OS, fixed Hyper-V resources, guest build, security state and compiler used for the published software measurements.','# Environment\n\n```json\n'+json.dumps({'host':host,'guest':guest},indent=2)+'\n```\n\nPython and report dependencies are pinned in `requirements.txt`. Compilers and build tools run on the host; native workloads, signed drivers and WPR run in the dedicated guest. No second guest WDK installation was needed for these signed binary evaluations.')
    write('vdevice/overview.md','Windows virtual USB device performance — Vdevice architecture','Source-reviewed UdeCx virtual USB architecture, verified vendor HID and Xbox 360 profiles, and the boundaries of current Vdevice measurements.','''# Vdevice: virtual USB devices

Vdevice exposes descriptor-driven virtual USB functions through a C++17 SDK and a KMDF/UdeCx driver. The source defines bounded queues and a shared one-hour evaluation allowance; neither was patched for this campaign. HID vendor-defined reports and Xbox 360 state delivery were functionally received by independent Windows applications.

The source includes keyboard, mouse, Xbox 360, DS4 and Xbox One/GIP examples. Their presence is an integration starting point, not runtime qualification for every profile. Read the [audit](../comparisons/index.md), [measured vendor HID result](latency.md) and [Xbox 360 comparison](comparisons.md).

Creation-call time, Windows enumeration, first observed input and deletion-call time are separate milestones. A deletion API returning does not establish that every PnP node has disappeared. Queueing, delegated USB controls and Windows inbox drivers are part of the tested path.
''')
    write('vdevice/throughput.md','Windows virtual HID throughput — requested vs observed cadence','Why requested scheduling rate, SDK acceptance, observed reports and USB polling are distinct metrics in the Vdevice virtual HID campaign.','''# Submission cadence and delivered reports

The campaign requests 125, 1,000 and 10,000 reports per second using a high-resolution waitable timer where supported. It records actual QPC submission intervals, SDK return codes and independently observed content. [Per-run results](../assets/results.json) include actual rate, missing reports and submission cost.

A requested 10 kHz submission schedule is not proof of 10 kHz physical USB polling. The virtual full-speed HID descriptor requests a 1 ms interrupt interval. Windows scheduling, buffers and virtual USB behavior remain part of the path. These finite-rate scenarios do not establish an absolute maximum sustainable throughput.

See the [measured table](latency.md) for all rates and the [raw CSV archive](../assets/raw-results.zip) to reconstruct the observed cadence. Longer saturation and multi-device campaigns must be executed before claiming a maximum throughput or long-term stability bound.
''')
    write('interceptor/overview.md','Windows keyboard and mouse interception benchmark — validation scope','Keyboard and mouse benchmark design, product-specific SDK boundaries, input-filter attachment requirements and available independent Raw Input checks.','''# Keyboard and mouse interception

Interceptor and its Keyboard & Mouse edition use product-specific C++17 APIs with capture batches and explicit forwarding. Interception V2 preserves the original C ABI through its own compatibility backend. These APIs and driver identities are not interchangeable.

The lab's keyboard/mouse scenarios create only authorized Vdevice HID fixtures. An independent Raw Input receiver on the guest desktop records their content and timestamps. Before interpreting a filter result, verify the PnP stack, captured-source identity, capture count and forwarding/modification/blocking outcome. A service being Running is insufficient.

The vendor-HID results on this site do not traverse these filters. They must not be advertised as keyboard/mouse filter overhead. The [measurement guide](../methodology/measurement.md) defines the correlation rules. [Raw runs](../data.md) distinguish completed, invalid and not-executed cases.

## Practical integration

Use a matching driver, SDK and example from one edition. Restore a clean VM before switching overlapping filters. Without a capture owner, input pass-through and emergency recovery are separate functional requirements that need testing. No real host input is captured by this lab.
''')
    write('interceptor/comparisons.md','Interception V2 and oblitum Interception — compatibility vs performance','Separate original Interception ABI compatibility, filter attachment and independent keyboard/mouse delivery measurements before comparing implementations.','''# Interception compatibility is not a latency result

oblitum/Interception supplies the original C API and a keyboard/mouse interception driver. TitanCSA Interception V2 exposes the original SDK ABI through a different implementation. The combined Interceptor product uses its own C++ API. A shared application ABI makes equivalent test applications possible; it does not establish identical filter positions or performance.

Pin both driver versions and the original DLL, restore clean installations, enumerate supported test devices and verify receive/forward behavior before timing. Classic class-filter installations may need a guest restart. If a generated virtual HID does not traverse a driver, that scenario must remain unmeasured for that driver.

[Pinned repositories](../comparisons/index.md) · [Method](../methodology/measurement.md)
''')
    write('gamepad/overview.md','Windows gamepad interception driver benchmark — HID, XUSB and GIP','Why virtual controller creation and physical gamepad report interception require different tests, with protocol-specific measurement boundaries.','''# Gamepad interception: separate the protocols

The combined Interceptor and controller-only edition expose HID, XUSB/XInput, XInputHID and GIP paths under product-specific masks. Source paths and SDK types are inspected in the [audit](../comparisons/index.md). Runtime support must be demonstrated for each descriptor, connection and Windows path.

The [virtual Xbox 360 comparison](../vdevice/comparisons.md) measures device creation/state delivery, not interception of an external gamepad. No HID result is generalized to GIP, Bluetooth or physical USB controllers.

For a valid interception test, submit known virtual states, prove filter attachment and capture, modify a chosen button/stick/trigger, then verify the result with independent XInput or HID. Blocked-state checks must account for XInput polling: a state not observed by an application is not automatically a dropped kernel report. Protocol-specific physical-device and reconnect campaigns remain outside the currently measured dataset.
''')
    write('comparisons/vigem-alternatives.md','ViGEmBus alternatives for Windows 11 — choose by device model','Compare Vdevice, libvirtualhid, vJoy and Windows VHF/UdeCx reference architectures by required profile, licensing and measured evidence rather than a global ranking.','''# ViGEmBus alternatives: start with the device model

ViGEmBus targets virtual Xbox 360 and DS4-style devices. Its archived maintenance state is recorded in the repository audit. A replacement should be chosen by supported Windows builds, controller profile, redistribution terms, API migration and verified application behavior.

| Need | Candidate | What to verify |
|---|---|---|
| Descriptor-driven virtual USB | Vdevice | USB controls, endpoints, inbox-driver binding, profile behavior |
| Cross-platform virtual input API | libvirtualhid | Backend-specific profile support and Windows licensing |
| Virtual joystick | vJoy | DirectInput/joystick semantics; do not equate it with XInput |
| Windows HID source | Microsoft VHF sample architecture | Driver integration, signing and report semantics |
| Xbox 360 application-facing profile | Vdevice or ViGEmBus | [Executed XInput comparison](../vdevice/comparisons.md) |

HidHide controls visibility/access to devices; it does not replace the virtual controller engine. No best-driver claim is supported merely by feature count. Exact releases, licenses and source links are in the [audit](index.md).
''')
    write('comparisons/kmdf-umdf.md','KMDF vs UMDF virtual HID performance — what a fair test requires','Compare kernel and user-mode virtual HID architectures only with matched profiles, independent receivers and measured Windows paths.','''# KMDF vs UMDF: architecture is not a benchmark

KMDF and UMDF place different components in different execution environments. A framework label alone cannot predict latency: transport, batching, scheduling, SDK logic and receiver API matter.

Vdevice uses KMDF/UdeCx USB emulation. Microsoft's documented VHF HID source architecture uses a kernel-mode source driver and an inbox HID tree. The current libvirtualhid README describes Windows driver-backed UMDF paths; its exact implementation and required license must be evaluated before any numerical comparison. These descriptions should not be collapsed into one interchangeable HID stack.

An honest comparison needs the same functional HID profile, report sizes, source schedule, independent receiver, Windows build, security policy and measured endpoint. No KMDF-versus-UMDF performance ranking has been executed in this campaign. The current [results](../vdevice/latency.md) cover one UdeCx vendor-HID path.

References: [Microsoft VHF architecture](https://learn.microsoft.com/en-us/windows-hardware/drivers/hid/virtual-hid-framework--vhf-), [upstream libvirtualhid](https://github.com/LizardByte/libvirtualhid).
''')
    write('compatibility/index.md','Windows input driver compatibility — observed vs documented','Compatibility matrix distinguishing independently received virtual profiles, source-reviewed examples and unexecuted physical controller tests.','''# Compatibility evidence

| Project / profile | Source/documentation | This lab's runtime status |
|---|---|---|
| Vdevice vendor-defined HID | Descriptor-driven UdeCx | Independently received through Windows HID |
| Vdevice virtual Xbox 360 | Published Xbox360 example | Independently received through XInput |
| ViGEmBus virtual Xbox 360 | Public X360 client API | Independently received through XInput |
| Vdevice keyboard/mouse | Published HID examples and lab descriptors | Inspect raw-input result records; no universal hardware claim |
| Vdevice DS4 / Xbox One GIP | Published examples | Independent HID/XInput delivery measured; see protocol-specific results |
| Interceptor controller HID/XUSB/GIP | Source and SDK paths | XUSB modification verified; the original DS4 campaign includes WDF-001. Teardown fix validation applies to signed demo 1.0.6.0 |
| HidHide | Device access/visibility control | Audited; not scored as interception |
| libvirtualhid Windows profiles | Backend-specific upstream documentation | Not installed; license required |
| vJoy (BrunnerInnovation 2.2.2.0) | Virtual joystick model | Independent WinMM X/Y/button comparison executed; not an XInput score |

No entry establishes physical controller compatibility or all-Windows-build support. See [environment](../methodology/environment.md) and [limitations](../methodology/limitations.md).
''')
    p=ROOT/'docs/data.md';p.write_text('''---
title: Windows input benchmark dataset — raw reports and provenance
description: Download measured QPC timestamps, sequence validation, environment records, failed runs and derived statistics for the TitanCSA benchmark laboratory.
dataset: true
published: 2026-11-17
updated: 2026-11-17
---
# Download the evidence

[Raw CSV/JSON and environment archive](assets/raw-results.zip) · [HID per-run results](assets/results.json) · [HID aggregate intervals](assets/aggregates.json) · [Controller per-run results](assets/xinput-results.json) · [Joystick results](assets/joystick-results.json) · [Stability records](assets/stability-results.json) · [Resource diagnostics](methodology/diagnostics.md)

Data are CC BY 4.0; benchmark code is MIT. Upstream software and repository metadata retain their own terms. Cite the run ID and exact repository revision. Raw runs are append-only: a failed run is retained, and a retry receives a new identifier.

`submission.csv` records sequence, entry QPC, return QPC and SDK error. `reception.csv` records source sequence, submission QPC, receive QPC and content validity. XInput uses corresponding `xinput-*.csv` files with one acknowledged state outstanding. QPC frequency, warm-up, seed, rate, profile and origin are in each run JSON. PnP text snapshots are retained when collected. Derived JSON records validation status and file hashes.

The archive contains real measurements and invalid-run diagnostics. It contains no simulated ranking, private credentials, activation keys or commercial package.
''',encoding='utf8')
    print('Generated substantive site pages and pinned source evidence')
if __name__=='__main__':main()
