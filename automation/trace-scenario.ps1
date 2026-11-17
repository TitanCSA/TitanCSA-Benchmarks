# Instrumented trial: ETL stays private; primary latency charts exclude this purpose.
. (Join-Path $PSScriptRoot 'Lab.ps1')
$id=[guid]::NewGuid().ToString('N')
$private=Join-Path $script:BenchmarkRoot ('.local/etw/'+$id)
New-Item -ItemType Directory -Path $private -Force|Out-Null
$s=New-BenchmarkSession
$ownedTrace=$false
try {
 Invoke-Command -Session $s -ScriptBlock {
  & wpr.exe -start GeneralProfile -filemode
  if($LASTEXITCODE -ne 0){throw 'WPR did not start; existing sessions will not be cancelled'}
 }
 $ownedTrace=$true
 $started=[DateTime]::UtcNow.ToString('o')
 & (Join-Path $PSScriptRoot 'run-virtual-device-tests.ps1') -Rates @(1000) -Repetitions 1 -Samples 1000 -Purpose instrumented
}finally {
 if($ownedTrace){
  Invoke-Command -Session $s -ArgumentList $id -ScriptBlock {
   param($id)
   & wpr.exe -stop ('C:\TitanCSABenchmarkLab\'+$id+'.etl')
   if($LASTEXITCODE -ne 0){throw 'WPR stop failed'}
  }
  Copy-Item ('C:\TitanCSABenchmarkLab\'+$id+'.etl') (Join-Path $private 'trace.etl') -FromSession $s
 }
 Remove-PSSession $s
}
$trace=Join-Path $private 'trace.etl'
$xperf='C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\xperf.exe'
& $xperf -i $trace -o (Join-Path $private 'trace-statistics.txt') -a tracestats -detail
if($LASTEXITCODE -ne 0){throw 'ETL statistics validation failed'}
@{id=$id;started_utc=$started;profile='WPR GeneralProfile filemode';scenario='vendor HID 1000 reports at requested 1000/s; purpose=instrumented';etl_sha256=(Get-FileHash $trace).Hash.ToLowerInvariant();etl_bytes=(Get-Item $trace).Length;private_trace=$true;analysis='xperf trace-statistics decoded locally; no isolated driver CPU/DPC attribution claimed';latency_chart_included=$false}|ConvertTo-Json|Set-Content (Join-Path $script:BenchmarkRoot 'reports/etw-validation.json') -Encoding ASCII
Write-Output 'WPR trace recorded and decoded; private ETL retained, fingerprint published.'
& (Join-Path $script:BenchmarkRoot '.venv/Scripts/python.exe') (Join-Path $script:BenchmarkRoot 'scripts/summarize_etw.py') $private
if($LASTEXITCODE -ne 0){throw 'Sanitized ETW summary failed'}
