param([string]$ParentDisk,[string]$CredentialFile,[Guid]$ParentVmId)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$private=Join-Path $root '.local'
$recordPath=Join-Path $private 'lab.json'
if(Test-Path $recordPath){throw 'Lab already recorded; inspect its identity before reusing it.'}
if(Get-VM -Name 'TitanCSA-Benchmark-Lab' -ErrorAction SilentlyContinue){throw 'An unowned VM already has the requested name.'}
$parentVm=Get-VM -Id $ParentVmId
if($parentVm.State -ne 'Off'){throw 'Parent VM must already be off. This script never stops another VM.'}
$disk=Get-VHD -Path $ParentDisk
if($disk.Attached){throw 'Parent disk is attached'}
if(!(Test-Path -LiteralPath $CredentialFile)){throw 'Guest credential unavailable'}
$folder=Join-Path $private ('VM-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $folder|Out-Null
$child=Join-Path $folder 'system.vhdx'
New-VHD -Path $child -ParentPath $ParentDisk -Differencing|Out-Null
$vm=New-VM -Name 'TitanCSA-Benchmark-Lab' -Generation 2 -MemoryStartupBytes 3GB -Path $folder -VHDPath $child -SwitchName 'Default Switch'
Set-VM -VM $vm -ProcessorCount 2 -AutomaticCheckpointsEnabled $false -AutomaticStartAction Nothing -AutomaticStopAction ShutDown
Set-VMMemory -VM $vm -DynamicMemoryEnabled $false
Set-VMFirmware -VM $vm -EnableSecureBoot On -SecureBootTemplate MicrosoftWindows
@{vm_id=[string]$vm.Id;name=$vm.Name;credential_file=$CredentialFile;folder=$folder;parent=$ParentDisk;purpose='TitanCSA benchmarks only';created_utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content $recordPath -Encoding UTF8
Start-VM -VM $vm|Out-Null
Write-Output ('Dedicated benchmark VM created: '+$vm.Id)
