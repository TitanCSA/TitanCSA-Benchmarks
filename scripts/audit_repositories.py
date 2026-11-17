from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import json
from github_api import API
ROOT=Path(__file__).resolve().parents[1]
REPOS=['TitanCSA/Interceptor','TitanCSA/Interceptor-Keyboard-Mouse','TitanCSA/Interceptor-Gamepad-Controller','TitanCSA/Vdevice','TitanCSA/Interception-V2','oblitum/Interception','nefarius/ViGEmBus','nefarius/ViGEmClient','nefarius/HidHide','LizardByte/libvirtualhid','jshafer817/vJoy','BrunnerInnovation/vJoy','njz3/vJoy','microsoft/Windows-driver-samples']
def inspect(name):
    api=API(authenticate=True)
    try:
        r=api.call('GET','/repos/'+name)
        c=api.call('GET','/repos/'+name+'/commits/'+r['default_branch'])
        releases=api.call('GET','/repos/'+name+'/releases?per_page=1')
        return {'requested':name,'repository':r['full_name'],'url':r['html_url'],'default_branch':r['default_branch'],'commit':c['sha'],'commit_date':c['commit']['committer']['date'],'archived':r['archived'],'license':(r.get('license') or {}).get('spdx_id'),'description':r['description'],'release':None if not releases else {k:releases[0].get(k) for k in ['tag_name','published_at','html_url','assets']},'benchmark_status':'not_executed'}
    except Exception as e:return {'requested':name,'error':str(e),'benchmark_status':'not_executed'}
if __name__=='__main__':
    result={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'repositories':list(ThreadPoolExecutor(max_workers=4).map(inspect,REPOS))}
    target=ROOT/'reports/repository-audit.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    for r in result['repositories']:print(r['requested'],r.get('commit',r.get('error')),r.get('release',{}).get('tag_name') if r.get('release') else '')
