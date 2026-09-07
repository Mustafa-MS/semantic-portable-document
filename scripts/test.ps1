$ErrorActionPreference = 'Stop'
$workspacePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonExe = if (Test-Path -LiteralPath $workspacePython) { $workspacePython } else { 'python' }
$env:PYTHONPATH = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
& $pythonExe -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
