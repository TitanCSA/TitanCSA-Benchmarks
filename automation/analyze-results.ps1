$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$python=Join-Path $root '.venv/Scripts/python.exe'
foreach($script in 'report.py','xinput_report.py','input_report.py','joystick_report.py','stability_report.py','site_content.py','etw_report.py','final_report.py','archive_results.py'){
 & $python (Join-Path $root ('scripts/'+$script));if($LASTEXITCODE -ne 0){throw ('Analysis failed: '+$script)}
}
Push-Location $root
try{& $python -m mkdocs build --strict;if($LASTEXITCODE -ne 0){throw 'Site build failed'};& $python scripts/validate_site.py;if($LASTEXITCODE -ne 0){throw 'Site validation failed'}}finally{Pop-Location}
