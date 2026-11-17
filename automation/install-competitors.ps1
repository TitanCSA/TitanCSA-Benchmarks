param([ValidateSet('ViGEmBus')][string]$Project='ViGEmBus')
. (Join-Path $PSScriptRoot 'Lab.ps1')
$file='ViGEmBus_1.22.0_x64_x86_arm64.exe'
$item=(Get-Content (Join-Path $script:BenchmarkRoot 'reports/artifacts.json') -Raw|ConvertFrom-Json)|Where-Object name -eq $file
$source=Join-Path $script:BenchmarkRoot ('.local/downloads/'+$file)
if((Get-FileHash $source).Hash.ToLowerInvariant() -ne $item.sha256){throw 'Artifact mismatch'}
$signature=Get-AuthenticodeSignature $source
if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Nefarius'){throw 'Unexpected installer signature'}
$s=New-BenchmarkSession
try {
 Copy-Item $source ('C:\TitanCSABenchmarkLab\bin\'+$file) -ToSession $s
 Invoke-Command -Session $s -ArgumentList $file -ScriptBlock {
  param($file)
  if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'}
  if(Get-Service Vdevice -ErrorAction SilentlyContinue){throw 'Restore clean baseline before installing competitor'}
  $p=Start-Process (Join-Path C:\TitanCSABenchmarkLab\bin $file) -ArgumentList '/quiet','/norestart' -WindowStyle Hidden -PassThru;$null=$p.Handle
  if(!$p.WaitForExit(120000)){Stop-Process -Id $p.Id -Force;throw 'Installer timeout'}
  if($p.ExitCode -notin 0,3010){throw ('Competitor installer failed: '+$p.ExitCode)}
  $d=Get-CimInstance Win32_SystemDriver -Filter "Name='ViGEmBus'";if($d.State -ne 'Running'){throw 'ViGEmBus did not load'}
  $path=$d.PathName.Replace('\SystemRoot\',($env:windir+'\')).Replace('\??\','');$sig=Get-AuthenticodeSignature $path
  if($sig.Status -ne 'Valid'){throw 'ViGEmBus signature invalid'}
  @{name=$d.Name;state=$d.State;sha256=(Get-FileHash $path).Hash;signature=$sig.Status.ToString();signer=$sig.SignerCertificate.Subject}|ConvertTo-Json
 }|Tee-Object -FilePath (Join-Path $script:BenchmarkRoot 'reports/install-vigem.json')
} finally {Remove-PSSession $s}
