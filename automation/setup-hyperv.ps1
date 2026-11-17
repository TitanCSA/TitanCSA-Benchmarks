$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if(!(Get-Command Get-VM -ErrorAction SilentlyContinue)){throw 'Hyper-V PowerShell tools are unavailable'}
$identity=[Security.Principal.WindowsIdentity]::GetCurrent()
$admin=([Security.Principal.WindowsPrincipal]::new($identity)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
@{captured_utc=[DateTime]::UtcNow.ToString('o');administrator=$admin;hyperv_tools=$true;powershell=$PSVersionTable.PSVersion.ToString();existing_vm_count=@(Get-VM).Count;free_ram_kib=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory;vm_names_changed=$false;host_drivers_changed=$false}|ConvertTo-Json|Set-Content (Join-Path $root 'reports/hyperv-detection.json') -Encoding ASCII
Write-Output 'Hyper-V detected; existing VM names and disks unchanged.'
