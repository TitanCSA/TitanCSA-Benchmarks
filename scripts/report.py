from pathlib import Path
import json,shutil,zipfile,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import ROOT,main as analyze
BASE='https://titancsa.github.io/TitanCSA-Benchmarks/'
def main():
    results=analyze();valid=[r for r in results if r['status']=='measured' and r['profile']=='vendor-hid' and r.get('purpose','latency')=='latency'];assert valid,'No real valid measurements; refusing to publish invented charts'
    assets=ROOT/'docs/assets';assets.mkdir(exist_ok=True)
    rates=sorted(set(r['requested_hz'] for r in valid));groups=[[r for r in valid if r['requested_hz']==hz] for hz in rates]
    fig,ax=plt.subplots(figsize=(9,4.7));x=np.arange(len(rates));width=.35
    ax.bar(x-width/2,[np.median([r['p50_us'] for r in g]) for g in groups],width,label='Median of run P50')
    ax.bar(x+width/2,[np.median([r['p99_us'] for r in g]) for g in groups],width,label='Median of run P99')
    ax.set_xticks(x,[str(hz) for hz in rates]);ax.set_xlabel('Requested report rate (reports/s); actual rate in table');ax.set_ylabel('Submission to HID ReadFile completion (microseconds)');ax.set_title('Vdevice 1.0.5.0 · Windows 11 Hyper-V · virtual vendor HID');ax.legend();ax.grid(axis='y',alpha=.2)
    fig.text(.01,.01,f"{len(valid)} runs · {sum(r['received'] for r in valid):,} post-warmup reports · {valid[-1]['utc'][:10]} · software path, not physical USB latency",fontsize=8)
    fig.tight_layout(rect=(0,.06,1,1));fig.savefig(assets/'hid-latency.svg');fig.savefig(assets/'hid-latency.png',dpi=160);plt.close(fig)
    table=['| Requested reports/s | Runs | Received reports | Median run P50 (µs) | Median run P99 (µs) | Observed submissions/s | Missing |','|---:|---:|---:|---:|---:|---:|---:|']
    aggregates=[]
    for hz,g in zip(rates,groups):
        med=np.array([r['p50_us'] for r in g]);rng=np.random.default_rng(42137)
        ci=np.percentile(np.median(rng.choice(med,(10000,len(med)),replace=True),axis=1),[2.5,97.5]) if len(med)>=3 else [float('nan')]*2
        aggregates.append({'requested_hz':hz,'runs':len(g),'median_run_p50_us':float(np.median(med)),'median_run_p50_bootstrap_95ci_us':[None if not np.isfinite(v) else float(v) for v in ci]})
        table.append(f"| {hz} | {len(g)} | {sum(r['received'] for r in g)} | {np.median(med):.2f} | {np.median([r['p99_us'] for r in g]):.2f} | {np.median([r['observed_submission_hz'] for r in g]):.1f} | {sum(r['missing'] for r in g)} |")
    (ROOT/'data/processed/aggregates.json').write_text(json.dumps(aggregates,indent=2)+'\n')
    text='''---
title: Windows virtual HID input latency — measured Vdevice results
description: Reproducible Windows 11 Hyper-V measurements from Vdevice report submission to an independent Windows HID receiver, with raw data and explicit limitations.
---
# Virtual HID input latency

These are real software-path measurements in a dedicated Windows 11 Hyper-V VM. The producer calls Vdevice `Send_Input`; a separate process receives the vendor-defined report through Windows `ReadFile`. Each report carries a sequence, same-guest QPC timestamp, seed and checksum. No physical USB latency or competitor superiority is claimed.

![Vdevice virtual vendor HID latency](../assets/hid-latency.svg)

'''+ '\n'.join(table)+'''

P50/P99 above are medians of per-run percentiles, not pooled percentiles. Warm-up is 100 reports per run. Requested frequency is a scheduling target; observed submissions are measured. All tails remain in the results. Repeats use fresh processes and device creation in the same VM, not independent hosts. Bootstrap intervals in the aggregate JSON describe between-run medians only; small samples and shared host conditions limit generalization.

## Scope and limitations

- This vendor-defined HID profile is not a keyboard, mouse or Xbox controller profile.
- It does not traverse an Interceptor filter. This page makes no interception-overhead claim.
- Latency includes producer work after the timestamp, Windows virtual USB/HID processing, queuing and receiver scheduling. It is not isolated kernel execution time.
- Windows HID buffering was set to 512 reports. Report length is 32 bytes; USB interrupt descriptor interval is 1 ms at full speed. A higher submission rate does not mean a higher USB polling frequency.
- Process CPU/memory counters cover the process lifetime, including enumeration and waiting; zero CPU counters at coarse Windows accounting resolution do not mean zero CPU cost.
- HVCI is disabled in the guest; Secure Boot is on. Other host workloads were not suspended.
- Pilot runs and failed runs remain in the archive. The results JSON identifies invalid runs and their reasons. No valid measured run is discarded for an unfavorable tail.

## Download and reproduce

[Raw CSV/JSON archive](../assets/raw-results.zip) · [Per-run statistics](../assets/results.json) · [Aggregate statistics](../assets/aggregates.json) · [Environment](../methodology/environment.md) · [Reproduction](../methodology/reproducibility.md)

'''
    (ROOT/'docs/vdevice/latency.md').write_text(text,encoding='utf8')
    for name in ['results.json','aggregates.json']:shutil.copyfile(ROOT/'data/processed'/name,assets/name)
    with zipfile.ZipFile(assets/'raw-results.zip','w',zipfile.ZIP_DEFLATED) as z:
        for folder in ['data/raw','data/stability','data/environments','reports']:
            for p in sorted((ROOT/folder).rglob('*')):
                if p.is_file():z.write(p,p.relative_to(ROOT).as_posix())
        z.write(ROOT/'data/LICENSE','data/LICENSE')
    print('Generated chart and report from measured CSV rows')
if __name__=='__main__':main()
