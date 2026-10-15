# validate-gitignore-pm-skills.ps1
# Ensures _pm-skills/ is in .gitignore so local state (update reports,
# backups) is never accidentally committed.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".gitignore")) {
    Write-Host "FAIL: .gitignore not found"
    exit 1
}

# Read line-by-line to avoid CRLF regex issues with -Raw
$lines = Get-Content ".gitignore"

if ($lines | Where-Object { $_ -match '^_pm-skills(/?)$' }) {
    Write-Host "PASS: _pm-skills/ is in .gitignore"
    exit 0
} else {
    Write-Host "FAIL: _pm-skills/ is not in .gitignore"
    Write-Host "  Add '_pm-skills/' to .gitignore to prevent committing local state"
    exit 1
}
