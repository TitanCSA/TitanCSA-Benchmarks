param([ValidateSet('mouse','keyboard')][string]$Profile='mouse',[ValidateSet('baseline','Keyboard-Mouse','Combined')][string]$Filter='baseline',[ValidateSet('forward','modify','block')][string]$Operation='forward',[int]$Repetitions=3,[int]$Samples=1000,[int]$Rate=125)
. (Join-Path $PSScriptRoot 'Lab.ps1')
if($Profile -eq 'keyboard' -and $Operation -ne 'forward'){throw 'Keyboard remap/block measurement not implemented'}
if($Filter -eq 'baseline' -and $Operation -ne 'forward'){throw 'No filter for requested operation'}
$s=New-BenchmarkSession;$campaign=[guid]::NewGuid().ToString('N');$local=Join-Path $script:BenchmarkRoot ('data/raw/'+$campaign);New-Item -ItemType Directory $local|Out-Null
try{
 $bins=@('TitanCSA-Benchmark-InputGenerator.exe','TitanCSA-Benchmark-RawReceiver.exe');if($Filter -ne 'baseline'){$bins+='TitanCSA-Benchmark-Intercept-'+$Filter+'.exe'}
 foreach($n in $bins){Copy-Item (Join-Path $script:BenchmarkRoot ('build/Release/'+$n)) ('C:\TitanCSABenchmarkLab\bin\'+$n) -ToSession $s}
 for($rep=0;$rep -lt $Repetitions;$rep++){
  $id=$campaign+'-'+$rep+'-'+$Profile+'-'+$Filter+'-'+$Operation
  $cfg=@{samples=$Samples;warmup=100;requested_hz=$Rate;seed=42137;profile=$Profile;filter=$Filter;operation=$Operation;repetition=$rep;run_id=$id;utc=[DateTime]::UtcNow.ToString('o');category='raw-input';version='Vdevice 1.0.5.0';measurement='Vdevice Send_Input entry to independent Raw Input delivery';closed_loop=($Profile -eq 'mouse')}
$cfg.build_identity=Get-BenchmarkBuildIdentity
  $p=Join-Path $script:BenchmarkRoot '.local/raw-scenario.json';$cfg|ConvertTo-Json -Depth 10|Set-Content $p -Encoding ASCII;Copy-Item $p C:\TitanCSABenchmarkLab\scenario.json -ToSession $s
  Invoke-Command -Session $s -ArgumentList $id,$Filter,$Profile -ScriptBlock {
   param($id,$filter,$profile)
   $ErrorActionPreference='Stop';$out='C:\TitanCSABenchmarkLab\results\'+$id;$adapter=$null
   $gen=Start-Process C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-InputGenerator.exe -ArgumentList 'C:\TitanCSABenchmarkLab\scenario.json',$out -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-generator.stderr');$null=$gen.Handle
   $task='TitanCSA-Benchmark-RawReceiver'
   try{
    $end=(Get-Date).AddSeconds(30);while(!(Test-Path (Join-Path $out 'run.json')) -and !$gen.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 50}
    if(!(Test-Path (Join-Path $out 'run.json'))){throw 'Virtual input enumeration failed'}
    if($filter -ne 'baseline'){
     $adapter=Start-Process ('C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-Intercept-'+$filter+'.exe') -ArgumentList $out -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-adapter.stderr');$null=$adapter.Handle
     $end=(Get-Date).AddSeconds(20);while(!(Test-Path (Join-Path $out 'adapter-ready.json')) -and !$adapter.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 50}
     if(!(Test-Path (Join-Path $out 'adapter-ready.json'))){throw 'Filter adapter did not become ready'}
    }
    $devices=Get-PnpDevice -PresentOnly|Where-Object InstanceId -match $(if($profile -eq 'mouse'){'VID_FFFF&PID_B752'}else{'VID_FFFF&PID_B753'})
    foreach($d in $devices){pnputil /enum-devices /instanceid $d.InstanceId /stack /services /relations /drivers|Out-File (Join-Path $out 'pnp-stack.txt') -Append -Encoding UTF8}
    $account=(Get-CimInstance Win32_ComputerSystem).UserName;if(!$account){throw 'No interactive benchmark desktop'}
    $action=New-ScheduledTaskAction -Execute C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-RawReceiver.exe -Argument $out
    $principal=New-ScheduledTaskPrincipal -UserId $account -LogonType Interactive -RunLevel Highest
    Register-ScheduledTask -TaskName $task -Action $action -Principal $principal -Force|Out-Null;Start-ScheduledTask -TaskName $task
    if(!$gen.WaitForExit(120000)){throw 'Generator deadline'}
    if($gen.ExitCode -ne 0){throw 'Generator failed'}
    if($adapter){if(!$adapter.WaitForExit(10000) -or $adapter.ExitCode -ne 0){throw 'Filter adapter failed'}}
    if(!(Test-Path (Join-Path $out 'receiver-done.json'))){throw 'Independent receiver incomplete'}
    @{status='completed';generator_exit=$gen.ExitCode;receiver_task_exit=(Get-ScheduledTaskInfo $task).LastTaskResult}|ConvertTo-Json|Set-Content (Join-Path $out 'orchestration.json') -Encoding ASCII
   }finally{Stop-ScheduledTask $task -ErrorAction SilentlyContinue;Unregister-ScheduledTask $task -Confirm:$false -ErrorAction SilentlyContinue;foreach($proc in @($gen,$adapter)){if($proc -and !$proc.HasExited){Stop-Process -Id $proc.Id -Force}}}
  }
  Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$id) $local -FromSession $s -Recurse;Write-Output ('Measured '+$id)
 }
}finally{Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$campaign+'*') $local -FromSession $s -Recurse -Force -ErrorAction SilentlyContinue;Remove-PSSession $s}
