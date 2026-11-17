"""Additional plots from validated raw measurements, never synthetic fill data."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import ROOT,rows
assets=ROOT/'docs/assets'
runs=json.loads((ROOT/'data/processed/results.json').read_text())
hid=[r for r in runs if r['status']=='measured' and r['profile']=='vendor-hid' and r.get('purpose','latency')=='latency']
fig,ax=plt.subplots(figsize=(9,4.8));samples=0
for hz in sorted(set(r['requested_hz'] for r in hid)):
    values=[]
    for r in hid:
        if r['requested_hz']!=hz:continue
        p=ROOT/r['source'];cfg=json.loads((p/'run.json').read_text(encoding='utf-8-sig'));data=[x for x in rows(p/'reception.csv') if x['sequence']>=cfg['warmup']]
        values.extend((x['receive_qpc']-x['submit_qpc'])*1e6/cfg['qpc_frequency'] for x in data if x['content_valid'])
    latency=np.sort(values);samples+=len(latency)
    assert len(latency)>0 and min(latency)>0
    ax.step(latency,np.arange(1,len(latency)+1)*100/len(latency),where='post',label=f'{hz:,}/s requested; n={len(latency):,}')
ax.set_xscale('log');ax.set_xlabel('Submission to independent HID observation (microseconds, log scale)');ax.set_ylabel('Observed reports at or below latency (%)');ax.set_title('Vdevice 1.0.5.0 · Windows 11 Hyper-V · latency distribution');ax.grid(alpha=.2);ax.legend(loc='lower right')
fig.text(.01,.01,f'{samples:,} observed post-warmup reports · 2026-11-17 · descriptive pooled CDF, not run-level headline percentiles',fontsize=8);fig.tight_layout(rect=(0,.05,1,1))
for ext in ['svg','png']:fig.savefig(assets/f'hid-distribution.{ext}',dpi=150)
plt.close(fig)
pad=json.loads((ROOT/'data/processed/xinput-results.json').read_text());valid=[r for r in pad if r['status']=='measured' and r['filter']=='baseline' and r.get('producer_peak_working_set_bytes') is not None]
keys=sorted(set((r['backend'],r['profile']) for r in valid));groups=[[r for r in valid if (r['backend'],r['profile'])==k] for k in keys]
fig,axes=plt.subplots(1,2,figsize=(11,5));labels=[a+'\n'+b for a,b in keys]
for ax,field,factor,title,ylabel in [(axes[0],'producer_cpu_lifetime_ms',1,'Producer process-lifetime CPU','CPU time (milliseconds)'),(axes[1],'producer_peak_working_set_bytes',1/(1024**2),'Producer peak working set','Peak working set (MiB)')]:
    values=[[r[field]*factor for r in g] for g in groups]
    ax.boxplot(values,tick_labels=labels,showfliers=True)
    for i,vals in enumerate(values,1):ax.scatter([i]*len(vals),vals,s=12,alpha=.65,color='#4051b5',zorder=3)
    ax.set_title(title);ax.set_ylabel(ylabel);ax.tick_params(axis='x',labelsize=8,rotation=22);ax.grid(axis='y',alpha=.2)
fig.suptitle('Virtual controller baseline fixtures · Windows 11 Hyper-V · 2026-11-17')
fig.text(.01,.01,'Setup, warm-up, SDK workers and waiting included; coarse Windows CPU accounting; not isolated driver CPU or a throughput-normalized ranking.',fontsize=8)
fig.tight_layout(rect=(0,.07,1,.95))
for ext in ['svg','png']:fig.savefig(assets/f'controller-resources.{ext}',dpi=150)
plt.close(fig)
text=['---','title: Input latency distributions and process resource diagnostics','description: Generated latency CDF and producer CPU and memory plots from validated virtual-device records, with raw-data links and measurement limitations.','---','# Distributions and resource diagnostics','','## Vendor HID latency distribution','','![Observed vendor HID latency cumulative distribution](../assets/hid-distribution.svg)','','This descriptive CDF pools independently observed post-warmup reports at each requested submission rate. It retains measured tails and excludes stability/instrumented trials. Run-level medians and bootstrap intervals remain the headline statistics on the [latency page](../vdevice/latency.md). Unmatched reports are counted there and in the raw results; a received-report CDF does not depict missing reports.','','## Controller producer CPU and memory','','![Controller producer process CPU and peak working set](../assets/controller-resources.svg)','','Points are individual validated baseline runs; boxes describe their distribution. CPU is process-lifetime user plus kernel accounting in milliseconds, including initialization, warm-up and SDK threads. Peak working set is process pages, not driver pool usage. Different profile stacks and polling schedules prevent a universal CPU-efficiency ranking. Zero at coarse accounting resolution does not mean zero work.','','| Backend/profile | Runs | Median producer CPU (ms) | Median peak working set (MiB) |','|---|---:|---:|---:|']
for key,g in zip(keys,groups):text.append(f'| {key[0]}/{key[1]} | {len(g)} | {np.median([r["producer_cpu_lifetime_ms"] for r in g]):.3f} | {np.median([r["producer_peak_working_set_bytes"]/(1024**2) for r in g]):.3f} |')
text+=['','These figures do not establish device enumeration latency or a memory-leak verdict. Dedicated enumeration timing and multi-hour leak qualification remain additional work. See the [five-minute memory observation](stability.md), [separate WPR/DPC trial](etw.md) and [open stability incident](incident-wdf-001.md).','','[Raw measurements](../assets/raw-results.zip) · [Per-run resource counters](../assets/xinput-results.json). All charts are regenerated by `scripts/diagnostic_charts.py` from validated records.']
(ROOT/'docs/methodology/diagnostics.md').write_text('\n'.join(text)+'\n',encoding='utf8')
print('Diagnostic plots generated:',samples,'HID reports;',len(valid),'controller process records')
