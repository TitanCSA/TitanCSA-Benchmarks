param([ValidateSet('Vdevice')][string]$Project='Vdevice')
. (Join-Path $PSScriptRoot 'Lab.ps1')
$items=Get-Content (Join-Path $script:BenchmarkRoot 'reports/artifacts.json') -Raw|ConvertFrom-Json
$item=$items|Where-Object name -eq 'VdeviceSetupConsole.exe'
$source=Join-Path $script:BenchmarkRoot '.local/downloads/VdeviceSetupConsole.exe'
if((Get-FileHash $source).Hash.ToLowerInvariant() -ne $item.sha256){throw 'Artifact digest mismatch'}
$s=New-BenchmarkSession
try {
 Copy-Item $source C:\TitanCSABenchmarkLab\bin\VdeviceSetupConsole.exe -ToSession $s
 Invoke-Command -Session $s -ScriptBlock {
  if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'}
  & C:\TitanCSABenchmarkLab\bin\VdeviceSetupConsole.exe /install
  if($LASTEXITCODE -notin 0,3010){throw 'Driver installation failed'}
  $driver=Get-CimInstance Win32_SystemDriver -Filter "Name='Vdevice'"
  if($driver.State -ne 'Running'){throw 'Driver did not load'}
  $path=$driver.PathName.Replace('\SystemRoot\',($env:windir+'\')).Replace('\??\','')
  $sig=Get-AuthenticodeSignature -LiteralPath $path
  if($sig.Status -ne 'Valid' -or $sig.SignerCertificate.Subject -notmatch 'Microsoft Windows Hardware Compatibility Publisher'){throw 'Expected Microsoft driver signature'}
  @{name=$driver.Name;state=$driver.State;sha256=(Get-FileHash $path).Hash;version=(Get-Item $path).VersionInfo.FileVersion;signature=$sig.Status.ToString();signer=$sig.SignerCertificate.Subject}|ConvertTo-Json
 } | Tee-Object -FilePath (Join-Path $script:BenchmarkRoot '.local/install-vdevice.log')
} finally {Remove-PSSession $s}
