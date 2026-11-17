param([string]$Checkpoint='Clean-Benchmark-Baseline')
. (Join-Path $PSScriptRoot 'Lab.ps1')
$r=Get-BenchmarkLab
$snapshot=Get-VMSnapshot -VM (Get-VM -Id $r.vm_id) -Name $Checkpoint -ErrorAction Stop
Restore-VMSnapshot -VMSnapshot $snapshot -Confirm:$false
if((Get-VM -Id $r.vm_id).State -eq 'Off'){Start-VM -VM (Get-VM -Id $r.vm_id)|Out-Null}
