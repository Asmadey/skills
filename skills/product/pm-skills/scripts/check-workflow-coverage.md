# check-workflow-coverage.sh / check-workflow-coverage.ps1

## Purpose

Verify that every workflow source file in `_workflows/` has matching entries
across the repo: a generated docs page, an AGENTS.md entry, and an mkdocs.yml
nav entry. Prevents new workflows from shipping without full cross-reference
coverage.

## Usage

```bash
./scripts/check-workflow-coverage.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-workflow-coverage.ps1
```

## What It Does

1. Lists all `_workflows/*.md` files (excluding `README.md` and files starting with `_`)
2. For each workflow, derives the slug (e.g., `feature-kickoff` from `feature-kickoff.md`)
3. Checks that these exist:
   - `docs/workflows/{slug}.md` (generated page)
   - An entry containing the workflow slug in `AGENTS.md`
   - An entry referencing `workflows/{slug}.md` in `mkdocs.yml`
4. Reports missing entries
5. Advisory section: lists which workflows have matching commands (not required)

## Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | All workflows are fully covered |
| `1`  | One or more workflows are missing entries |

## When to Use

- After adding a new workflow to `_workflows/`
- After editing `AGENTS.md` or `mkdocs.yml` navigation
- In CI to catch incomplete workflow additions

## Example Output

```
=== Workflow Coverage Check ===

Found 9 workflow(s) in _workflows/

--- Advisory: Workflow command coverage ---
  [OK] commands/workflow-feature-kickoff.md
  [OK] commands/workflow-customer-discovery.md
  [--] commands/workflow-lean-startup.md (not found - optional)

PASS: All 9 workflows have full coverage.
```

```
=== Workflow Coverage Check ===

Found 10 workflow(s) in _workflows/

[FAIL] Missing generated page: docs/workflows/new-workflow.md
[FAIL] mkdocs.yml: no entry for workflows/new-workflow.md

FAIL: One or more workflows are missing entries.
```

## Safety

Read-only. Does not modify any files.
