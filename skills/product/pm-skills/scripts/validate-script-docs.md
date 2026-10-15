# validate-script-docs.sh / validate-script-docs.ps1

## Purpose

Ensure every `.sh`/`.ps1` script pair in `scripts/` has a companion `.md`
documentation file. Enforces the convention that scripts ship with
human-readable documentation explaining purpose, usage, and behavior.

## Usage

```bash
./scripts/validate-script-docs.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-script-docs.ps1
```

## What It Does

1. Scans `scripts/` for all `.sh` and `.ps1` files
2. Extracts unique base names (e.g., `build-release` from `build-release.sh`
   and `build-release.ps1`)
3. For each base name, checks that `scripts/{base}.md` exists
4. Also verifies `scripts/README_SCRIPTS.md` exists
5. Reports any missing documentation files

## Convention

Every script pair follows:
```
scripts/foo.sh       ← bash implementation
scripts/foo.ps1      ← PowerShell implementation
scripts/foo.md       ← companion documentation (covers both)
```

The `.md` file should include: Purpose, Usage (bash + PS examples), What It
Does, Exit Codes, When to Use, and Safety notes.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All script pairs have companion `.md` files |
| `1` | One or more script pairs are missing documentation |

## When to Use

- In CI on every push/PR (catches undocumented scripts before merge)
- After adding a new script pair
- Before release (verify documentation completeness)

## Example Output

```
PASS: All 12 script pairs have companion .md files
```

```
FAIL: Missing companion doc: scripts/check-workflow-coverage.md
       Has: check-workflow-coverage.sh
       Has: check-workflow-coverage.ps1

FAIL: 1 script pair(s) missing companion .md documentation
  Convention: scripts/foo.sh + scripts/foo.ps1 → scripts/foo.md
```

## Safety

Read-only. Does not modify any files.
