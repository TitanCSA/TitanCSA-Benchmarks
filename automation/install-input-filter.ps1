param([ValidateSet('Keyboard-Mouse','Combined','Gamepad-Controller')][string]$Edition='Keyboard-Mouse')
. (Join-Path $PSScriptRoot 'Lab.ps1')
$name=if($Edition -eq 'Combined'){'Interceptor'}else{'Interceptor-'+$Edition}
$source=Join-Path $script:BenchmarkRoot ('.local/downloads/'+$name+'-SetupConsole.exe')
$artifact=(Get-Content (Join-Path $script:BenchmarkRoot 'reports/artifacts.json') -Raw|ConvertFrom-Json)|Where-Object name -eq ($name+'-SetupConsole.exe')
if((Get-FileHash $source).Hash.ToLowerInvariant() -ne $artifact.sha256){throw 'Installer digest mismatch'}
$s=New-BenchmarkSession
try{Copy-Item $source C:\TitanCSABenchmarkLab\bin\FilterSetup.exe -ToSession $s
 Invoke-Command -Session $s -ScriptBlock {
  if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'}
  & C:\TitanCSABenchmarkLab\bin\FilterSetup.exe /install
  if($LASTEXITCODE -notin 0,3010){throw ('Filter installer exit '+$LASTEXITCODE)}
 }|Tee-Object -FilePath (Join-Path $script:BenchmarkRoot ('reports/install-'+$name+'.txt'))
}finally{Remove-PSSession $s}
