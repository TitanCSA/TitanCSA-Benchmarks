"""Append only the requested benchmark section to fresh GitHub README contents."""
from pathlib import Path
import base64,json,statistics,urllib.request
from github_api import API
root=Path(__file__).resolve().parents[1]
base='https://titancsa.github.io/TitanCSA-Benchmarks/'
with urllib.request.urlopen(base,timeout=30) as response:assert response.status==200
raw=json.loads((root/'data/processed/results.json').read_text())
pad=json.loads((root/'data/processed/xinput-results.json').read_text())
api=API(True);receipt=[]
for name,filter_name in [('Interceptor','Combined'),('Interceptor-Keyboard-Mouse','Keyboard-Mouse'),('Interceptor-Gamepad-Controller','Gamepad-Controller'),('Vdevice',None)]:
    if name=='Vdevice':
        rows=[r for r in raw if r['status']=='measured' and r['profile']=='vendor-hid' and r.get('purpose','latency')=='latency']
        table=f'| Vendor-defined HID delivery | {len(rows)} validated runs; {sum(r["received"] for r in rows):,} post-warmup reports |\n'
        target='vdevice/latency/';description='Vendor HID reports, independent keyboard/mouse and controller reception, and a matched WinMM joystick subset.'
    elif name=='Interceptor-Keyboard-Mouse':
        rows=[r for r in raw if r['status']=='measured' and r['filter']==filter_name]
        table=f'| Virtual keyboard/mouse filter paths | {len(rows)} validated runs: forwarding, mouse remapping and controlled blocking |\n'
        target='interceptor/results/';description='Virtual HID input crosses the tested filter and is checked by a separate Windows Raw Input receiver, with per-run PnP and capture evidence.'
    else:
        rows=[r for r in pad if r['status']=='measured' and r['filter']==filter_name and r['profile']=='xbox360']
        table=f'| Virtual XUSB modification to XInput observation | {len(rows)} validated runs; median run P50 {statistics.median(r["p50_us"] for r in rows):.2f} microseconds |\n'
        target='gamepad/results/';description='Selected virtual input transformations are independently observed; controller results are separated by protocol and receiver API.'
    section=f'''## Performance & Benchmarks

[Measured results and raw data]({base}{target}) · [Comparisons]({base}comparisons/) · [Methodology]({base}methodology/measurement/)

{description} These are publisher-operated Windows 11 Hyper-V software-path measurements, not physical USB latency or a universal speed ranking.

| Tested scope | Verified result |
|---|---|
{table}
**Stability limitation:** the Vdevice-backed controller campaign reproduced an unresolved guest WDF queue-purge bugcheck. Successful timings do not establish safe repeated teardown. See the [incident and test limits]({base}methodology/incident-wdf-001/).
'''
    repo='TitanCSA/'+name
    existing=api.call('GET','/repos/'+repo+'/readme')
    content=base64.b64decode(existing['content']).decode('utf8')
    if '## Performance & Benchmarks' in content:
        receipt.append({'repository':repo,'status':'existing section retained for review'});continue
    result=api.call('PUT','/repos/'+repo+'/contents/'+existing['path'],{'message':'Link measured benchmark evidence and open stability finding','sha':existing['sha'],'content':base64.b64encode((content.rstrip()+'\n\n'+section).encode()).decode()})
    receipt.append({'repository':repo,'status':'updated','commit':result['commit']['sha'],'url':result['commit']['html_url']})
    print(repo,'README updated')
(root/'reports/readme-publication.json').write_text(json.dumps(receipt,indent=2)+'\n')
