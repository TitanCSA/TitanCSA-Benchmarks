# Initial vendor-HID/XUSB comparison only. Other families have separate runners.
# Do not dispatch repeated controller teardown while WDF-001 remains unresolved.
. (Join-Path $PSScriptRoot 'Lab.ps1')
$lab=Get-BenchmarkLab
if(!(Get-VMSnapshot -VM (Get-VM -Id $lab.vm_id) -Name 'Clean-Benchmark-Baseline' -ErrorAction SilentlyContinue)){throw 'A reviewed clean lab baseline is required'}
& (Join-Path $PSScriptRoot 'reset-vm.ps1')
& (Join-Path $PSScriptRoot 'install-titancsa.ps1')
& (Join-Path $PSScriptRoot 'run-virtual-device-tests.ps1')
& (Join-Path $PSScriptRoot 'run-gamepad-tests.ps1') -Backend vdevice
& (Join-Path $PSScriptRoot 'reset-vm.ps1')
& (Join-Path $PSScriptRoot 'install-competitors.ps1')
& (Join-Path $PSScriptRoot 'run-gamepad-tests.ps1') -Backend vigem
Write-Output 'Campaign collected. Validate and review results before publication.'
