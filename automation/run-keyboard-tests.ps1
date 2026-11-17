param([ValidateSet('baseline','Keyboard-Mouse','Combined')][string]$Filter='baseline',[int]$Repetitions=3,[int]$Samples=1000,[int]$Rate=125)
& (Join-Path $PSScriptRoot 'run-input-tests.ps1') -Profile keyboard -Filter $Filter -Repetitions $Repetitions -Samples $Samples -Rate $Rate
