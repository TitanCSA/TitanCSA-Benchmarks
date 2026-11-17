from pathlib import Path
import json,hashlib,urllib.request,zipfile
root=Path(__file__).resolve().parents[1]
item=next(x for x in json.loads((root/'reports/artifacts.json').read_text()) if x['name']=='vJoy-SDK.zip')
archive=root/'.local/downloads/vJoy-SDK.zip';archive.parent.mkdir(parents=True,exist_ok=True)
if not archive.exists():archive.write_bytes(urllib.request.urlopen(item['url'],timeout=60).read())
assert hashlib.sha256(archive.read_bytes()).hexdigest()==item['sha256']
out=root/'.local/vjoy-sdk';out.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:
    for name in z.namelist():assert (out/name).resolve().is_relative_to(out.resolve())
    z.extractall(out)
print('Pinned vJoy 2.2.2.0 SDK extracted; no installer executed')
