param([ValidateSet('baseline','Keyboard-Mouse','Combined')][string]$Filter='baseline',[ValidateSet('forward','modify','block')][string]$Operation='forward',[int]$Repetitions=3,[int]$Samples=1000,[int]$Rate=125)
& (Join-Path $PSScriptRoot 'run-input-tests.ps1') -Profile mouse -Filter $Filter -Operation $Operation -Repetitions $Repetitions -Samples $Samples -Rate $Rate
