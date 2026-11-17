$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
foreach($name in 'python','git','cmake'){if(!(Get-Command $name -ErrorAction SilentlyContinue)){throw ('Install official prerequisite first: '+$name)}}
$python=Join-Path $root '.venv/Scripts/python.exe'
if(!(Test-Path $python)){python -m venv (Join-Path $root '.venv');if($LASTEXITCODE -ne 0){throw 'Virtual environment creation failed'}}
& $python -m pip install --disable-pip-version-check -r (Join-Path $root 'requirements.txt')
if($LASTEXITCODE -ne 0){throw 'Report dependencies failed'}
Write-Output 'Pinned report dependencies ready; no host driver or security setting changed.'
