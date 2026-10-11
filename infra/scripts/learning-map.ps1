# Project Analyzer - deterministic learning map for a project.
# Reads registries/knowledge-registry.yaml (concept graph) and
# registries/evidence.yaml (current mastery), selects the concepts a project
# uses, and prints a prerequisite-ordered study plan with the gaps.
# No LLM, no network, no Docker.
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/learning-map.ps1 -Project devmate
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/learning-map.ps1 -Project devmate -Out docs/learning/paths/devmate-learning-map.md

param(
    [Parameter(Mandatory = $true)][string]$Project,
    [string]$Out
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegFile = "$RootDir/registries/knowledge-registry.yaml"
$EvFile = "$RootDir/registries/evidence.yaml"

foreach ($f in @($RegFile, $EvFile)) {
    if (-not (Test-Path -LiteralPath $f -PathType Leaf)) {
        Write-Host "FAIL: missing input $f"
        exit 1
    }
}

function Split-List {
    param([string]$Raw)
    $Raw = $Raw.Trim()
    if ($Raw -eq "") { return @() }
    return @($Raw -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne "" })
}

# --- Parse nodes --------------------------------------------------------
$nodes = @()
$cur = $null
foreach ($line in (Get-Content -LiteralPath $RegFile -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $nodes += $cur }
        $cur = @{
            id = $matches[1].Trim(); name = ""; level = ""; level_target = 0
            prerequisites = @(); taught_in = @(); sources = @(); exercises = @()
            used_by_projects = @(); evidence_required = @()
        }
        continue
    }
    if (-not $cur) { continue }
    if ($line -match '^\s*name:\s*(.+)') { $cur.name = $matches[1].Trim() }
    elseif ($line -match '^\s*level:\s*(.+)') { $cur.level = $matches[1].Trim() }
    elseif ($line -match '^\s*level_target:\s*(\d+)') { $cur.level_target = [int]$matches[1] }
    elseif ($line -match '^\s*prerequisites:\s*\[(.*)\]') { $cur.prerequisites = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*taught_in:\s*\[(.*)\]') { $cur.taught_in = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*sources:\s*\[(.*)\]') { $cur.sources = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*exercises:\s*\[(.*)\]') { $cur.exercises = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*used_by_projects:\s*\[(.*)\]') { $cur.used_by_projects = @(Split-List $matches[1]) }
    elseif ($line -match '^\s*evidence_required:\s*\[(.*)\]') { $cur.evidence_required = @(Split-List $matches[1]) }
}
if ($cur) { $nodes += $cur }

# --- Parse evidence (current level per skill = max) ---------------------
$current = @{}
$ce = $null
foreach ($line in (Get-Content -LiteralPath $EvFile -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') { $ce = @{ skill = ""; level = 0 }; continue }
    if (-not $ce) { continue }
    if ($line -match '^\s*skill:\s*(.+)') { $ce.skill = $matches[1].Trim() }
    elseif ($line -match '^\s*level:\s*(\d+)') { $ce.level = [int]$matches[1] }
    if ($ce.skill -and $ce.level -gt 0) {
        if (-not $current.ContainsKey($ce.skill) -or $ce.level -gt $current[$ce.skill]) {
            $current[$ce.skill] = $ce.level
        }
        $ce = $null
    }
}

# --- Select the project's concepts --------------------------------------
$required = @($nodes | Where-Object {
    $hit = $false
    foreach ($p in $_.used_by_projects) { if ($p -like "*$Project*") { $hit = $true; break } }
    $hit
})

if ($required.Count -eq 0) {
    Write-Host "No concepts reference project '$Project'. Check the used_by_projects values in the registry."
    exit 1
}

$requiredIds = @($required | ForEach-Object { $_.id })

# --- Topological order (prerequisites before dependents) ----------------
$indegree = @{}
$adj = @{}
foreach ($n in $required) {
    $indegree[$n.id] = 0
    $adj[$n.id] = @()
}
foreach ($n in $required) {
    foreach ($p in $n.prerequisites) {
        if ($requiredIds -contains $p) {
            $adj[$p] += $n.id
            $indegree[$n.id] = $indegree[$n.id] + 1
        }
    }
}
$ready = @($indegree.Keys | Where-Object { $indegree[$_] -eq 0 } | Sort-Object)
$order = @()
while ($ready.Count -gt 0) {
    $id = $ready[0]
    $ready = @($ready | Select-Object -Skip 1)
    $order += $id
    foreach ($m in $adj[$id]) {
        $indegree[$m] = $indegree[$m] - 1
        if ($indegree[$m] -eq 0) { $ready = @(($ready + $m) | Sort-Object) }
    }
}
# Any node left (cycle) is appended so nothing is silently dropped.
foreach ($n in $required) { if ($order -notcontains $n.id) { $order += $n.id } }

$byId = @{}
foreach ($n in $required) { $byId[$n.id] = $n }

$gaps = @($required | Where-Object {
    $lvl = if ($current.ContainsKey($_.id)) { $current[$_.id] } else { 0 }
    $lvl -lt $_.level_target
})

# --- Render -------------------------------------------------------------
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append("# Learning Map: $Project`n`n")
[void]$sb.Append("Generated by ``infra/scripts/learning-map.ps1`` from ``registries/knowledge-registry.yaml`` + ``registries/evidence.yaml``.`n`n")
[void]$sb.Append("**Required concepts:** $($required.Count) | **At target:** $($required.Count - $gaps.Count) | **Gaps:** $($gaps.Count)`n`n")

[void]$sb.Append("## Study plan (prerequisite order)`n`n")
$i = 0
foreach ($id in $order) {
    $n = $byId[$id]
    $lvl = if ($current.ContainsKey($id)) { $current[$id] } else { 0 }
    $gap = [Math]::Max(0, $n.level_target - $lvl)
    $status = if ($gap -gt 0) { "GAP" } else { "ok" }
    $i++
    [void]$sb.Append("$i. ``$($n.id)`` - $($n.name)  [$status] target $($n.level_target), current $lvl, gap $gap`n")
    [void]$sb.Append("   - taught_in: $(if ($n.taught_in.Count) { ($n.taught_in -join ', ') } else { 'none' })`n")
    [void]$sb.Append("   - source: $(if ($n.sources.Count) { ($n.sources -join ', ') } else { 'none' })`n")
    [void]$sb.Append("   - exercise: $(if ($n.exercises.Count) { ($n.exercises -join ', ') } else { 'none' })`n")
    [void]$sb.Append("   - evidence required: $(if ($n.evidence_required.Count) { ($n.evidence_required -join ', ') } else { 'none' })`n")
}
[void]$sb.Append("`n## Focus first (the gaps, in prerequisite order)`n`n")
$gapIds = @($order | Where-Object { $gaps.id -contains $_ })
if ($gapIds.Count -eq 0) {
    [void]$sb.Append("None - every required concept is at or above target.`n")
} else {
    foreach ($id in $gapIds) {
        $n = $byId[$id]
        $lvl = if ($current.ContainsKey($id)) { $current[$id] } else { 0 }
        [void]$sb.Append("- ``$($n.id)`` - $($n.name) (target $($n.level_target), current $lvl)`n")
    }
}

$content = $sb.ToString()
if ($Out) {
    $target = if ([System.IO.Path]::IsPathRooted($Out)) { $Out } else { Join-Path $RootDir $Out }
    [System.IO.File]::WriteAllText($target, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Wrote $Out ($($required.Count) concepts, $($gaps.Count) gaps)"
} else {
    Write-Output $content
}
