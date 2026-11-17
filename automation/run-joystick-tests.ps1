param([ValidateSet('vdevice','vjoy')][string]$Backend,[int]$Repetitions=3,[int]$Samples=1000)
. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession;$campaign=[guid]::NewGuid().ToString('N');$local=Join-Path $script:BenchmarkRoot ('data/raw/'+$campaign);New-Item -ItemType Directory $local|Out-Null
try{
 foreach($n in 'TitanCSA-Benchmark-Joystick.exe','TitanCSA-Benchmark-JoystickReceiver.exe'){Copy-Item (Join-Path $script:BenchmarkRoot ('build/Release/'+$n)) ('C:\TitanCSABenchmarkLab\bin\'+$n) -ToSession $s}
 if($Backend -eq 'vjoy'){Copy-Item (Join-Path $script:BenchmarkRoot '.local/vjoy-sdk/SDK/lib/x64/vJoyInterface.dll') C:\TitanCSABenchmarkLab\bin\vJoyInterface.dll -ToSession $s}
 for($rep=0;$rep -lt $Repetitions;$rep++){
  $id=$campaign+'-'+$rep+'-'+$Backend
  $cfg=@{backend=$Backend;samples=$Samples;warmup=100;seed=42137;repetition=$rep;run_id=$id;utc=[DateTime]::UtcNow.ToString('o');profile='generic-joystick-xy-eight-buttons';category='virtual-joystick';device_origin='virtual';version=$(if($Backend -eq 'vjoy'){'2.2.2.0'}else{'1.0.5.0'});collect_stack=$true;build_identity=(Get-BenchmarkBuildIdentity)}
  $p=Join-Path $script:BenchmarkRoot '.local/joystick-scenario.json';$cfg|ConvertTo-Json -Depth 12|Set-Content $p -Encoding ASCII;Copy-Item $p C:\TitanCSABenchmarkLab\joystick-scenario.json -ToSession $s
  Invoke-Command -Session $s -ArgumentList $id -ScriptBlock {
   param($id)
   $ErrorActionPreference='Stop';$out='C:\TitanCSABenchmarkLab\results\'+$id
   $p=Start-Process C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-Joystick.exe -ArgumentList 'C:\TitanCSABenchmarkLab\joystick-scenario.json',$out,'C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-JoystickReceiver.exe' -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-joystick.stderr');$null=$p.Handle
   try{
    $end=(Get-Date).AddSeconds(30);while(!(Test-Path (Join-Path $out 'joystick-run.json')) -and !$p.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 100}
    if(!(Test-Path (Join-Path $out 'joystick-run.json'))){throw 'Joystick creation failed; inspect native diagnostics'}
    $devices=Get-PnpDevice -PresentOnly|Where-Object InstanceId -match '(VID_FFFF&PID_B754|VID_1234&PID_BEAD|ROOT\\VJOY)'
    foreach($d in $devices){pnputil /enum-devices /instanceid $d.InstanceId /stack /services /relations /drivers|Out-File (Join-Path $out 'pnp-stack.txt') -Append -Encoding UTF8}
    '{"captured":true}'|Set-Content (Join-Path $out 'stack-captured.json') -Encoding ASCII
    if(!$p.WaitForExit(120000)){throw 'Joystick test timeout'}
    if($p.ExitCode -ne 0){throw 'Joystick test failed; inspect native diagnostics'}
   }finally{if(!$p.HasExited){Stop-Process -Id $p.Id -Force}}
  }
  Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$id) $local -FromSession $s -Recurse;Write-Output ('Measured '+$id)
 }
}finally{Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$campaign+'*') $local -FromSession $s -Recurse -Force -ErrorAction SilentlyContinue;Remove-PSSession $s}
