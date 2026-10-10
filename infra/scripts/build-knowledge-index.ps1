# Build the concept-oriented knowledge index from the knowledge registry.
# Renders registries/knowledge-registry.yaml into docs/reference/INDEX.md so the
# reference stays a generated view of the graph, never a hand-edited copy.
# -Check: exit 1 if the committed index drifts from the registry (CI gate).
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/build-knowledge-index.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/build-knowledge-index.ps1 -Check

param([switch]$Check)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegFile = "$RootDir/registries/knowledge-registry.yaml"
$OutFile = "$RootDir/docs/reference/INDEX.md"

function Split-List {
    param([string]$Raw)
    $Raw = $Raw.Trim()
    if ($Raw -eq "") { return @() }
    return @($Raw -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne "" })
}

if (-not (Test-Path -LiteralPath $RegFile -PathType Leaf)) {
    Write-Host "FAIL: registry missing: $RegFile"
    exit 1
}

# --- Parse nodes (same shape as tests/knowledge/validate.ps1) -----------
$nodes = @()
$domainOrder = @()
$cur = $null
$domain = ""
foreach ($line in (Get-Content -LiteralPath $RegFile -Raw) -split "`n") {
    if ($line -match '^\s{2}([a-z][a-z0-9-]*):\s*$') {
        $domain = $matches[1]
        if ($domainOrder -notcontains $domain) { $domainOrder += $domain }
        continue
    }
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $nodes += $cur }
        $cur = @{
            id = $matches[1].Trim(); domain = $domain; name = ""; level = ""
            prerequisites = @(); taught_in = @(); sources = @()
            exercises = @(); used_by_projects = @(); evidence = ""; status = ""
        }
        continue
    }
    if (-not $cur) { continue }
    if ($line -match '^\s*name:\s*(.+)') { $cur.name = $matches[1].Trim() }
    elseif ($line -match '^\s*level:\s*(.+)') { $cur.level = $matches[1].Trim() }
    elseif ($line -match '^\s*prerequisites:\s*\[(.*)\]') { $cur.prerequisites = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*taught_in:\s*\[(.*)\]') { $cur.taught_in = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*sources:\s*\[(.*)\]') { $cur.sources = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*exercises:\s*\[(.*)\]') { $cur.exercises = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*used_by_projects:\s*\[(.*)\]') { $cur.used_by_projects = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*evidence:\s*(.+)') { $cur.evidence = $matches[1].Trim().Trim('"') }
    elseif ($line -match '^\s*status:\s*(.+)') { $cur.status = $matches[1].Trim() }
}
if ($cur) { $nodes += $cur }

function Code-List {
    param([string[]]$Items)
    if ($Items.Count -eq 0) { return "none" }
    return (($Items | ForEach-Object { "``$_``" }) -join ", ")
}

# --- Render -------------------------------------------------------------
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append("# Knowledge Index`n`n")
[void]$sb.Append("> Generated from ``registries/knowledge-registry.yaml`` by ``infra/scripts/build-knowledge-index.ps1``.`n")
[void]$sb.Append("> Do not edit by hand. Run the script and commit the result. The knowledge gate fails CI when this file drifts.`n`n")
[void]$sb.Append("**$($nodes.Count) concepts across $($domainOrder.Count) domains.**`n")

foreach ($d in $domainOrder) {
    $dn = @($nodes | Where-Object { $_.domain -eq $d })
    [void]$sb.Append("`n## $d`n")
    foreach ($n in $dn) {
        [void]$sb.Append("`n### ``$($n.id)`` - $($n.name)`n`n")
        [void]$sb.Append("- **Level:** $($n.level)`n")
        [void]$sb.Append("- **Prerequisites:** $(Code-List $n.prerequisites)`n")
        [void]$sb.Append("- **Taught in:** $(Code-List $n.taught_in)`n")
        [void]$sb.Append("- **Sources:** $(Code-List $n.sources)`n")
        [void]$sb.Append("- **Exercises:** $(Code-List $n.exercises)`n")
        [void]$sb.Append("- **Used by:** $(Code-List $n.used_by_projects)`n")
        [void]$sb.Append("- **Evidence:** $($n.evidence)`n")
    }
}

$content = $sb.ToString()

if ($Check) {
    if (-not (Test-Path -LiteralPath $OutFile -PathType Leaf)) {
        Write-Host "FAIL: knowledge index missing: docs/reference/INDEX.md (run build-knowledge-index.ps1)"
        exit 1
    }
    $existing = (Get-Content -LiteralPath $OutFile -Raw) -replace "`r`n", "`n"
    if ($existing.TrimEnd("`n") -ne $content.TrimEnd("`n")) {
        Write-Host "FAIL: docs/reference/INDEX.md is stale (run build-knowledge-index.ps1 and commit)"
        exit 1
    }
    Write-Host "knowledge index: OK ($($nodes.Count) concepts)"
    exit 0
}

[System.IO.File]::WriteAllText($OutFile, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote docs/reference/INDEX.md ($($nodes.Count) concepts across $($domainOrder.Count) domains)"
