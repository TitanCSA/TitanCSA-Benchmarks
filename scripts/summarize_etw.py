"""Publish aggregate trace evidence only, never process/system details from an ETL."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
root=Path(__file__).resolve().parents[1]
private=Path(sys.argv[1]).resolve()
assert private.is_relative_to((root/'.local/etw').resolve())
xperf='C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/xperf.exe'
trace=private/'trace.etl'
for action,name in [('tracestats','trace-header.txt'),('dpcisr','dpc-isr.txt')]:
    subprocess.run([xperf,'-i',str(trace),'-o',str(private/name),'-a',action],check=True,capture_output=True)
header=(private/'trace-header.txt').read_text();dpc=(private/'dpc-isr.txt').read_text()
def number(pattern,text):
    match=re.search(pattern,text);assert match,pattern
    return int(match[1])
cpu=re.search(r'^\s*(\d+)\s+[\d.]+,\s*(\d+)\s+[\d.]+,\s*Vdevice.sys\s*$',dpc,re.M);assert cpu
result={'profile':'WPR GeneralProfile filemode','etl_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),'etl_bytes':trace.stat().st_size,'private_trace':True,'scenario':'Vendor HID; purpose=instrumented; 1000 measured and 100 warm-up reports; requested 1000/s','lost_events':number(r'Total # Lost Events\s*:\s*(\d+)',header),'lost_buffers':number(r'Total # Lost Buffers\s*:\s*(\d+)',header),'trace_duration_us':number(r'CPU Usage from 0 us to (\d+) us',dpc),'vdevice_dpc_duration_us_by_cpu':[int(cpu[1]),int(cpu[2])],'vdevice_dpc_count':number(r'Total = (\d+) for module Vdevice.sys',dpc),'limitations':'Whole instrumented trace includes setup, warm-up, report generation and teardown; DPC attribution by module is not total driver CPU, ISR proof, per-report cost or an uninstrumented latency measurement.'}
(root/'reports/etw-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('Sanitized ETW evidence written; lost events:',result['lost_events'])
