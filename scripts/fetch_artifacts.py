from pathlib import Path
import hashlib,json,urllib.request,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'reports/artifacts.json').read_text())
out=ROOT/'.local/downloads';out.mkdir(parents=True,exist_ok=True)
for item in manifest:
    name=item['name'];assert Path(name).name==name and '/' not in name and '\\' not in name
    url=urllib.parse.urlparse(item['url']);assert url.scheme=='https' and url.hostname=='github.com'
    path=out/name
    if not path.exists():
        temporary=path.with_suffix(path.suffix+'.partial')
        with urllib.request.urlopen(item['url'],timeout=120) as response:temporary.write_bytes(response.read())
        assert hashlib.sha256(temporary.read_bytes()).hexdigest()==item['sha256'],'Artifact digest mismatch: '+name
        temporary.replace(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'Artifact digest mismatch: '+name
print('Pinned artifacts verified:',len(manifest),'; no installer executed, manifest unchanged')
