$ErrorActionPreference='Stop'
$script:BenchmarkRoot=Split-Path $PSScriptRoot -Parent
function Get-BenchmarkLab {
 $r=Get-Content (Join-Path $script:BenchmarkRoot '.local/lab.json') -Raw|ConvertFrom-Json
 $vm=Get-VM -Id $r.vm_id
 if($vm.Name -ne 'TitanCSA-Benchmark-Lab' -or $r.purpose -ne 'TitanCSA benchmarks only'){throw 'Lab ownership mismatch'}
 return $r
}
function New-BenchmarkSession {
 $r=Get-BenchmarkLab
 $credential=Import-Clixml -LiteralPath $r.credential_file
 for($attempt=0;$attempt -lt 5;$attempt++){
  try{return (New-PSSession -VMId $r.vm_id -Credential $credential -ErrorAction Stop)}
  catch{if($attempt -eq 4){throw};Start-Sleep -Seconds 2}
 }
}
function Get-BenchmarkBuildIdentity {
 $hashes=@{}
 Get-ChildItem (Join-Path $script:BenchmarkRoot 'build/Release') -Filter 'TitanCSA-Benchmark-*.exe'|ForEach-Object{$hashes[$_.Name]=(Get-FileHash $_.FullName).Hash.ToLowerInvariant()}
 $audit=Get-Content (Join-Path $script:BenchmarkRoot 'reports/repository-audit.json') -Raw|ConvertFrom-Json
 $sourceHashes=@{}
 Get-ChildItem (Join-Path $script:BenchmarkRoot 'benchmarks') -Recurse -File|Where-Object Extension -in '.cpp','.h'|ForEach-Object{$sourceHashes[$_.FullName.Substring($script:BenchmarkRoot.Length+1).Replace('\','/')]=(Get-FileHash $_.FullName).Hash.ToLowerInvariant()}
 $buildManifest=Join-Path $script:BenchmarkRoot 'build/build-identity.json'
 $buildRecord=if(Test-Path $buildManifest){Get-Content $buildManifest -Raw|ConvertFrom-Json}else{$null}
 return @{executables=$hashes;source_files=$sourceHashes;source_snapshot_kind='Files observed at run start; build attestation separate when available';build_record=$buildRecord;source_commits=@($audit.repositories|Select-Object requested,commit);baseline='See per-run PnP evidence and clean-baseline-v2.txt';host_cpu_load_percent=(Get-CimInstance Win32_Processor).LoadPercentage;host_free_ram_kib=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory}
}
