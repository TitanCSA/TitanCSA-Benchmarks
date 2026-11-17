. (Join-Path $PSScriptRoot 'Lab.ps1')
$s=New-BenchmarkSession
try {
 $folders=Invoke-Command -Session $s -ScriptBlock {Get-ChildItem C:\TitanCSABenchmarkLab\results -Directory|Select-Object -ExpandProperty Name}
 foreach($name in $folders){
  if($name -notmatch '^[a-f0-9]{32}-'){throw 'Unexpected lab result name'}
  $campaign=$name.Substring(0,32);$base=Join-Path $script:BenchmarkRoot ('data/raw/'+$campaign);New-Item -ItemType Directory -Force $base|Out-Null
  $target=Join-Path $base $name
  if(!(Test-Path $target)){Copy-Item ('C:\TitanCSABenchmarkLab\results\'+$name) $base -FromSession $s -Recurse}
 }
}finally{Remove-PSSession $s}
Write-Output 'Previously uncollected result directories copied without overwriting stored runs.'
