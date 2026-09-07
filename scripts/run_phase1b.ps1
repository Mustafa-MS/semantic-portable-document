$ErrorActionPreference = 'Stop'
$workspacePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonExe = if (Test-Path -LiteralPath $workspacePython) { $workspacePython } else { 'python' }
$workspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONPATH = $workspaceRoot
& $pythonExe -m harness.run_phase1b
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
