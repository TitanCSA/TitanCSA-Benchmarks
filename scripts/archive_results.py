"""Build the downloadable archive after every report has been refreshed."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
with zipfile.ZipFile(root/'docs/assets/raw-results.zip','w',zipfile.ZIP_DEFLATED) as z:
    for folder in ['data/raw','data/stability','data/environments','reports']:
        for p in sorted((root/folder).rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    z.write(root/'data/LICENSE','data/LICENSE')
print('Raw archive refreshed after all reports')
