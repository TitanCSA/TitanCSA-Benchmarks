from pathlib import Path
import json
import numpy as np
from analyze import ROOT,rows
def main():
    results=[]
    for p in sorted((ROOT/'data/raw').rglob('xinput-run.json')):
        try:
            cfg=json.loads(p.read_text())
            for key in ['run_id','backend','version','utc']:assert key in cfg
        except (ValueError,AssertionError) as e:
            results.append({'run_id':p.parent.name,'status':'invalid','source':p.parent.relative_to(ROOT).as_posix(),'reason':'Missing or malformed run metadata, including interrupted crash writes','backend':'unknown','profile':'unknown','filter':'unknown','operation':'unknown','version':'unknown','utc':'unknown'});continue
        r={'run_id':cfg['run_id'],'backend':cfg['backend'],'version':cfg['version'],'utc':cfg['utc'],'status':'invalid','source':p.parent.relative_to(ROOT).as_posix(),'filter':cfg.get('filter','baseline'),'operation':cfg.get('operation','forward'),'profile':cfg.get('profile','xbox360'),'receiver_api':'HID ReadFile' if cfg.get('profile')=='ds4' else 'XInput','executable_hashes_recorded':bool(cfg.get('build_identity'))}
        try:
            assert json.loads((p.parent/'xinput-done.json').read_text())['status']=='completed','No completion record'
            sent=rows(p.parent/'xinput-submission.csv');rx=rows(p.parent/'xinput-reception.csv');count=cfg['samples'];warm=cfg['warmup'];freq=cfg['qpc_frequency']
            assert len(sent)==len(rx)==count+warm,'Closed-loop sequence incomplete'
            assert [x['sequence'] for x in sent]==[x['sequence'] for x in rx]==list(range(1,count+warm+1)),'Sequence reordered or duplicated'
            assert all(a['submit_qpc']==b['submit_qpc'] and b['receive_qpc']>=a['submit_qpc'] for a,b in zip(sent,rx)),'Timestamp mismatch'
            if r['profile']=='ds4':
                for row in rx:
                    n=row['sequence'];buttons=((1<<(n%12))<<4)|(n%8)
                    if r['operation']=='modify':buttons^=0xf0
                    assert (row['lx'],row['ly'],row['rx'],row['ry'],row['buttons'],row['lt'],row['rt'],row['report_bytes'])==(n%256,255-n%256,(3*n)%256,255-(3*n)%256,buttons,n%256,255-n%256,64),'DS4 observed bytes mismatch'
            if r['filter']!='baseline':
                adapter=json.loads((p.parent/'adapter-done.json').read_text())
                assert adapter['captured']==count+warm,'Capture count differs from generated-state count; background/protocol reports not individually correlated'
                if r['operation']=='modify':assert adapter['modified']==count+warm,'Controller modification not demonstrated'
                stack=(p.parent/'pnp-stack.txt').read_text(encoding='utf-8-sig')
                assert ('InterceptorGamepadController' if r['filter']=='Gamepad-Controller' else 'Interceptor') in stack,'Controller filter attachment missing'
            lat=np.array([(b['receive_qpc']-b['submit_qpc'])*1e6/freq for b in rx[warm:]])
            r.update(status='measured',samples=count,p50_us=float(np.percentile(lat,50)),p99_us=float(np.percentile(lat,99)),min_us=float(min(lat)),max_us=float(max(lat)),mean_us=float(np.mean(lat)),submission_p50_us=float(np.median([(x['return_qpc']-x['submit_qpc'])*1e6/freq for x in sent[warm:]])),stack_captured=(p.parent/'pnp-stack.txt').exists())
            for label,filename in [('producer','xinput-done.json'),('receiver','xinput-receiver.json')]:
                counters=json.loads((p.parent/filename).read_text()).get('resources',{})
                r[label+'_cpu_lifetime_ms']=(counters.get('user_100ns',0)+counters.get('kernel_100ns',0))/10000
                r[label+'_peak_working_set_bytes']=counters.get('peak_working_set_bytes')
        except (AssertionError,FileNotFoundError,KeyError,ValueError) as e:r['reason']=str(e)
        results.append(r)
    (ROOT/'data/processed/xinput-results.json').write_text(json.dumps(results,indent=2)+'\n')
    valid=[r for r in results if r['status']=='measured'];lines=['| Backend | Release | Runs | States observed | Median run P50 (µs) | Median run P99 (µs) |','|---|---|---:|---:|---:|---:|']
    for backend in ['vdevice','vigem']:
        g=[r for r in valid if r['backend']==backend and r['filter']=='baseline' and r['profile']=='xbox360']
        if g:lines.append(f"| {backend} | {g[0]['version']} | {len(g)} | {sum(x['samples'] for x in g)} | {np.median([x['p50_us'] for x in g]):.2f} | {np.median([x['p99_us'] for x in g]):.2f} |")
    text='''---
title: Vdevice vs ViGEmBus — Windows Xbox 360 state visibility benchmark
description: Measured virtual Xbox 360 state visibility through an independent XInput receiver, with raw data and architecture-specific comparison limits.
---
# Vdevice vs ViGEmBus: Xbox 360 state visibility

Both backends create a virtual Xbox 360 controller in the same Windows 11 Hyper-V VM. A separate receiver uses Windows XInput only. The producer changes buttons, sticks and triggers; the receiver validates the complete expected state before acknowledging it. There is one outstanding state, so this measures **closed-loop submission-to-state visibility**, not physical input latency, free-running report loss or maximum throughput.

'''+ '\n'.join(lines)+'''

## Interpretation

These paths implement the same application-facing controller profile through different stacks. Vdevice emulates a USB function handled by Windows `xusb22`; ViGEmBus exposes its own virtual bus/target. Vdevice uses its published example session, including model translation and a control worker; ViGEm uses its public X360 client API. The measured cost includes those SDK layers and the receiver's XInput polling and scheduling. It is not an isolated comparison of kernel instruction costs.

Fresh producer/receiver processes are used for each run. Warm-up is 100 states. All raw timestamps remain available. Initial runs were performed in driver blocks; additional alternating restored sessions are recorded where available. Shared-host scheduling, small sample size and different device paths prevent a universal faster-driver conclusion. No overall ranking is inferred.

[Raw data](../assets/raw-results.zip) · [Per-run Xbox results](../assets/xinput-results.json) · [Measurement method](../methodology/measurement.md) · [Source audit](../comparisons/index.md)
'''
    (ROOT/'docs/vdevice/comparisons.md').write_text(text,encoding='utf8');(ROOT/'docs/assets/xinput-results.json').write_text(json.dumps(results,indent=2)+'\n')
    lines=['---','title: Gamepad report interception and delivery — protocol-specific results','description: Independently verified virtual Xbox 360, DS4 and GIP state delivery, including captured and modified states where the tested filter path is proven.','---','# Gamepad results by protocol','','These are virtual source devices. HID ReadFile and XInput are different observation APIs; their numbers must not be pooled into a global ranking. Every filtered row additionally requires PnP attachment, the complete generated capture count and independently observed modified content.','','| Profile | Receiver | Backend | Filter | Operation | Runs | States | Median run P50 (µs) | Median run P99 (µs) |','|---|---|---|---|---|---:|---:|---:|---:|']
    for key in sorted(set((x['profile'],x['backend'],x['filter'],x['operation']) for x in valid)):
        group=[x for x in valid if (x['profile'],x['backend'],x['filter'],x['operation'])==key]
        lines.append(f"| {key[0]} | {group[0]['receiver_api']} | {key[1]} | {key[2]} | {key[3]} | {len(group)} | {sum(x['samples'] for x in group)} | {np.median([x['p50_us'] for x in group]):.2f} | {np.median([x['p99_us'] for x in group]):.2f} |")
    lines+=['','DS4 reports record the observed thumb axes, twelve-button/D-pad field, triggers and report size in CSV. GIP uses a native virtual USB profile observed through XInput, with trigger conversion explicitly handled by the producer. Neither is a physical Bluetooth/USB measurement.','','Initial filter association may require a guest restart. The fixture uses a stable USB serial so Windows can retain per-instance filter configuration. This is a descriptor-level fixture adaptation, not a driver or license modification. Failed pre-restart attempts remain in the dataset.','','CPU figures in per-run JSON are producer/receiver process-lifetime milliseconds, including initialization and warm-up. Peak working set includes process pages and SDKs. Neither is isolated kernel CPU or driver pool usage.','','[Per-run controller results](../assets/xinput-results.json) · [Raw data](../assets/raw-results.zip) · [Method](../methodology/measurement.md)']
    (ROOT/'docs/gamepad/results.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('XInput validated runs:',len(valid))
if __name__=='__main__':main()
