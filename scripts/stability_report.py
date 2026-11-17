import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import ROOT
def main():
    runs=[]
    for folder in sorted((ROOT/'data/stability').glob('*')):
        if not folder.is_dir() or not (folder/'after.json').exists():continue
        before=json.loads((folder/'before.json').read_text());after=json.loads((folder/'after.json').read_text())
        with (folder/'memory.csv').open(newline='') as f:memory=list(csv.DictReader(f))
        runs.append({'id':folder.name,'samples':len(memory),'remaining_processes':after['remaining_owned_native_processes'],'remaining_test_pnp_nodes':after['present_test_nodes'],'boot_timestamp_unchanged':before['boot']==after['boot'],'nonpaged_min_bytes':min(int(r['nonpaged_bytes']) for r in memory),'nonpaged_max_bytes':max(int(r['nonpaged_bytes']) for r in memory),'paged_min_bytes':min(int(r['paged_bytes']) for r in memory),'paged_max_bytes':max(int(r['paged_bytes']) for r in memory)})
        fig,ax=plt.subplots(figsize=(9,4.2));ax.plot(range(len(memory)),[int(r['nonpaged_bytes'])/1048576 for r in memory],label='System nonpaged pool');ax.plot(range(len(memory)),[int(r['paged_bytes'])/1048576 for r in memory],label='System paged pool');ax.set_xlabel('Monitor sample index (nominal interval 10 s)');ax.set_ylabel('MiB (system-wide; not driver-attributed)');ax.set_title('Windows 11 Hyper-V · monitored virtual HID stability trial');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(ROOT/'docs/assets/stability-memory.svg');plt.close(fig)
    (ROOT/'data/processed/stability-results.json').write_text(json.dumps(runs,indent=2)+'\n')
    text='''---
title: Virtual HID stability trial — five-minute reception and memory observations
description: A bounded monitored Windows virtual HID run, including independently validated reports, device/process cleanup and system pool counters without leak-free claims.
---
# Five-minute monitored HID trial

The dedicated VM ran a 125 reports/s vendor-HID scenario for 37,500 measured reports plus 100 warm-up reports. Independent Windows HID reception and the standard sequence/checksum validator qualify the CSV. This series is tagged `purpose=stability` and is excluded from primary latency charts because a PowerShell memory sampler intentionally runs alongside it.

![System pool memory samples](../assets/stability-memory.svg)

| Observation | Recorded result |
|---|---|
'''
    for r in runs:
        text+=f"| Memory samples | {r['samples']} |\n| Owned native processes after cleanup | {r['remaining_processes']} |\n| Present vendor-HID test nodes after cleanup | {r['remaining_test_pnp_nodes']} |\n| Nonpaged pool range, system-wide | {r['nonpaged_min_bytes']/1048576:.2f}–{r['nonpaged_max_bytes']/1048576:.2f} MiB |\n"
    text+='''
## What this does and does not show

This is one five-minute exposure, not a multi-hour soak, fault-injection qualification or proof of no memory leaks. Pool counters cover all guest drivers, Windows background work and the sampler. They cannot attribute allocations or deallocations to Vdevice alone.

The wall-clock-derived WMI boot timestamp changed between the initial post-checkpoint snapshot and the final observation. That field is therefore not used as a reliable restart detector. The native workload's continuous completed QPC/sequence record is the timing evidence; no latency is computed from host/guest or unsynchronized wall clocks.

**This standalone vendor-HID run does not close [WDF-001](incident-wdf-001.md).** The controller teardown incident remains visible and unresolved. More isolated pool-tag attribution, repeated teardown, cancellation and long-duration tests are needed.

[Raw CSV/JSON](../assets/raw-results.zip) · [Per-run qualification](../assets/results.json) · [Environment](environment.md)
'''
    (ROOT/'docs/methodology/stability.md').write_text(text,encoding='utf8')
    (ROOT/'docs/assets/stability-results.json').write_bytes((ROOT/'data/processed/stability-results.json').read_bytes())
    print('Monitored stability trials:',len(runs))
if __name__=='__main__':main()
