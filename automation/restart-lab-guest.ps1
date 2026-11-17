. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession
try{
 $boot=Invoke-Command -Session $s -ScriptBlock {(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToFileTimeUtc()}
 Invoke-Command -Session $s -ScriptBlock {if(!(Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)){throw 'Lab marker missing'};Restart-Computer -Force}
}finally{Remove-PSSession $s}
Start-Sleep -Seconds 15
for($attempt=0;$attempt -lt 12;$attempt++){
 $s=$null
 try{
  $s=New-BenchmarkSession
  $ready=Invoke-Command -Session $s -ArgumentList $boot -ScriptBlock {
   param($oldBoot)
   $os=Get-CimInstance Win32_OperatingSystem
   $os.LastBootUpTime.ToFileTimeUtc() -ne $oldBoot -and ((Get-Date)-$os.LastBootUpTime).TotalSeconds -ge 12 -and (Test-Path C:\TitanCSABenchmarkLab\authorized-lab.json)
  }
  if($ready){Write-Output 'Owned guest restarted and ready.';return}
 }finally{if($s){Remove-PSSession $s}}
 Start-Sleep -Seconds 2
}
throw 'Owned guest did not finish restart within the readiness window'
