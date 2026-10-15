# validate-gitignore-pm-skills.sh / validate-gitignore-pm-skills.ps1

## Purpose

Ensure `_pm-skills/` is listed in `.gitignore`. The `_pm-skills/` directory
holds local state (update reports, backups) created by the
`/update-pm-skills` skill. Without a `.gitignore` entry, users could
accidentally commit local state to the repo.

## Usage

```bash
./scripts/validate-gitignore-pm-skills.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-gitignore-pm-skills.ps1
```

## What It Does

1. Reads `.gitignore`
2. Checks for a line matching `^_pm-skills/` or `^_pm-skills$`
3. Reports pass or fail

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | `_pm-skills/` is in `.gitignore` |
| `1` | Entry missing, or `.gitignore` not found |

## When to Use

- In CI on every push/PR (advisory initially)
- After editing `.gitignore`

## Example Output

```
PASS: _pm-skills/ is in .gitignore
```

```
FAIL: _pm-skills/ is not in .gitignore
  Add '_pm-skills/' to .gitignore to prevent committing local state
```

## Safety

Read-only. Does not modify any files.
