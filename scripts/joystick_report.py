import json,hashlib
import numpy as np
from analyze import ROOT,rows
def main():
    results=[]
    for p in sorted((ROOT/'data/raw').rglob('joystick-run.json')):
        try:cfg=json.loads(p.read_text())
        except ValueError:
            results.append({'run_id':p.parent.name,'backend':'unknown','profile':'unknown','source':p.parent.relative_to(ROOT).as_posix(),'status':'invalid','reason':'Malformed or interrupted run metadata'});continue
        r={'run_id':cfg['run_id'],'backend':cfg['backend'],'profile':cfg['profile'],'version':cfg['version'],'source':p.parent.relative_to(ROOT).as_posix(),'status':'invalid','utc':cfg['utc']}
        try:
            assert json.loads((p.parent/'joystick-done.json').read_text())['status']=='completed','No completed native run'
            tx=rows(p.parent/'joystick-submission.csv');rx=rows(p.parent/'joystick-reception.csv');caps=json.loads((p.parent/'joystick-caps.json').read_text());total=cfg['samples']+cfg['warmup'];warm=cfg['warmup'];freq=cfg['qpc_frequency'];lo=cfg['axis_min'];hi=cfg['axis_max']
            assert len(tx)==len(rx)==total,'Incomplete joystick sequence'
            for n,(a,b) in enumerate(zip(tx,rx),1):
                assert a['sequence']==b['sequence']==n and a['submit_qpc']==b['submit_qpc'] and b['receive_qpc']>=b['submit_qpc'],'Joystick correlation mismatch'
                raw=lo+(n%200+1)*(hi-lo)//256;other=hi-(raw-lo)
                x=caps['x_min']+(raw-lo)*(caps['x_max']-caps['x_min'])//(hi-lo);y=caps['y_min']+(other-lo)*(caps['y_max']-caps['y_min'])//(hi-lo)
                assert abs(b['observed_x']-x)<=3 and abs(b['observed_y']-y)<=3 and b['observed_buttons']==1<<(n%8),'Observed joystick state mismatch'
            lat=np.array([(b['receive_qpc']-b['submit_qpc'])*1e6/freq for b in rx[warm:]])
            r.update(status='measured',samples=cfg['samples'],p50_us=float(np.percentile(lat,50)),p99_us=float(np.percentile(lat,99)),min_us=float(min(lat)),max_us=float(max(lat)),stack_captured=(p.parent/'pnp-stack.txt').exists(),hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.parent.iterdir() if f.is_file()})
        except (AssertionError,FileNotFoundError,KeyError,ValueError) as e:r['reason']=str(e)
        results.append(r)
    text=['---','title: Vdevice vs vJoy — virtual joystick state visibility through WinMM','description: Matched X/Y axes and eight buttons measured through an independent WinMM receiver, with raw observed states and per-run PnP evidence.','---','# Vdevice vs vJoy: a joystick comparison','','This compares a shared subset of joystick functionality: two axes and eight selected buttons. Vdevice uses a descriptor-driven USB HID joystick; vJoy 2.2.2.0 (BrunnerInnovation distribution) uses its own virtual HID driver and SDK. A separate executable observes each state through Windows `joyGetPosEx`. This is not an XInput or Xbox-controller benchmark.','','| Backend | Release | Runs | States | Median run P50 (µs) | Median run P99 (µs) |','|---|---|---:|---:|---:|---:|']
    for backend in ['vdevice','vjoy']:
        g=[r for r in results if r['status']=='measured' and r['backend']==backend]
        if g:text.append(f"| {backend} | {g[0]['version']} | {len(g)} | {sum(r['samples'] for r in g)} | {np.median([r['p50_us'] for r in g]):.2f} | {np.median([r['p99_us'] for r in g]):.2f} |")
    text+=['','The producer waits for acknowledgement after independent observation; only one state is outstanding. WinMM normalization is checked against the declared logical axis range and Windows capability ranges, with a three-unit tolerance for integer scaling. Consecutive states are separated by much more than that tolerance and use distinct button bits. Raw CSV includes observed X/Y/buttons, sequence and QPC timestamps.','','The two devices expose more capabilities than this shared subset. vJoy force feedback, additional axes/buttons, USB control handling and other transports are not scored here. WinMM polling, SDK work and scheduling are included. These are software-path measurements in one Hyper-V VM, not physical latency or a universal driver ranking.','','[Per-run joystick data](../assets/joystick-results.json) · [Raw archive](../assets/raw-results.zip) · [Methodology](../methodology/measurement.md)']
    (ROOT/'docs/vdevice/joystick.md').write_text('\n'.join(text)+'\n',encoding='utf8');(ROOT/'data/processed/joystick-results.json').write_text(json.dumps(results,indent=2)+'\n');(ROOT/'docs/assets/joystick-results.json').write_text(json.dumps(results,indent=2)+'\n');print('Valid joystick series:',sum(r['status']=='measured' for r in results))
if __name__=='__main__':main()
