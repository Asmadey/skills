# validate-script-docs.ps1
# Ensures every .sh/.ps1 script pair in scripts/ has a companion .md file.
# Convention: scripts/foo.sh + scripts/foo.ps1 → scripts/foo.md

$ErrorActionPreference = "Stop"

$scriptsDir = "scripts"
$missing = 0
$checked = 0

# Build list of unique script base names
$bases = @()
Get-ChildItem "$scriptsDir" -File | Where-Object {
    $_.Extension -in '.sh', '.ps1'
} | ForEach-Object {
    $base = $_.BaseName
    if ($base -ne "README_SCRIPTS") {
        $bases += $base
    }
}

$uniqueBases = $bases | Sort-Object -Unique

foreach ($base in $uniqueBases) {
    $checked++
    $docFile = Join-Path $scriptsDir "$base.md"
    if (-not (Test-Path $docFile)) {
        Write-Host "FAIL: Missing companion doc: $docFile"
        if (Test-Path (Join-Path $scriptsDir "$base.sh")) {
            Write-Host "       Has: $base.sh"
        }
        if (Test-Path (Join-Path $scriptsDir "$base.ps1")) {
            Write-Host "       Has: $base.ps1"
        }
        $missing++
    }
}

# Also check README_SCRIPTS.md
if (-not (Test-Path (Join-Path $scriptsDir "README_SCRIPTS.md"))) {
    Write-Host "FAIL: Missing $scriptsDir/README_SCRIPTS.md"
    $missing++
}

if ($missing -eq 0) {
    Write-Host "PASS: All $checked script pairs have companion .md files"
    exit 0
} else {
    Write-Host ""
    Write-Host "FAIL: $missing script pair(s) missing companion .md documentation"
    Write-Host "  Convention: scripts/foo.sh + scripts/foo.ps1 -> scripts/foo.md"
    exit 1
}
