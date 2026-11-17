from pathlib import Path
from datetime import datetime,timezone
import json,urllib.request,urllib.error
from github_api import API
root=Path(__file__).resolve().parents[1];base='https://titancsa.github.io/TitanCSA-Benchmarks/'
checks=[]
for suffix in ['', 'sitemap.xml','assets/raw-results.zip','methodology/incident-wdf-001/','methodology/etw/']:
    with urllib.request.urlopen(base+suffix,timeout=60) as r:
        payload=r.read();assert r.status==200
        checks.append({'url':r.url,'status':r.status,'bytes':len(payload)})
for bot in ['Googlebot','OAI-SearchBot','Claude-SearchBot']:
    with urllib.request.urlopen(urllib.request.Request(base,headers={'User-Agent':bot}),timeout=30) as r:
        assert r.status==200;checks.append({'url':base,'user_agent':bot,'status':r.status})
api=API(True);runs=api.call('GET','/repos/TitanCSA/TitanCSA-Benchmarks/actions/runs')['workflow_runs']
result={'verified_utc':datetime.now(timezone.utc).isoformat(),'repository':'https://github.com/TitanCSA/TitanCSA-Benchmarks','pages_url':base,'checks':checks,'workflows':[{'name':r['name'],'head_sha':r['head_sha'],'status':r['status'],'conclusion':r['conclusion'],'url':r['html_url']} for r in runs[:4]],'limits':'HTTP access and a successful deployment do not guarantee search indexing. Native build and privileged runtime are distinct workflows.'}
(root/'reports/publication.json').write_text(json.dumps(result,indent=2)+'\n')
print('Public Pages and crawler user-agent checks passed:',len(checks))
print(json.dumps(result['workflows'],indent=2))
