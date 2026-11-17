from pathlib import Path
import hashlib,json,urllib.request
ROOT=Path(__file__).resolve().parents[1]
audit=json.loads((ROOT/'reports/repository-audit.json').read_text())
selected={'TitanCSA/Vdevice':['VdeviceSetupConsole.exe','Vdevice-Driver-1.0.5.0.zip'],'nefarius/ViGEmBus':['ViGEmBus_1.22.0_x64_x86_arm64.exe'],'oblitum/Interception':['Interception.zip']}
out=ROOT/'.local/downloads';out.mkdir(parents=True,exist_ok=True)
manifest=[]
for repo,names in selected.items():
    r=next(x for x in audit['repositories'] if x['requested']==repo)
    for name in names:
        a=next(x for x in r['release']['assets'] if x['name']==name)
        path=out/name
        if not path.exists():
            with urllib.request.urlopen(a['browser_download_url'],timeout=120) as response:path.write_bytes(response.read())
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        expected=a.get('digest')
        if expected and expected!='sha256:'+sha:raise ValueError('Published digest mismatch: '+name)
        manifest.append({'repository':repo,'release':r['release']['tag_name'],'name':name,'url':a['browser_download_url'],'sha256':sha,'upstream_digest_verified':bool(expected),'size':path.stat().st_size})
(ROOT/'reports/artifacts.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
print('Downloaded and hashed',len(manifest),'official release artifacts')
