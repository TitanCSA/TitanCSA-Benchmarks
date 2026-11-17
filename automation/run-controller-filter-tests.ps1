param([ValidateSet('Combined','Gamepad-Controller')][string]$Filter,[int]$Repetitions=3,[ValidateSet('forward','modify')][string]$Operation='modify',[ValidateSet('xbox360','ds4','xbox-one-gip')][string]$Profile='xbox360')
. (Join-Path $PSScriptRoot 'Lab.ps1')
for($attempt=0;$attempt -lt 3;$attempt++){
 $started=[DateTime]::UtcNow
 try{& (Join-Path $PSScriptRoot 'run-gamepad-tests.ps1') -Backend vdevice -Filter $Filter -Operation $Operation -Repetitions $Repetitions -Profile $Profile;return}
 catch{
  $candidates=@(Get-ChildItem (Join-Path $script:BenchmarkRoot 'data/raw') -Recurse -Filter 'xinput-run.json'|ForEach-Object{
   try{$cfg=Get-Content $_.FullName -Raw|ConvertFrom-Json}catch{return}
   if($cfg.filter -eq $Filter -and [DateTime]::Parse($cfg.utc).ToUniversalTime() -ge $started.AddSeconds(-1)){[pscustomobject]@{directory=$_.DirectoryName;utc=$cfg.utc}}
  }|Sort-Object utc -Descending)
  if(!$candidates -or $attempt -eq 2){throw}
  $diag=Join-Path $candidates[0].directory 'adapter-init.json'
  if(!(Test-Path $diag) -or !(Get-Content $diag -Raw|ConvertFrom-Json).reboot_required){throw}
  Write-Output 'Windows requires guest restart for the recorded filter association. Failed attempt retained.'
  & (Join-Path $PSScriptRoot 'restart-lab-guest.ps1')
 }
}
