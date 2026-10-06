# Docs gates: relative-link scan + current-focus freshness.
# Mirrors the Docs job in .github/workflows/ci.yml so local runs and CI
# execute the same checks. Exit 0 when all gates pass, 1 otherwise.
# ASCII only: do not add unicode banners (PS 5.1 needs a BOM for those).

$ErrorActionPreference = "Continue"
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$fail = 0

# --- Gate 1: no broken relative .md links under docs/ (excluding archive) ---
$mdFiles = Get-ChildItem -Path (Join-Path $repoRoot "docs") -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch "docs.plan.archive" }
$linkPattern = '\]\(([^)#][^)]*\.md[^)]*)\)'
foreach ($file in $mdFiles) {
    $dir = Split-Path -Parent $file.FullName
    $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) { continue }
    foreach ($m in [regex]::Matches($content, $linkPattern)) {
        $link = $m.Groups[1].Value -replace '#.*$', ''
        if ($link -match '^https?://') { continue }
        $target = Join-Path $dir $link
        if (-not (Test-Path -LiteralPath $target)) {
            Write-Host ("BROKEN LINK in {0} -> {1}" -f $file.FullName, $link)
            $fail = 1
        }
    }
}
if ($fail -eq 0) { Write-Host "link_scan: OK" } else { Write-Host "link_scan: FAIL" }

# --- Gate 2: current-focus.md stamp no older than 8 days ---
$focus = Join-Path $repoRoot "docs\tracking\current-focus.md"
$focusFail = 0
$text = Get-Content -LiteralPath $focus -Raw
if ($text -match '\*\*Last updated:\*\*\s+(\d{4}-\d{2}-\d{2})') {
    $stamp = [datetime]::ParseExact($Matches[1], "yyyy-MM-dd", $null)
    $age = ((Get-Date).Date - $stamp.Date).Days
    Write-Host ("current-focus.md stamped {0} ({1} days old)" -f $Matches[1], $age)
    if ($age -gt 8) {
        Write-Host "FRESHNESS FAIL: older than 8 days"
        $focusFail = 1
    }
} else {
    Write-Host "FRESHNESS FAIL: no 'Last updated:' stamp found"
    $focusFail = 1
}
if ($focusFail -eq 0) { Write-Host "freshness: OK" }
if ($focusFail -eq 1) { $fail = 1 }

exit $fail
