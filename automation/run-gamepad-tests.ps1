param([ValidateSet('vdevice','vigem')][string]$Backend,[int]$Repetitions=3,[int]$Samples=1000,[ValidateSet('baseline','Combined','Gamepad-Controller')][string]$Filter='baseline',[ValidateSet('forward','modify')][string]$Operation='forward',[ValidateSet('xbox360','ds4','xbox-one-gip')][string]$Profile='xbox360')
. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession
$campaign=[guid]::NewGuid().ToString('N');$local=Join-Path $script:BenchmarkRoot ('data/raw/'+$campaign)
New-Item -ItemType Directory $local|Out-Null
try {
 foreach($n in 'TitanCSA-Benchmark-XInput.exe','TitanCSA-Benchmark-XInputReceiver.exe','TitanCSA-Benchmark-Ds4Receiver.exe'){Copy-Item (Join-Path $script:BenchmarkRoot ('build/Release/'+$n)) ('C:\TitanCSABenchmarkLab\bin\'+$n) -ToSession $s}
 if($Filter -ne 'baseline'){$n='TitanCSA-Benchmark-Intercept-'+$Filter+'.exe';Copy-Item (Join-Path $script:BenchmarkRoot ('build/Release/'+$n)) ('C:\TitanCSABenchmarkLab\bin\'+$n) -ToSession $s}
 for($rep=0;$rep -lt $Repetitions;$rep++){
  $id=$campaign+'-'+$rep+'-'+$Backend
  $cfg=@{backend=$Backend;samples=$Samples;warmup=100;repetition=$rep;run_id=$id;utc=[DateTime]::UtcNow.ToString('o');category='virtual-xbox360';device_origin='virtual';version=$(if($Backend -eq 'vdevice'){'1.0.5.0'}else{'1.22.0'});mode='closed-loop';seed=42137;collect_stack=$true}
  $cfg.filter=$Filter;$cfg.operation=$Operation
  $cfg.profile=$Profile
$cfg.build_identity=Get-BenchmarkBuildIdentity
  $p=Join-Path $script:BenchmarkRoot '.local/xinput-scenario.json';$cfg|ConvertTo-Json -Depth 10|Set-Content $p -Encoding ASCII;Copy-Item $p C:\TitanCSABenchmarkLab\xinput-scenario.json -ToSession $s
  Invoke-Command -Session $s -ArgumentList $id,$Filter,$Profile -ScriptBlock {
   param($id,$filter,$profile)
   $adapter=$null
   $out='C:\TitanCSABenchmarkLab\results\'+$id
   $receiver=if($profile -eq 'ds4'){'C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-Ds4Receiver.exe'}else{'C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-XInputReceiver.exe'}
   $p=Start-Process C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-XInput.exe -ArgumentList 'C:\TitanCSABenchmarkLab\xinput-scenario.json',$out,$receiver -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-xinput.stderr');$null=$p.Handle
   try{
    $end=(Get-Date).AddSeconds(45);while(!(Test-Path (Join-Path $out 'xinput-run.json')) -and !$p.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 100}
    if(!(Test-Path (Join-Path $out 'xinput-run.json'))){throw 'Native controller enumeration failed'}
    if($filter -ne 'baseline'){
     $adapter=Start-Process ('C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-Intercept-'+$filter+'.exe') -ArgumentList $out -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-adapter.stderr');$null=$adapter.Handle
     $end=(Get-Date).AddSeconds(30);while(!(Test-Path (Join-Path $out 'adapter-ready.json')) -and !$adapter.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 50}
     if(!(Test-Path (Join-Path $out 'adapter-ready.json'))){throw 'Controller filter adapter startup failed'}
    }
    $devices=Get-PnpDevice -PresentOnly|Where-Object InstanceId -match '(VID_045E&PID_028E|VID_045E&PID_02D1|VID_054C&PID_05C4|VIGEM)'
    foreach($d in $devices){pnputil /enum-devices /instanceid $d.InstanceId /stack /services /relations /drivers | Out-File (Join-Path $out 'pnp-stack.txt') -Append -Encoding UTF8}
    '{"captured":true}'|Set-Content (Join-Path $out 'stack-captured.json') -Encoding ASCII
    if(!$p.WaitForExit(120000)){throw 'XInput test timeout'}
    if($p.ExitCode -ne 0){throw 'XInput native test failed'}
    if($adapter -and (!$adapter.WaitForExit(5000) -or $adapter.ExitCode -ne 0)){throw 'Controller filter adapter failed'}
   } finally {foreach($proc in @($p,$adapter)){if($proc -and !$proc.HasExited){Stop-Process -Id $proc.Id -Force}}}
  }
  Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$id) $local -FromSession $s -Recurse
  Write-Output ('Measured '+$id)
 }
} finally {Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$campaign+'*') $local -FromSession $s -Recurse -Force -ErrorAction SilentlyContinue;Remove-PSSession $s}
