# Run once after provisioning a genuinely clean owned guest, before checkpointing.
. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession
try {
 Invoke-Command -Session $s -ScriptBlock {
  $ErrorActionPreference='Stop'
  $existing=@(Get-Service Filter,Vdevice,Interceptor,InterceptorKeyboardMouse,InterceptorGamepadController,ViGEmBus,vJoy -ErrorAction SilentlyContinue)
  if($existing){throw 'Input drivers already installed; use a reviewed clean guest before baseline creation. No driver was removed.'}
  $drivers=@(Get-WindowsDriver -Online|Where-Object { [IO.Path]::GetFileName($_.OriginalFileName) -match '^(filter|filterkeyboard|filtermouse|filterx360)\.inf$' })
  if($drivers){throw 'Inherited Filter INF packages detected; do not label this image as a clean baseline.'}
  foreach($dir in 'C:\TitanCSABenchmarkLab','C:\TitanCSABenchmarkLab\bin','C:\TitanCSABenchmarkLab\results','C:\TitanCSABenchmarkLab\stability'){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
  @{purpose='TitanCSA benchmarks only';inputs='Generated laboratory fixtures only';created_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content C:\TitanCSABenchmarkLab\authorized-lab.json -Encoding ASCII
 }
}finally{Remove-PSSession $s}
Write-Output 'Owned clean guest initialized; create the reviewed baseline checkpoint next.'
