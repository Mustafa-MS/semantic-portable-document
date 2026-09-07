$ErrorActionPreference = 'Stop'
$workspacePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonExe = if (Test-Path -LiteralPath $workspacePython) { $workspacePython } else { 'python' }
$workspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:PYTHONPATH = "$workspaceRoot;$workspaceRoot\.phase1c\deps\python"
$env:PYTHONUTF8 = '1'
& $pythonExe -m harness.run_phase1c
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
