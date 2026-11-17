"""Create the requested owned repository and configure workflow-based Pages."""
from github_api import API
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
api=API(True);name='TitanCSA/TitanCSA-Benchmarks'
try:repo=api.call('GET','/repos/'+name)
except RuntimeError as e:
    if 'HTTP 404' not in str(e):raise
    repo=api.call('POST','/user/repos',{'name':'TitanCSA-Benchmarks','description':'Reproducible Windows input driver benchmarks: independent HID/Raw Input/XInput receivers, real Hyper-V measurements, raw data and source audits.','private':False,'auto_init':False,'has_wiki':False,'homepage':'https://titancsa.github.io/TitanCSA-Benchmarks/'})
assert repo['full_name'].lower()==name.lower() and repo['owner']['login'].lower()=='titancsa'
api.call('PUT','/repos/'+name+'/topics',{'names':['windows','benchmark','hyper-v','hid','xinput','usb','kmdf','input-latency','virtual-gamepad','reproducible-research','driver','cpp']})
try:pages=api.call('GET','/repos/'+name+'/pages')
except RuntimeError as e:
    if 'HTTP 404' not in str(e):raise
    pages=api.call('POST','/repos/'+name+'/pages',{'build_type':'workflow'})
if pages.get('build_type')!='workflow':api.call('PUT','/repos/'+name+'/pages',{'build_type':'workflow'})
out={'repository':repo['html_url'],'pages_url':pages.get('html_url'),'build_type':'workflow'}
(ROOT/'.local/publication.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
