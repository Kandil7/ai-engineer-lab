# Build the skills scoreboard: a generated view of the evidence ledger joined
# with the knowledge registry. Replaces manual editing of mastery numbers.
# -Check: exit 1 if the committed scoreboard drifts (CI gate).
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/build-skills-scoreboard.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/build-skills-scoreboard.ps1 -Check

param([switch]$Check)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegFile = "$RootDir/registries/knowledge-registry.yaml"
$EvFile = "$RootDir/registries/evidence.yaml"
$OutFile = "$RootDir/docs/roadmap/skills-scoreboard.md"

foreach ($f in @($RegFile, $EvFile)) {
    if (-not (Test-Path -LiteralPath $f -PathType Leaf)) {
        Write-Host "FAIL: missing input $f"
        exit 1
    }
}

# --- Parse nodes --------------------------------------------------------
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
        $cur = @{ id = $matches[1].Trim(); domain = $domain; name = ""; level_target = 0 }
        continue
    }
    if (-not $cur) { continue }
    if ($line -match '^\s*name:\s*(.+)') { $cur.name = $matches[1].Trim() }
    elseif ($line -match '^\s*level_target:\s*(\d+)') { $cur.level_target = [int]$matches[1] }
}
if ($cur) { $nodes += $cur }

# --- Parse evidence -----------------------------------------------------
$current = @{}
$types = @{}
$count = @{}
$ce = $null
foreach ($line in (Get-Content -LiteralPath $EvFile -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') {
        $ce = @{ skill = ""; level = 0; type = "" }
        continue
    }
    if (-not $ce) { continue }
    if ($line -match '^\s*skill:\s*(.+)') { $ce.skill = $matches[1].Trim() }
    elseif ($line -match '^\s*level:\s*(\d+)') { $ce.level = [int]$matches[1] }
    elseif ($line -match '^\s*type:\s*(.+)') { $ce.type = $matches[1].Trim() }
    if ($ce.skill -and $ce.level -gt 0 -and $ce.type) {
        if (-not $current.ContainsKey($ce.skill) -or $ce.level -gt $current[$ce.skill]) {
            $current[$ce.skill] = $ce.level
        }
        if (-not $types.ContainsKey($ce.skill)) { $types[$ce.skill] = @() }
        if ($types[$ce.skill] -notcontains $ce.type) { $types[$ce.skill] += $ce.type }
        $count[$ce.skill] = 1 + ($count[$ce.skill])
        $ce = $null
    }
}

# --- Render -------------------------------------------------------------
$withEvidence = @($nodes | Where-Object { $current.ContainsKey($_.id) }).Count
$metTarget = @($nodes | Where-Object { $current.ContainsKey($_.id) -and $current[$_.id] -ge $_.level_target }).Count
$noEvidence = $nodes.Count - $withEvidence

$sb = New-Object System.Text.StringBuilder
[void]$sb.Append("# Skills Scoreboard`n`n")
[void]$sb.Append("> Generated from ``registries/evidence.yaml`` joined with ``registries/knowledge-registry.yaml`` by ``infra/scripts/build-skills-scoreboard.ps1``.`n")
[void]$sb.Append("> Do not edit by hand. Run the script and commit the result. The knowledge gate fails CI when this file drifts.`n`n")
[void]$sb.Append("**Summary:** $($nodes.Count) concepts, $withEvidence with evidence, $metTarget at or above target, $noEvidence with no evidence yet.`n")

foreach ($d in $domainOrder) {
    $dn = @($nodes | Where-Object { $_.domain -eq $d })
    [void]$sb.Append("`n## $d`n`n")
    [void]$sb.Append("| Concept | Target | Current | Gap | Evidence |`n")
    [void]$sb.Append("| --- | --- | --- | --- | --- |`n")
    foreach ($n in $dn) {
        $lvl = if ($current.ContainsKey($n.id)) { $current[$n.id] } else { 0 }
        $gap = [Math]::Max(0, $n.level_target - $lvl)
        $evText = if ($count.ContainsKey($n.id)) { "$($count[$n.id]) ($($types[$n.id] -join ', '))" } else { "none" }
        [void]$sb.Append("| ``$($n.id)`` $($n.name) | $($n.level_target) | $lvl | $gap | $evText |`n")
    }
}

$content = $sb.ToString()

if ($Check) {
    if (-not (Test-Path -LiteralPath $OutFile -PathType Leaf)) {
        Write-Host "FAIL: skills scoreboard missing (run build-skills-scoreboard.ps1)"
        exit 1
    }
    $existing = (Get-Content -LiteralPath $OutFile -Raw) -replace "`r`n", "`n"
    if ($existing.TrimEnd("`n") -ne $content.TrimEnd("`n")) {
        Write-Host "FAIL: docs/roadmap/skills-scoreboard.md is stale (run build-skills-scoreboard.ps1 and commit)"
        exit 1
    }
    Write-Host "skills scoreboard: OK ($($nodes.Count) concepts, $withEvidence with evidence)"
    exit 0
}

[System.IO.File]::WriteAllText($OutFile, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote docs/roadmap/skills-scoreboard.md ($($nodes.Count) concepts, $withEvidence with evidence)"
