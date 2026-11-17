. (Join-Path $PSScriptRoot 'Lab.ps1')
$file='vJoySetup_v2.2.2.0_Win10_Win11.exe';$source=Join-Path $script:BenchmarkRoot ('.local/downloads/'+$file)
$artifact=(Get-Content (Join-Path $script:BenchmarkRoot 'reports/artifacts.json') -Raw|ConvertFrom-Json)|Where-Object name -eq $file
if((Get-FileHash $source).Hash.ToLowerInvariant() -ne $artifact.sha256){throw 'vJoy artifact changed'}
$sig=Get-AuthenticodeSignature $source;if($sig.Status -ne 'Valid' -or $sig.SignerCertificate.Subject -notmatch 'Brunner'){throw 'Unexpected vJoy installer signature'}
$s=New-BenchmarkSession
try{Copy-Item $source ('C:\TitanCSABenchmarkLab\bin\'+$file) -ToSession $s
 Invoke-Command -Session $s -ArgumentList $file -ScriptBlock {
  param($file)
  if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'}
  if(Get-Service Vdevice,Interceptor,InterceptorKeyboardMouse,InterceptorGamepadController,ViGEmBus -ErrorAction SilentlyContinue){throw 'Restore corrected clean baseline before vJoy'}
  $p=Start-Process (Join-Path C:\TitanCSABenchmarkLab\bin $file) -ArgumentList '/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-','/LOG=C:\TitanCSABenchmarkLab\vjoy-install.log' -WindowStyle Hidden -PassThru;$null=$p.Handle
  if(!$p.WaitForExit(120000)){Stop-Process -Id $p.Id -Force;throw 'vJoy installer deadline'}
  if($p.ExitCode -notin 0,3010){throw ('vJoy install exit '+$p.ExitCode)}
  $d=Get-CimInstance Win32_SystemDriver -Filter "Name='vjoy'";if(!$d){throw 'vJoy driver missing'}
  $path=$d.PathName.Replace('\SystemRoot\',($env:windir+'\')).Replace('\??\','');$sig=Get-AuthenticodeSignature $path;if($sig.Status -ne 'Valid'){throw 'vJoy SYS signature invalid'}
  @{name=$d.Name;state=$d.State;sha256=(Get-FileHash $path).Hash;signature=$sig.Status.ToString();signer=$sig.SignerCertificate.Subject}|ConvertTo-Json
 }|Tee-Object -FilePath (Join-Path $script:BenchmarkRoot 'reports/install-vjoy.json')
}finally{Copy-Item C:\TitanCSABenchmarkLab\vjoy-install.log (Join-Path $script:BenchmarkRoot '.local/vjoy-install.log') -FromSession $s -ErrorAction SilentlyContinue;Remove-PSSession $s}
