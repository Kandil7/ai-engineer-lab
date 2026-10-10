# Local CI: the full gate in one command. Mirrors .github/workflows/ci.yml
# (devmate job + workspace job + docs job) using the local environments of
# record: the devmate .venv python and the five tests/*/validate.ps1 suites.
# After `uv sync --locked --extra dev`, the same checks run via
# `uv run --frozen python -m <tool>`; CI already does that.
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/local-ci.ps1

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$failed = $false

function Invoke-Gate {
    param([string]$Name, [string]$Workdir, [string]$Command)
    Write-Host ""
    Write-Host ("=== {0} ===" -f $Name)
    Push-Location -LiteralPath $Workdir
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) {
            Write-Host ("FAIL: {0} (exit {1})" -f $Name, $LASTEXITCODE)
            $script:failed = $true
        } else {
            Write-Host ("PASS: {0}" -f $Name)
        }
    } finally {
        Pop-Location
    }
}

$devmate = Join-Path $repoRoot "projects\04-ai-engineering\devmate"
$devPy = Join-Path $devmate ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $devPy)) {
    Write-Host "FAIL: devmate venv python not found at $devPy"
    exit 1
}

Invoke-Gate "devmate ruff" $devmate "& `"$devPy`" -m ruff check ."
Invoke-Gate "devmate format" $devmate "& `"$devPy`" -m ruff format --check ."
Invoke-Gate "devmate mypy" $devmate "& `"$devPy`" -m mypy src/"
Invoke-Gate "devmate pytest" $devmate "& `"$devPy`" -m pytest -q --cov=devmate --cov-report=term-missing"

$legacy = Join-Path $repoRoot "projects\00-core-foundations\python"
Invoke-Gate "legacy pytest" $legacy "& python -m pytest -q"

foreach ($suite in @("prompts", "workflows", "templates", "registries", "knowledge", "repo-structure")) {
    Invoke-Gate "validate $suite" $repoRoot ("powershell -NoProfile -ExecutionPolicy Bypass -File tests/{0}/validate.ps1" -f $suite)
}

Invoke-Gate "knowledge index" $repoRoot "powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/build-knowledge-index.ps1 -Check"

Invoke-Gate "docs gates" $repoRoot "powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/docs-gates.ps1"

Write-Host ""
if ($failed) {
    Write-Host "LOCAL CI: FAIL"
    exit 1
} else {
    Write-Host "LOCAL CI: ALL GREEN"
    exit 0
}
