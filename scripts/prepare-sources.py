"""Fetch audited commits without modifying installed drivers or credentials."""
from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'reports/repository-audit.json').read_text())
for repo in ['TitanCSA/Vdevice','TitanCSA/Interceptor','TitanCSA/Interceptor-Keyboard-Mouse','TitanCSA/Interceptor-Gamepad-Controller','nefarius/ViGEmClient','oblitum/Interception']:
    r=next(x for x in audit['repositories'] if x['requested']==repo)
    dest=root/'.local/sources'/repo.replace('/','--');dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():subprocess.run(['git','clone','--no-checkout',r['url']+'.git',str(dest)],check=True)
    subprocess.run(['git','-C',str(dest),'fetch','--depth=1','origin',r['commit']],check=True)
    subprocess.run(['git','-C',str(dest),'checkout','--detach',r['commit']],check=True)
    assert subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()==r['commit']
print('Audited source commits prepared')
