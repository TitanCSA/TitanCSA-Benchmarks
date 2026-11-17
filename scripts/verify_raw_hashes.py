"""Fail when stored raw-file bytes differ from their recorded measurement hashes."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];checked=0
for name in ['results.json','xinput-results.json','joystick-results.json']:
    for run in json.loads((root/'data/processed'/name).read_text()):
        for filename,expected in run.get('hashes',{}).items():
            path=root/run['source']/filename
            assert path.resolve().is_relative_to((root/'data/raw').resolve())
            assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,'Raw evidence hash differs: '+str(path.relative_to(root))
            checked+=1
assert checked>0,'No raw hashes checked'
print('Original raw file hashes verified:',checked)
