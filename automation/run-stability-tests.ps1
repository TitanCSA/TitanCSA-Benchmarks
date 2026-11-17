param([ValidateRange(30,300)][int]$Seconds=300)
. (Join-Path $PSScriptRoot 'Lab.ps1')
$id=[guid]::NewGuid().ToString('N');$local=Join-Path $script:BenchmarkRoot ('data/stability/'+$id);New-Item -ItemType Directory $local -Force|Out-Null
$s=New-BenchmarkSession
try{
 Invoke-Command -Session $s -ArgumentList $id,$Seconds -ScriptBlock {
  param($id,$seconds)
  $dir='C:\TitanCSABenchmarkLab\stability\'+$id;New-Item -ItemType Directory -Path $dir -Force|Out-Null
  @{boot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToFileTimeUtc();utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content (Join-Path $dir 'before.json') -Encoding ASCII
  $global:BenchmarkMemorySampler=Start-Job -ArgumentList $dir,($seconds+90) -ScriptBlock {
   param($dir,$duration)
   $end=(Get-Date).AddSeconds($duration)
   while((Get-Date) -lt $end -and !(Test-Path (Join-Path $dir 'stop'))){
    $m=Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
    [pscustomobject]@{utc=[DateTime]::UtcNow.ToString('o');nonpaged_bytes=$m.PoolNonpagedBytes;paged_bytes=$m.PoolPagedBytes;available_mib=$m.AvailableMBytes}|Export-Csv (Join-Path $dir 'memory.csv') -NoTypeInformation -Append -Encoding ASCII
    Start-Sleep -Seconds 10
   }
  }
 }
 & (Join-Path $PSScriptRoot 'run-virtual-device-tests.ps1') -Rates @(125) -Repetitions 1 -Samples ($Seconds*125) -Purpose stability
 Invoke-Command -Session $s -ArgumentList $id -ScriptBlock {
  param($id)
  $dir='C:\TitanCSABenchmarkLab\stability\'+$id;Set-Content (Join-Path $dir 'stop') stop;Wait-Job $global:BenchmarkMemorySampler -Timeout 15|Out-Null;Stop-Job $global:BenchmarkMemorySampler -ErrorAction SilentlyContinue;Remove-Job $global:BenchmarkMemorySampler -Force
  Start-Sleep -Seconds 3
  @{boot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToFileTimeUtc();utc=[DateTime]::UtcNow.ToString('o');present_test_nodes=@(Get-PnpDevice -PresentOnly|Where-Object InstanceId -match 'VID_FFFF&PID_B751').Count;remaining_owned_native_processes=@(Get-Process 'TitanCSA-Benchmark-*' -ErrorAction SilentlyContinue).Count}|ConvertTo-Json|Set-Content (Join-Path $dir 'after.json') -Encoding ASCII
 }
}finally{
 Copy-Item ('C:\TitanCSABenchmarkLab\stability\'+$id+'\*') $local -FromSession $s -Recurse -ErrorAction SilentlyContinue
 Remove-PSSession $s
}
