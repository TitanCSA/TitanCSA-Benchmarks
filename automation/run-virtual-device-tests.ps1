param([int[]]$Rates=@(125,1000,10000),[int]$Repetitions=5,[int]$Samples=1000,[ValidateSet('latency','stability','instrumented')][string]$Purpose='latency')
. (Join-Path $PSScriptRoot 'Lab.ps1')
if($Repetitions -lt 1 -or $Repetitions -gt 20 -or $Samples -lt 1 -or $Samples -gt 100000){throw 'Invalid campaign bounds'}
$s=New-BenchmarkSession
$campaign=[guid]::NewGuid().ToString('N')
$local=Join-Path $script:BenchmarkRoot ('data/raw/'+$campaign)
New-Item -ItemType Directory $local|Out-Null
try {
 foreach($n in 'TitanCSA-Benchmark-InputGenerator.exe','TitanCSA-Benchmark-HidReceiver.exe'){
  Copy-Item (Join-Path $script:BenchmarkRoot ('build/Release/'+$n)) ('C:\TitanCSABenchmarkLab\bin\'+$n) -ToSession $s
 }
 # Alternate rate order deterministically between independent repetitions.
 for($rep=0;$rep -lt $Repetitions;$rep++){
  $order=if($rep%2){@($Rates|Sort-Object -Descending)}else{$Rates}
  foreach($hz in $order){
   $id=$campaign+'-'+$rep+'-'+$hz
   $cfg=@{samples=$Samples;warmup=100;requested_hz=$hz;seed=42137;repetition=$rep;run_id=$id;project='TitanCSA/Vdevice';category='virtual-vendor-hid';version='1.0.5.0';utc=[DateTime]::UtcNow.ToString('o')}
   $cfg.purpose=$Purpose
$cfg.build_identity=Get-BenchmarkBuildIdentity
   $source=Join-Path $script:BenchmarkRoot ('.local/'+$id+'.json');$cfg|ConvertTo-Json -Depth 10|Set-Content $source -Encoding ASCII
   Copy-Item $source C:\TitanCSABenchmarkLab\scenario.json -ToSession $s
   Invoke-Command -Session $s -ArgumentList $id -ScriptBlock {
    param($id)
    $ErrorActionPreference='Stop';$out='C:\TitanCSABenchmarkLab\results\'+$id
    $gen=Start-Process C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-InputGenerator.exe -ArgumentList @('C:\TitanCSABenchmarkLab\scenario.json',$out) -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-generator.stderr')
    $null=$gen.Handle
    $end=(Get-Date).AddSeconds(30);while(!(Test-Path (Join-Path $out 'run.json')) -and !$gen.HasExited -and (Get-Date) -lt $end){Start-Sleep -Milliseconds 50}
    if(Test-Path (Join-Path $out 'run.json')){
     $devices=Get-PnpDevice -PresentOnly|Where-Object InstanceId -match 'VID_FFFF&PID_B751'
     foreach($d in $devices){pnputil /enum-devices /instanceid $d.InstanceId /stack /services /relations /drivers | Out-File (Join-Path $out 'pnp-stack.txt') -Append -Encoding UTF8}
    }
    $receiver=Start-Process C:\TitanCSABenchmarkLab\bin\TitanCSA-Benchmark-HidReceiver.exe -ArgumentList @($out) -WindowStyle Hidden -PassThru -RedirectStandardError ($out+'-receiver.stderr')
    $null=$receiver.Handle
    try{
     $runConfig=Get-Content (Join-Path $out 'run.json') -Raw|ConvertFrom-Json
     $timeout=[Math]::Min(720000,[Math]::Max(120000,[int][Math]::Ceiling(($runConfig.samples+$runConfig.warmup)*1000/$runConfig.requested_hz)+60000))
     if(!$gen.WaitForExit($timeout)){throw 'Generator timeout'}
     if(!$receiver.WaitForExit(15000)){throw 'Receiver timeout'}
     if($gen.ExitCode -ne 0 -or $receiver.ExitCode -ne 0){throw "Native run failed: generator=$($gen.ExitCode), receiver=$($receiver.ExitCode)"}
     @{generator_exit=$gen.ExitCode;receiver_exit=$receiver.ExitCode;status='completed'}|ConvertTo-Json|Set-Content (Join-Path $out 'orchestration.json') -Encoding ASCII
    } finally {foreach($p in $gen,$receiver){if(!$p.HasExited){Stop-Process -Id $p.Id -Force}}}
   }
   Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$id) $local -FromSession $s -Recurse
   Write-Output ('Measured '+$id)
  }
 }
} finally {
 # Even failed runs retain all available data and diagnostics locally.
 Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$campaign+'*') $local -FromSession $s -Recurse -Force -ErrorAction SilentlyContinue
 Remove-PSSession $s
}
