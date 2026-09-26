<#
.SYNOPSIS
    Validate cross-registry consistency for the .ai prompt/workflow system.

.DESCRIPTION
    Checks that the registries agree with each other and with the files on
    disk: prompt frontmatter matches prompt-registry.yaml, workflow frontmatter
    matches workflow-registry.yaml, every prompts_used / used_by /
    used_by_workflows / reusable_by / pairs_with_roles reference resolves, no
    active prompt is orphaned, every skill is actually used, and every concrete
    path referenced inside .ai/ resolves.

.EXAMPLE
    ./tests/registries/validate.ps1
#>

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$PromptReg = "$RootDir/registries/prompt-registry.yaml"
$WorkflowReg = "$RootDir/registries/workflow-registry.yaml"
$SkillsReg = "$RootDir/registries/skills-registry.yaml"
$TemplateReg = "$RootDir/registries/template-registry.yaml"

# ─── Counters ──────────────────────────────────────

$passCount = 0
$failCount = 0
$warnCount = 0

# ─── Helpers ───────────────────────────────────────

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

function Parse-List {
    # Comma-split that respects double-quoted items (section names may
    # contain commas, e.g. "My Inferences (not stated, my interpretation)").
    param([string]$Raw)
    $Raw = $Raw.Trim()
    if ($Raw -eq "") { return @() }
    $items = @($Raw -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") })
    $merged = @()
    $buf = ""
    foreach ($item in $items) {
        if ($buf -ne "") { $buf += "," }
        $buf += $item
        $quotes = @([regex]::Matches($buf, '"')).Count
        if ($quotes % 2 -eq 0) { $merged += $buf.Trim('"').Trim("'").Trim(); $buf = "" }
    }
    if ($buf -ne "") { $merged += $buf.Trim('"').Trim("'").Trim() }
    return @($merged | Where-Object { $_ -ne "" })
}

function Test-Ref {
    # A reference resolves if it exactly matches an id or matches via a
    # trailing-* glob (feature/*, debugging/*, learning/learn-from-*).
    param([string]$Ref, [string[]]$Ids)
    if ($Ref.EndsWith("*")) {
        $prefix = $Ref.Substring(0, $Ref.Length - 1)
        return @($Ids | Where-Object { $_.StartsWith($prefix) }).Count -gt 0
    }
    return $Ids -contains $Ref
}

function Get-Frontmatter {
    param([string]$Path)
    $text = Get-Content $Path -Raw -ErrorAction SilentlyContinue
    if ($text -match '(?s)^---\r?\n(.*?)\r?\n---') { return $matches[1] }
    return ""
}

function Get-FmValue {
    param([string]$Frontmatter, [string]$Key)
    if ($Frontmatter -match "(?m)^$([regex]::Escape($Key)):\s*\[(.*)\]\s*$") {
        return @{ isList = $true; value = (Parse-List $matches[1]) }
    }
    if ($Frontmatter -match "(?m)^$([regex]::Escape($Key)):\s*(.+?)\s*$") {
        return @{ isList = $false; value = $matches[1].Trim() }
    }
    return $null
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Registry Consistency Validation       ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── 1. Registries Exist ──────────────────────────

Write-Host "`n── Registry Files ──" -ForegroundColor White

foreach ($f in @($PromptReg, $WorkflowReg, $SkillsReg, $TemplateReg)) {
    if (Test-Path $f -PathType Leaf) {
        Write-Pass "Registry found: $(Split-Path $f -Leaf)"
    } else {
        Write-Fail "Registry missing: $f"
    }
}

if ($failCount -gt 0) { exit 1 }

# ─── 2. Parse prompt-registry.yaml ────────────────

$promptEntries = @()
$cur = $null
foreach ($line in (Get-Content $PromptReg -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $promptEntries += $cur }
        $cur = @{ id = $matches[1].Trim(); path = ""; version = ""; status = "";
                  layer = ""; used_by = @(); trigger = ""; constraints = @() }
    }
    elseif ($cur -and $line -match '^\s*path:\s*(.+)') { $cur.path = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*version:\s*(.+)') { $cur.version = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*status:\s*(.+)') { $cur.status = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*layer:\s*(.+)') { $cur.layer = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*used_by:\s*\[(.*)\]') { $cur.used_by = @(Parse-List $matches[1]) }
    elseif ($cur -and $line -match '^\s*trigger:\s*(.+)') { $cur.trigger = $matches[1].Trim() }
}
if ($cur) { $promptEntries += $cur }

# ─── 3. Parse workflow-registry.yaml ──────────────

$workflowEntries = @()
$cur = $null
$category = ""
foreach ($line in (Get-Content $WorkflowReg -Raw) -split "`n") {
    if ($line -match '^\s{2}(\w+):') { $category = $matches[1] }
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $workflowEntries += $cur }
        $cur = @{ id = $matches[1].Trim(); path = ""; entry_point = "false";
                  prompts_used = @(); category = $category }
    }
    elseif ($cur -and $line -match '^\s*path:\s*(.+)') { $cur.path = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*entry_point:\s*(.+)') { $cur.entry_point = $matches[1].Trim().ToLower() }
    elseif ($cur -and $line -match '^\s*prompts_used:\s*\[(.*)\]') { $cur.prompts_used = @(Parse-List $matches[1]) }
}
if ($cur) { $workflowEntries += $cur }

# ─── 4. Parse skills-registry.yaml + template-registry.yaml ──

$skillEntries = @()
$cur = $null
foreach ($line in (Get-Content $SkillsReg -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $skillEntries += $cur }
        $cur = @{ id = $matches[1].Trim(); reusable_by = @() }
    }
    elseif ($cur -and $line -match '^\s*reusable_by:\s*\[(.*)\]') { $cur.reusable_by = @(Parse-List $matches[1]) }
}
if ($cur) { $skillEntries += $cur }

$templateEntries = @()
$cur = $null
foreach ($line in (Get-Content $TemplateReg -Raw) -split "`n") {
    if ($line -match '^\s*- id:\s*(.+)') {
        if ($cur) { $templateEntries += $cur }
        $cur = @{ id = $matches[1].Trim(); path = ""; used_by = @() }
    }
    elseif ($cur -and $line -match '^\s*path:\s*(.+)') { $cur.path = $matches[1].Trim() }
    elseif ($cur -and $line -match '^\s*used_by:\s*\[(.*)\]') { $cur.used_by = @(Parse-List $matches[1]) }
}
if ($cur) { $templateEntries += $cur }

$promptIds = @($promptEntries | ForEach-Object { $_.id })
$workflowIds = @($workflowEntries | ForEach-Object { $_.id })
$skillIds = @($skillEntries | ForEach-Object { $_.id })

Write-Pass "Parsed $($promptEntries.Count) prompts, $($workflowEntries.Count) workflows, $($skillEntries.Count) skills, $($templateEntries.Count) templates"

# ─── 5. Prompt frontmatter matches registry ───────

Write-Host "`n── Prompt Frontmatter ──" -ForegroundColor White

$usesSkills = @()
$pairsWith = @()
$fmUsedByWorkflows = @{}

foreach ($p in $promptEntries) {
    $full = Join-Path $RootDir $p.path
    if (-not (Test-Path $full -PathType Leaf)) {
        Write-Fail "Prompt file missing: $($p.id) ($($p.path))"
        continue
    }
    $fm = Get-Frontmatter $full
    if ($fm -eq "") {
        Write-Fail "Prompt '$($p.id)' has no YAML frontmatter"
        continue
    }
    $ok = $true
    foreach ($k in @("id", "version", "status", "layer")) {
        $v = Get-FmValue $fm $k
        if (-not $v -or $v.isList -or $v.value -ne $p[$k]) {
            Write-Fail "Prompt '$($p.id)': frontmatter $k='$($v.value)' != registry '$($p[$k])'"
            $ok = $false
        }
    }
    if ($ok) { Write-Pass "Frontmatter matches registry: $($p.id)" }

    $u = Get-FmValue $fm "uses_skills"
    if ($u -and $u.isList) { $usesSkills += $u.value }
    $pw = Get-FmValue $fm "pairs_with_roles"
    if ($pw -and $pw.isList) { $pairsWith += @{ id = $p.id; roles = $pw.value } }
    $ub = Get-FmValue $fm "used_by_workflows"
    if ($ub -and $ub.isList) { $fmUsedByWorkflows[$p.id] = $ub.value }

    if ($p.layer -eq "repair") {
        $t = Get-FmValue $fm "trigger"
        if ((-not $t) -or $t.isList -or $t.value -eq "") {
            Write-Fail "Repair prompt '$($p.id)' lacks a trigger in frontmatter"
        } elseif ($p.trigger -eq "" -or $p.trigger -ne $t.value) {
            Write-Fail "Repair prompt '$($p.id)': registry trigger='$($p.trigger)' != file '$($t.value)'"
        } else {
            Write-Pass "Repair trigger matches: $($p.id)"
        }
    }
}

# ─── 6. Workflow frontmatter matches registry ─────

Write-Host "`n── Workflow Frontmatter ──" -ForegroundColor White

foreach ($w in $workflowEntries) {
    $full = Join-Path $RootDir $w.path
    if (-not (Test-Path $full -PathType Leaf)) {
        Write-Fail "Workflow file missing: $($w.id) ($($w.path))"
        continue
    }
    $fm = Get-Frontmatter $full
    if ($fm -eq "") {
        Write-Fail "Workflow '$($w.id)' has no YAML frontmatter"
        continue
    }
    $ok = $true
    $fid = Get-FmValue $fm "id"
    if (-not $fid -or $fid.isList -or $fid.value -ne $w.id) {
        Write-Fail "Workflow frontmatter id='$($fid.value)' != registry '$($w.id)' ($($w.path))"
        $ok = $false
    }
    $fcat = Get-FmValue $fm "category"
    if (-not $fcat -or $fcat.isList -or $fcat.value -ne $w.category) {
        Write-Fail "Workflow '$($w.id)': frontmatter category='$($fcat.value)' != registry '$($w.category)'"
        $ok = $false
    }
    $fep = Get-FmValue $fm "entry_point"
    if (-not $fep -or $fep.isList -or $fep.value.ToLower() -ne $w.entry_point) {
        Write-Fail "Workflow '$($w.id)': frontmatter entry_point='$($fep.value)' != registry '$($w.entry_point)'"
        $ok = $false
    }
    $fv = Get-FmValue $fm "version"
    if (-not $fv -or $fv.isList -or $fv.value -notmatch '^\d+\.\d+\.\d+$') {
        Write-Fail "Workflow '$($w.id)' has missing/non-standard frontmatter version"
        $ok = $false
    }
    if ($ok) { Write-Pass "Frontmatter matches registry: $($w.id)" }
}

# ─── 7. prompts_used resolves ─────────────────────

Write-Host "`n── prompts_used Resolution ──" -ForegroundColor White
$sectionFailed = $false

foreach ($w in $workflowEntries) {
    foreach ($ref in $w.prompts_used) {
        if ($promptIds -contains $ref) {
            if ($Verbose) { Write-Pass "$($w.id) -> $ref" }
        } else {
            Write-Fail "Workflow '$($w.id)' references unknown prompt '$ref'"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All prompts_used references resolve" }

# ─── 8. Registry used_by resolves ─────────────────

Write-Host "`n── used_by Resolution ──" -ForegroundColor White
$sectionFailed = $false

foreach ($p in $promptEntries) {
    if ($p.status -eq "deprecated") {
        if ($p.used_by.Count -gt 0) {
            Write-Fail "Deprecated prompt '$($p.id)' must have empty used_by"
            $sectionFailed = $true
        } else {
            Write-Pass "Deprecated prompt unreferenced by design: $($p.id)"
        }
        continue
    }
    if ($p.used_by.Count -eq 0 -and $p.layer -ne "repair") {
        Write-Fail "Active non-repair prompt '$($p.id)' has empty used_by"
        $sectionFailed = $true
        continue
    }
    if ($p.layer -eq "repair" -and $p.used_by.Count -eq 0 -and $p.trigger -eq "") {
        Write-Fail "Repair prompt '$($p.id)' needs used_by entries or a trigger"
        $sectionFailed = $true
        continue
    }
    foreach ($ref in $p.used_by) {
        if (-not (Test-Ref $ref $workflowIds)) {
            Write-Fail "Prompt '$($p.id)' used_by '$ref' matches no workflow"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All registry used_by references resolve" }

foreach ($t in $templateEntries) {
    foreach ($ref in $t.used_by) {
        if (-not (Test-Ref $ref $workflowIds)) {
            Write-Fail "Template '$($t.id)' used_by '$ref' matches no workflow"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All template used_by references resolve" }

# ─── 9. Frontmatter used_by_workflows resolves ────

Write-Host "`n── used_by_workflows Resolution ──" -ForegroundColor White
$sectionFailed = $false

foreach ($id in $fmUsedByWorkflows.Keys) {
    foreach ($ref in $fmUsedByWorkflows[$id]) {
        if (-not (Test-Ref $ref $workflowIds)) {
            Write-Fail "Prompt '$id' frontmatter used_by_workflows '$ref' matches no workflow"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All frontmatter used_by_workflows references resolve" }

# ─── 10. No active prompt orphaned ─────────────────

Write-Host "`n── Orphan Check ──" -ForegroundColor White
$sectionFailed = $false

$referenced = @()
foreach ($w in $workflowEntries) { $referenced += $w.prompts_used }
$referenced = @($referenced | Sort-Object -Unique)

foreach ($p in $promptEntries) {
    if ($p.status -ne "active") { continue }
    if ($referenced -contains $p.id) { continue }
    $covered = $false
    foreach ($ref in $p.used_by) {
        if (Test-Ref $ref $workflowIds) { $covered = $true; break }
    }
    if ($p.layer -eq "repair" -and $p.trigger -ne "") { $covered = $true }
    if (-not $covered) {
        Write-Fail "Active prompt orphaned: $($p.id) (no prompts_used hit, no resolving used_by, no repair trigger)"
        $sectionFailed = $true
    }
}
if (-not $sectionFailed) { Write-Pass "No active prompt is orphaned" }

# ─── 11. Skills cross-check ───────────────────────

Write-Host "`n── Skills ──" -ForegroundColor White
$sectionFailed = $false

$usesSkills = @($usesSkills | Sort-Object -Unique)
foreach ($s in $usesSkills) {
    if ($skillIds -notcontains $s) {
        Write-Fail "Prompt frontmatter uses unknown skill '$s'"
        $sectionFailed = $true
    }
}
foreach ($s in $skillIds) {
    if ($usesSkills -notcontains $s) {
        Write-Warn "Skill '$s' is registered but no prompt declares it in uses_skills"
    }
}
foreach ($s in $skillEntries) {
    foreach ($r in $s.reusable_by) {
        if ($promptIds -notcontains $r) {
            Write-Fail "Skill '$($s.id)' reusable_by unknown prompt '$r'"
            $sectionFailed = $true
        } else {
            $fm = Get-Frontmatter (Join-Path $RootDir (($promptEntries | Where-Object { $_.id -eq $r }).path))
            $u = Get-FmValue $fm "uses_skills"
            if (-not $u -or -not $u.isList -or $u.value -notcontains $s.id) {
                Write-Fail "Skill '$($s.id)' claims reusable_by '$r' but that prompt does not declare it"
                $sectionFailed = $true
            }
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All skills resolve both directions" }

# ─── 12. pairs_with_roles resolves ────────────────

Write-Host "`n── pairs_with_roles ──" -ForegroundColor White
$sectionFailed = $false

foreach ($pw in $pairsWith) {
    foreach ($raw in $pw.roles) {
        # Task frontmatter names roles short (project-planner); the registry
        # id is role.project-planner. Normalize before resolving.
        $r = if ($raw -match '\.') { $raw } else { "role.$raw" }
        if ($promptIds -notcontains $r) {
            Write-Fail "Prompt '$($pw.id)' pairs with unknown role '$raw'"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All pairs_with_roles references resolve" }

# ─── 13. Path references inside .ai resolve ───────

Write-Host "`n── .ai Path References ──" -ForegroundColor White
$sectionFailed = $false

$aiFiles = Get-ChildItem "$RootDir/.ai" -Filter *.md -Recurse -ErrorAction SilentlyContinue
foreach ($f in $aiFiles) {
    $text = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    foreach ($m in [regex]::Matches($text, '(?:\.ai/|templates/|infra/scripts/|registries/|docs/|evaluations/|projects/)[A-Za-z0-9_\-/*.]+')) {
        $ref = $m.Value
        if ($ref -match '\*|NNNN|<|>$|\-$') { continue }          # placeholder or glob
        if ($ref -notmatch '\.(md|ps1|yaml|yml|toml|json)$') { continue }  # bare directory
        $target = Join-Path $RootDir ($ref -replace '/', '\')
        if (-not (Test-Path $target -PathType Leaf)) {
            Write-Fail "Dangling path reference '$ref' in $($f.Name)"
            $sectionFailed = $true
        }
    }
}
if (-not $sectionFailed) { Write-Pass "All concrete .ai path references resolve" }

# ─── Summary ───────────────────────────────────────

Write-Host "`n── Summary ──" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Warnings: $warnCount" -ForegroundColor $(if ($warnCount -gt 0) { "Yellow" } else { "Green" })

if ($failCount -gt 0 -or $warnCount -gt 0) {
    Write-Host "`n  [FAIL] Validation FAILED" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n  [PASS] All registry consistency checks valid" -ForegroundColor Green
    exit 0
}
