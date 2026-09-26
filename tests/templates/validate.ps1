<#
.SYNOPSIS
    Validate all templates exist and have required sections.

.DESCRIPTION
    Checks that every template listed in template-registry.yaml exists,
    each template has the required sections defined in the registry,
    and the registry matches the actual files on disk.

.EXAMPLE
    ./tests/templates/validate.ps1
    ./tests/templates/validate.ps1 -Verbose
#>

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegistryFile = "$RootDir/registries/template-registry.yaml"

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
  ║   Template Validation                   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── 1. Check Registry Exists ─────────────────────

Write-Host "`n── Registry Check ──" -ForegroundColor White

if (-not (Test-Path $RegistryFile)) {
    Write-Fail "Template registry not found: $RegistryFile"
    exit 1
}

Write-Pass "Template registry found"

# ─── 2. Parse Registry ────────────────────────────

Write-Host "`n── Registry Parsing ──" -ForegroundColor White

$registryContent = Get-Content $RegistryFile -Raw

# Extract template entries (simplified YAML parsing)
$templateEntries = @()
$lines = $registryContent -split "`n"
$currentTemplate = $null

foreach ($line in $lines) {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($currentTemplate) {
            $templateEntries += $currentTemplate
        }
        $currentTemplate = @{
            id = $matches[1].Trim()
            path = ""
            required_sections = @()
        }
    }
    elseif ($line -match '^\s*path:\s*(.+)') {
        if ($currentTemplate) {
            $currentTemplate.path = $matches[1].Trim()
        }
    }
    elseif ($line -match '^\s*required_sections:\s*\[(.+)\]') {
        if ($currentTemplate) {
            # Quote-aware split: section names may contain commas inside quotes
            # (e.g. "My Inferences (not stated, my interpretation)").
            $raw = $matches[1].Trim()
            $quoted = @([regex]::Matches($raw, '"([^"]*)"') | ForEach-Object { $_.Groups[1].Value })
            if ($quoted.Count -gt 0) {
                $sections = $quoted
            } else {
                $sections = $raw -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") }
            }
            $currentTemplate.required_sections = $sections
        }
    }
}

if ($currentTemplate) {
    $templateEntries += $currentTemplate
}

Write-Pass "Parsed $($templateEntries.Count) templates from registry"

# ─── 3. Validate Each Template ────────────────────

Write-Host "`n── Template Validation ──" -ForegroundColor White

foreach ($tpl in $templateEntries) {
    $fullPath = Join-Path $RootDir $tpl.path

    # Check file exists
    if (-not (Test-Path $fullPath -PathType Leaf)) {
        Write-Fail "Template file missing: $($tpl.id) ($($tpl.path))"
        continue
    }

    Write-Pass "File exists: $($tpl.id)"

    # Check required sections
    if ($tpl.required_sections.Count -gt 0) {
        $content = Get-Content $fullPath -Raw
        $missingSections = @()

        foreach ($section in $tpl.required_sections) {
            # Check for section as heading (## Section) or as placeholder
            $sectionPattern = "##?\s*$([regex]::Escape($section))"
            if ($content -notmatch $sectionPattern) {
                $missingSections += $section
            }
        }

        if ($missingSections.Count -gt 0) {
            Write-Warn "Template '$($tpl.id)' missing sections: $($missingSections -join ', ')"
        } else {
            Write-Pass "All sections present: $($tpl.id)"
        }
    }
}

# ─── 4. Check for Orphaned Templates ──────────────

Write-Host "`n── Orphan Check ──" -ForegroundColor White

$registryPaths = $templateEntries | ForEach-Object { $_.path }
$templateFiles = Get-ChildItem "$RootDir/templates/*.template.md" -ErrorAction SilentlyContinue

foreach ($file in $templateFiles) {
    $relativePath = $file.FullName.Replace("$RootDir\", "").Replace("\", "/")
    if ($relativePath -notin $registryPaths) {
        Write-Warn "Orphaned template (not in registry): $($file.Name)"
    } else {
        if ($Verbose) {
            Write-Pass "Registered: $($file.Name)"
        }
    }
}

# Check registry entries that don't have files
foreach ($tpl in $templateEntries) {
    $fullPath = Join-Path $RootDir $tpl.path
    if (-not (Test-Path $fullPath)) {
        Write-Fail "Registry entry without file: $($tpl.id) -> $($tpl.path)"
    }
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
    Write-Host "`n  [PASS] All templates valid" -ForegroundColor Green
    exit 0
}
