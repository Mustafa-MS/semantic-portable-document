$ErrorActionPreference = 'Stop'
$workspacePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonExe = if (Test-Path -LiteralPath $workspacePython) { $workspacePython } else { 'python' }
$env:PYTHONPATH = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
& $pythonExe -m harness.run_phase1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
