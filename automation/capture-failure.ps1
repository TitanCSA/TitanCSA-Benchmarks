. (Join-Path $PSScriptRoot 'Lab.ps1')
$id=[guid]::NewGuid().ToString('N');$local=Join-Path $script:BenchmarkRoot ('.local/crashes/'+$id);New-Item -ItemType Directory $local -Force|Out-Null
$s=New-BenchmarkSession
try{
 Invoke-Command -Session $s -ScriptBlock {
  Get-WinEvent -FilterHashtable @{LogName='System';Id=1001,41,1074} -MaxEvents 8 -ErrorAction SilentlyContinue|Select TimeCreated,RecordId,Id,ProviderName,Message|ConvertTo-Json -Depth 4
 }|Set-Content (Join-Path $local 'events-private.json') -Encoding UTF8
 $dumps=Invoke-Command -Session $s -ScriptBlock {Get-ChildItem C:\Windows\Minidump -File -ErrorAction SilentlyContinue|Sort-Object LastWriteTime -Descending|Select-Object -First 1 -ExpandProperty FullName}
 if($dumps){Copy-Item -LiteralPath $dumps -Destination (Join-Path $local 'minidump.dmp') -FromSession $s}
}finally{Remove-PSSession $s}
@{directory=$local;captured_utc=[DateTime]::UtcNow.ToString('o');dump_public=$false}|ConvertTo-Json|Set-Content (Join-Path $script:BenchmarkRoot '.local/latest-failure.json') -Encoding ASCII
Write-Output 'Owned guest failure evidence captured privately; no dump published.'
