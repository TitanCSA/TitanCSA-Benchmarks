"""Generate an explicit 18-point audit with source/documented/measured boundaries."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'reports/repository-audit.json').read_text())
names=['Interceptor','Interceptor-Keyboard-Mouse','Interceptor-Gamepad-Controller','Vdevice']
lines=['---','title: TitanCSA drivers — eighteen-point architecture and evidence audit','description: Per-project source, SDK, licensing, installation, runtime evidence and performance limitations for the four main TitanCSA driver products.','---','# Main projects: architecture and evidence audit','','**Source** means inspected code at the pinned revision. **Documented** means an upstream claim. **Measured** means selected paths actually executed in the owned guest; it never certifies every supported device. No driver behavior was changed.','']
records=[]
for name in names:
    repo='TitanCSA/'+name;r=next(x for x in audit['repositories'] if x['requested']==repo);folder=root/'.local/sources'/repo.replace('/','--')
    assert folder.exists()
    isv=name=='Vdevice';controller=name in ['Interceptor','Interceptor-Gamepad-Controller'];km=name in ['Interceptor','Interceptor-Keyboard-Mouse']
    url=r['url']+'/tree/'+r['commit']
    def link(path):return f'[{path}]({url}/{path})'
    paths=[str(p.relative_to(folder)).replace('\\','/') for p in folder.rglob('*') if p.is_file() and '.git/' not in str(p.relative_to(folder)).replace('\\','/')]
    tests=[p for p in paths if ('test' in p.lower() and p.endswith(('.cpp','.ps1','.cs')))]
    details={
      '01 Architecture':('Source: KMDF/UdeCx USB-device emulation with user-mode descriptor/report SDK.' if isv else 'Source: KMDF input filter, control interface and product-specific input/controller masks.')+' '+link('driver'),
      '02 Ring 0 / Ring 3':'Source: signed SYS handles kernel/PnP/I/O work; C++ SDK, examples and installer execute in user mode. SDK calls do not grant arbitrary kernel execution.',
      '03 Driver type':('Source: UdeCx device-emulation driver, not an input-rewriting filter.' if isv else 'Source: WdfFdoInitSetFilter paths; input/device family depends on product build masks.'),
      '04 API / SDK':('Source: Create_Device, Delete_Device and Send_Input; raw USB/HID configuration.' if isv else 'Source: Init_AllDevices, Get_Input_With_Timeout and Send_Input; product-specific event families.')+' '+link(name if isv else 'Interceptor'),
      '05 Languages':'Source inventory: C kernel implementation, C++ SDK/examples, PowerShell build/install orchestration and C# installer/UI components. Registry wrappers are not separate kernel implementations.',
      '06 Compatible devices':('Documented/examples: USB HID keyboard, mouse, DS4, X360 and Xbox One/GIP; arbitrary descriptor support remains subject to Windows stacks.' if isv else 'Documented product families: '+(', '.join(x for x,on in [('keyboard/mouse',km),('HID/XUSB/XInputHID/GIP controllers',controller)] if on))+'. Selected virtual fixtures are measured; physical devices remain unqualified.'),
      '07 Verified functionality':('Measured: vendor HID sequences/checksums, independent keyboard/mouse reception, XUSB/DS4/GIP state delivery, generic joystick and upstream five-profile live test.' if isv else ('Measured: keyboard forwarding, mouse forwarding/modification/controlled block.' if name=='Interceptor-Keyboard-Mouse' else 'Measured: '+('keyboard forwarding, mouse modification and ' if km else '')+'XUSB modification'+(' and DS4 modification.' if name=='Interceptor-Gamepad-Controller' else '.'))),
      '08 Mechanism':('Source: virtual USB endpoints and report queuing consumed by Windows class drivers; receiver independently uses HID/Raw Input/XInput/WinMM.' if isv else 'Source: capture through family-specific filter paths, user-mode decision and forwarding. Measured modification must be independently visible; PnP attachment is required.'),
      '09 Technical limitations':'These virtual fixtures cover selected transport paths. GIP/ViGEm-filter extra protocol reports lack one-to-one capture correlation. See the [WDF-001 incident](../methodology/incident-wdf-001.md) for the signed demo teardown and commercial pre-activation checks.',
      '10 Windows compatibility':'Documented: Windows 10/11 x64 (Interceptor combined specifies 1709+). Measured: Windows 11 build 26100 Hyper-V only, Secure Boot on and HVCI off. No HLK/HVCI qualification claimed.',
      '11 Signature':'Measured installation: downloaded release SYS Authenticode verified as Valid, Microsoft Windows Hardware Compatibility Publisher. Source/release identity and hashes are separate evidence; source availability does not certify a rebuilt SYS.',
      '12 License':'Inspected: user-mode source MIT; driver/demo/evaluation-source terms and third-party licenses are separate. One-hour demo behavior was retained. '+link('LICENSE')+'; '+link('driver/README.md'),
      '13 Benchmark possibilities':('Executed: vendor HID, virtual controllers and matched joystick subset. Missing: physical latency, exhaustive endpoint/control coverage and hardware bandwidth.' if isv else 'Executed: generated virtual fixtures crossing selected filters, independent observed content and capture/PnP gating. Missing: exhaustive physical controllers, Bluetooth and every protocol feature.'),
      '14 Installation':'Executed signed release GUI/CLI installer in owned VM, PnP/service/signature checks, device creation and independent behavior checks. Controller association sometimes needs a guest restart. '+link('docs/INSTALLATION.md'),
      '15 Existing examples':link('Examples')+'; consumed as source fixtures, not assumed to prove support. Vdevice ExampleRuntime uses a stable USB serial for repeatable per-instance filter association.',
      '16 Repository activity':f"Metadata: pinned commit {r['commit']}; last commit {r['commit_date']}; archived={r['archived']}; latest audited release {r['release']['tag_name']}. README-only updates after the audit do not change the measured binary.",
      '17 Existing tests':'Source inventory: '+(', '.join('`'+p+'`' for p in tests[:8]) if tests else 'examples/build checks; no separate test-suite execution inferred')+'. Only actual lab results and the recorded upstream Vdevice live test are asserted as executed.',
      '18 Performance risks':'Observed: scheduler/SDK/queue overhead, large filtered mouse end-to-end delays, and shared-host tails. Vdevice controller teardown reproduced WDF queue-purge STATUS_DELETE_PENDING. Profile-specific ViGEm/vJoy median advantages remain visible; no universal TitanCSA speed/stability claim.'
    }
    records.append({'repository':repo,'commit':r['commit'],'points':details})
    lines+=['## '+name,'','| Audit point | Evidence and boundary |','|---|---|']+[f'| {k} | {v} |' for k,v in details.items()]+['']
lines+=['[Numerical results](../gamepad/results.md) · [Source and competitor inventory](index.md) · [WDF-001 incident and fix status](../methodology/incident-wdf-001.md)']
(root/'reports/main-project-audit.json').write_text(json.dumps(records,indent=2)+'\n')
(root/'docs/comparisons/main-projects.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('18-point source/documented/measured audit generated for',len(records),'projects')
