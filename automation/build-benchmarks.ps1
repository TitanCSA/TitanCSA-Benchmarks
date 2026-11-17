param([string]$Configuration='Release')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$inputs=@(Get-ChildItem (Join-Path $root 'benchmarks') -Recurse -File|Where-Object Extension -in '.cpp','.h')+@(Get-Item (Join-Path $root 'CMakeLists.txt'))
$before=@{};foreach($p in $inputs){$before[$p.FullName]=(Get-FileHash $p.FullName).Hash}
cmake -S $root -B (Join-Path $root 'build') -A x64
if($LASTEXITCODE -ne 0){throw 'CMake configuration failed'}
cmake --build (Join-Path $root 'build') --config $Configuration
if($LASTEXITCODE -ne 0){throw 'Native compilation failed'}
$hashes=@{};foreach($p in $inputs){if((Get-FileHash $p.FullName).Hash -ne $before[$p.FullName]){throw 'Source changed during compilation'};$hashes[$p.FullName.Substring($root.Length+1).Replace('\','/')]=$before[$p.FullName].ToLowerInvariant()}
$executables=@{};Get-ChildItem (Join-Path $root ('build/'+$Configuration)) -Filter *.exe|ForEach-Object{$executables[$_.Name]=(Get-FileHash $_.FullName).Hash.ToLowerInvariant()}
@{built_utc=[DateTime]::UtcNow.ToString('o');source_files=$hashes;executables=$executables;configuration=$Configuration;fixture_adaptation='Only Xbox360 example serial is fixed for persistent per-instance association; see CMakeLists.txt'}|ConvertTo-Json -Depth 10|Set-Content (Join-Path $root 'build/build-identity.json') -Encoding ASCII
