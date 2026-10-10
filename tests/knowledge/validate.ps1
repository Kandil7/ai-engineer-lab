# Validate the knowledge registry: the concept graph behind the Learning OS.
# Checks that every node resolves: unique ids, prerequisites that exist,
# taught_in / exercises / used_by_projects paths present on disk, source
# anchors that exist in source-index.md, and no orphan or cyclic node.
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tests/knowledge/validate.ps1

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegFile = "$RootDir/registries/knowledge-registry.yaml"
$SourceIndex = "$RootDir/learning-sources/source-index.md"

$passCount = 0
$failCount = 0

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

function Split-List {
    param([string]$Raw)
    $Raw = $Raw.Trim()
    if ($Raw -eq "") { return @() }
    return @($Raw -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne "" })
}

Write-Host ""
Write-Host "  Knowledge Registry Validation" -ForegroundColor Magenta

# --- 1. Registry exists -------------------------------------------------
if (-not (Test-Path -LiteralPath $RegFile -PathType Leaf)) {
    Write-Fail "Registry missing: $RegFile"
    exit 1
}
Write-Pass "Registry found: registries/knowledge-registry.yaml"

# --- 2. Parse nodes -----------------------------------------------------
$nodes = @()
$cur = $null
$domain = ""
foreach ($line in (Get-Content -LiteralPath $RegFile -Raw) -split "`n") {
    if ($line -match '^\s{2}([a-z][a-z0-9-]*):\s*$') {
        $domain = $matches[1]
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

if ($nodes.Count -eq 0) {
    Write-Fail "No nodes parsed from registry"
    exit 1
}
Write-Pass "Parsed $($nodes.Count) concept nodes"

$ids = @($nodes | ForEach-Object { $_.id })

# --- 3. Unique ids ------------------------------------------------------
$dupes = @($ids | Group-Object | Where-Object { $_.Count -gt 1 } | ForEach-Object { $_.Name })
if ($dupes.Count -gt 0) {
    Write-Fail "Duplicate node ids: $($dupes -join ', ')"
} else {
    Write-Pass "All node ids are unique"
}

# --- 4. Required fields -------------------------------------------------
$fieldFail = $false
foreach ($n in $nodes) {
    if ($n.name -eq "") { Write-Fail "Node '$($n.id)' has empty name"; $fieldFail = $true }
    if ($n.level -notin @("core", "advanced")) { Write-Fail "Node '$($n.id)' has invalid level '$($n.level)'"; $fieldFail = $true }
    if ($n.evidence -eq "") { Write-Fail "Node '$($n.id)' has empty evidence"; $fieldFail = $true }
    if ($n.status -notin @("active", "deprecated")) { Write-Fail "Node '$($n.id)' has invalid status '$($n.status)'"; $fieldFail = $true }
    if ($n.taught_in.Count -eq 0) { Write-Fail "Node '$($n.id)' has no taught_in"; $fieldFail = $true }
    if ($n.used_by_projects.Count -eq 0) { Write-Fail "Node '$($n.id)' has no used_by_projects"; $fieldFail = $true }
}
if (-not $fieldFail) { Write-Pass "All nodes carry name, level, evidence, status, taught_in, used_by_projects" }

# --- 5. Prerequisites resolve ------------------------------------------
$prereqFail = $false
foreach ($n in $nodes) {
    foreach ($p in $n.prerequisites) {
        if ($ids -notcontains $p) {
            Write-Fail "Node '$($n.id)' prerequisite '$p' is not a known node id"
            $prereqFail = $true
        }
    }
}
if (-not $prereqFail) { Write-Pass "All prerequisites resolve to known nodes" }

# --- 6. Path references exist ------------------------------------------
$pathFail = $false
foreach ($n in $nodes) {
    foreach ($ref in @($n.taught_in + $n.exercises + $n.used_by_projects)) {
        $target = Join-Path $RootDir ($ref -replace '/', '\')
        if (-not (Test-Path -LiteralPath $target)) {
            Write-Fail "Node '$($n.id)' references missing path '$ref'"
            $pathFail = $true
        }
    }
}
if (-not $pathFail) { Write-Pass "All taught_in / exercises / used_by_projects paths exist" }

# --- 7. Source anchors exist -------------------------------------------
$srcFail = $false
if (-not (Test-Path -LiteralPath $SourceIndex -PathType Leaf)) {
    Write-Fail "Source index missing: $SourceIndex"
    exit 1
}
$indexNumbers = @([regex]::Matches((Get-Content -LiteralPath $SourceIndex -Raw), '(?m)^\|\s*(\d+)\s*\|') | ForEach-Object { $_.Groups[1].Value })
foreach ($n in $nodes) {
    foreach ($src in $n.sources) {
        if ($src -notmatch '^source-index#(\d+)$') {
            Write-Fail "Node '$($n.id)' source '$src' is not a source-index#N anchor"
            $srcFail = $true
            continue
        }
        if ($indexNumbers -notcontains $matches[1]) {
            Write-Fail "Node '$($n.id)' source anchor '#$($matches[1])' not found in source-index.md"
            $srcFail = $true
        }
    }
}
if (-not $srcFail) { Write-Pass "All source anchors resolve in source-index.md" }

# --- 8. No orphan / cyclic node ----------------------------------------
# A node is anchored if it is a root (no prerequisites) or any prerequisite
# is anchored. Any node left unanchored sits in a cycle or a dangling chain.
$anchored = @{}
foreach ($n in $nodes) { if ($n.prerequisites.Count -eq 0) { $anchored[$n.id] = $true } }
$changed = $true
while ($changed) {
    $changed = $false
    foreach ($n in $nodes) {
        if ($anchored.ContainsKey($n.id)) { continue }
        foreach ($p in $n.prerequisites) {
            if ($anchored.ContainsKey($p)) { $anchored[$n.id] = $true; $changed = $true; break }
        }
    }
}
$orphans = @($nodes | Where-Object { -not $anchored.ContainsKey($_.id) } | ForEach-Object { $_.id })
if ($orphans.Count -gt 0) {
    Write-Fail "Unreachable or cyclic nodes: $($orphans -join ', ')"
} else {
    Write-Pass "Every node is reachable from a root (no orphans, no cycles)"
}

# --- Summary ------------------------------------------------------------
Write-Host ""
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
if ($failCount -gt 0) {
    Write-Host ""
    Write-Host "  [FAIL] Knowledge registry validation FAILED" -ForegroundColor Red
    exit 1
} else {
    Write-Host ""
    Write-Host "  [PASS] Knowledge registry valid" -ForegroundColor Green
    exit 0
}
