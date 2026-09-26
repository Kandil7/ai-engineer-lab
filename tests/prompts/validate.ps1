<#
.SYNOPSIS
    Validate all prompt files exist and match the registry.

.DESCRIPTION
    Checks that every prompt listed in prompt-registry.yaml exists on disk,
    the registry matches actual files, and no orphaned prompts exist.

.EXAMPLE
    ./tests/prompts/validate.ps1
    ./tests/prompts/validate.ps1 -Verbose
#>

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegistryFile = "$RootDir/registries/prompt-registry.yaml"

# ─── Counters ──────────────────────────────────────

$passCount = 0
$failCount = 0
$warnCount = 0

# ─── Helpers ───────────────────────────────────────

function Write-Check {
    param([string]$Message)
    Write-Host "  [CHECK] $Message" -ForegroundColor Cyan
}

function Write-Pass {
    param([string]$Message)
    Write-Host "  [PASS]  $Message" -ForegroundColor Green
    $script:passCount++
}

function Write-Fail {
    param([string]$Message)
    Write-Host "  [FAIL]  $Message" -ForegroundColor Red
    $script:failCount++
}

function Write-Warn {
    param([string]$Message)
    Write-Host "  [WARN]  $Message" -ForegroundColor Yellow
    $script:warnCount++
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Prompt Validation                     ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── 1. Check Registry ────────────────────────────

Write-Host "`n── Registry Check ──" -ForegroundColor White

if (-not (Test-Path $RegistryFile)) {
    Write-Fail "Prompt registry not found: $RegistryFile"
    exit 1
}

Write-Pass "Prompt registry found"

# ─── 2. Parse Registry ────────────────────────────

Write-Host "`n── Registry Parsing ──" -ForegroundColor White

$registryContent = Get-Content $RegistryFile -Raw

# Extract prompt entries
$promptEntries = @()
$lines = $registryContent -split "`n"
$currentPrompt = $null

foreach ($line in $lines) {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($currentPrompt) {
            $promptEntries += $currentPrompt
        }
        $currentPrompt = @{
            id = $matches[1].Trim()
            path = ""
            layer = ""
            status = ""
            version = ""
        }
    }
    elseif ($line -match '^\s*path:\s*(.+)') {
        if ($currentPrompt) {
            $currentPrompt.path = $matches[1].Trim()
        }
    }
    elseif ($line -match '^\s*layer:\s*(.+)') {
        if ($currentPrompt) {
            $currentPrompt.layer = $matches[1].Trim()
        }
    }
    elseif ($line -match '^\s*status:\s*(.+)') {
        if ($currentPrompt) {
            $currentPrompt.status = $matches[1].Trim()
        }
    }
    elseif ($line -match '^\s*version:\s*(.+)') {
        if ($currentPrompt) {
            $currentPrompt.version = $matches[1].Trim()
        }
    }
}

if ($currentPrompt) {
    $promptEntries += $currentPrompt
}

Write-Pass "Parsed $($promptEntries.Count) prompts from registry"

# ─── 3. Validate Each Prompt ──────────────────────

Write-Host "`n── Prompt Validation ──" -ForegroundColor White

$layerCounts = @{}

foreach ($prompt in $promptEntries) {
    $fullPath = Join-Path $RootDir $prompt.path

    # Count by layer
    if (-not $layerCounts.ContainsKey($prompt.layer)) {
        $layerCounts[$prompt.layer] = 0
    }
    $layerCounts[$prompt.layer]++

    # Check file exists
    if (-not (Test-Path $fullPath -PathType Leaf)) {
        Write-Fail "Prompt file missing: $($prompt.id) ($($prompt.path))"
        continue
    }

    Write-Pass "File exists: $($prompt.id) (v$($prompt.version))"

    # Check prompt has content
    $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
    if ($content.Length -lt 20) {
        Write-Warn "Prompt '$($prompt.id)' seems too short ($($content.Length) chars)"
    }

    # Check status is valid
    if ($prompt.status -notin @("active", "draft", "deprecated")) {
        Write-Warn "Prompt '$($prompt.id)' has unusual status: $($prompt.status)"
    }

    # Check version format
    if ($prompt.version -notmatch '^\d+\.\d+\.\d+$') {
        Write-Warn "Prompt '$($prompt.id)' has non-standard version: $($prompt.version)"
    }
}

# ─── 4. Layer Summary ─────────────────────────────

Write-Host "`n── Layer Summary ──" -ForegroundColor White

foreach ($layer in $layerCounts.Keys | Sort-Object) {
    Write-Host "  $layer : $($layerCounts[$layer]) prompts" -ForegroundColor Gray
}

# ─── 5. Check for Orphaned Prompts ────────────────

Write-Host "`n── Orphan Check ──" -ForegroundColor White

$registryPaths = $promptEntries | ForEach-Object { $_.path }
$promptLayers = @("system", "roles", "tasks", "critics", "repair")

foreach ($layer in $promptLayers) {
    $layerDir = "$RootDir/.ai/prompts/$layer"
    if (Test-Path $layerDir -PathType Container) {
        $layerFiles = Get-ChildItem "$layerDir/*.md" -ErrorAction SilentlyContinue

        foreach ($file in $layerFiles) {
            $relativePath = $file.FullName.Replace("$RootDir\", "").Replace("\", "/")
            if ($relativePath -notin $registryPaths) {
                Write-Warn "Orphaned prompt (not in registry): $relativePath"
            } else {
                if ($Verbose) {
                    Write-Pass "Registered: $($file.Name)"
                }
            }
        }
    }
}

# Check registry entries that don't have files
foreach ($prompt in $promptEntries) {
    $fullPath = Join-Path $RootDir $prompt.path
    if (-not (Test-Path $fullPath)) {
        Write-Fail "Registry entry without file: $($prompt.id) -> $($prompt.path)"
    }
}

# ─── 6. Check for Duplicate IDs ───────────────────

Write-Host "`n── Duplicate Check ──" -ForegroundColor White

$ids = $promptEntries | ForEach-Object { $_.id }
$duplicates = $ids | Group-Object | Where-Object { $_.Count -gt 1 }

if ($duplicates) {
    foreach ($dup in $duplicates) {
        Write-Fail "Duplicate prompt ID: $($dup.Name) (found $($dup.Count) times)"
    }
} else {
    Write-Pass "No duplicate prompt IDs"
}

# ─── Summary ───────────────────────────────────────

Write-Host "`n── Summary ──" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Warnings: $warnCount" -ForegroundColor $(if ($warnCount -gt 0) { "Yellow" } else { "Green" })

if ($failCount -gt 0 -or $warnCount -gt 0) {
    Write-Host "`n  [FAIL] Validation FAILED" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n  [PASS] All prompts valid" -ForegroundColor Green
    exit 0
}
