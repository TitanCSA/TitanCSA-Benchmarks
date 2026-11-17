. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession
try {
 Copy-Item (Join-Path $script:BenchmarkRoot 'build/Release/Vdevice-Upstream-LiveTests.exe') C:\TitanCSABenchmarkLab\bin\Vdevice-Upstream-LiveTests.exe -ToSession $s
 Invoke-Command -Session $s -ScriptBlock {
  if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'}
  $p=Start-Process C:\TitanCSABenchmarkLab\bin\Vdevice-Upstream-LiveTests.exe -ArgumentList '--vm-live' -WindowStyle Hidden -PassThru -RedirectStandardOutput C:\TitanCSABenchmarkLab\profile-validation.txt -RedirectStandardError C:\TitanCSABenchmarkLab\profile-validation-errors.txt;$null=$p.Handle
  if(!$p.WaitForExit(120000)){Stop-Process -Id $p.Id -Force;throw 'Profile validation deadline'}
  @{exit_code=$p.ExitCode;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content C:\TitanCSABenchmarkLab\profile-validation.json -Encoding ASCII
  if($p.ExitCode -ne 0){throw 'At least one upstream profile validation failed; see retained logs'}
 } 
}finally{
 foreach($name in 'profile-validation.txt','profile-validation-errors.txt','profile-validation.json'){Copy-Item ('C:\TitanCSABenchmarkLab\'+$name) (Join-Path $script:BenchmarkRoot ('reports/'+$name)) -FromSession $s -ErrorAction SilentlyContinue}
 Remove-PSSession $s
}
