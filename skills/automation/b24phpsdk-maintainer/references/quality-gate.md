# Post-Implementation Quality Gate

## Contents
- Quality gate overview
- Phase 1: Light checks (linters and unit tests)
- Phase 2: Heavy checks (integration tests)
- Mandatory completion invariant
- Reporting format

---

## Quality gate overview

After writing all files and marking the issue plan complete, run validation in two sequential phases. **Do not run Phase 2 until Phase 1 passes completely.**

---

## Phase 1: Light checks (linters and unit tests)

Execute commands in strict order:

```bash
make lint-cs-fixer
make lint-rector
make lint-phpstan
make lint-deptrac
make test-unit
```

Rules:
- If any check fails, diagnose root causes before patching.
- Do NOT add classes to `deptrac.yaml` `skip_violations`. Fix namespace boundaries or dependency directions.
- All 5 commands must return exit code 0 before proceeding to Phase 2.

---

## Phase 2: Heavy checks (integration tests)

Run the scope-specific integration suite:

```bash
make test-integration-<scope>
```

Rules:
- Never skip, suppress, or comment out failing integration tests.
- Verify both live API payload mapping and type assertions.

---

## Mandatory completion invariant

Every completed task MUST run `make lint-rector` before reporting completion or submitting a PR. This invariant applies regardless of whether the change was large or a targeted single-file fix.

---

## Reporting format

Report quality gate results using the standardized block:

```markdown
## Test plan

- [x] `make lint-cs-fixer` — passed
- [x] `make lint-rector` — passed
- [x] `make lint-phpstan` — passed
- [x] `make lint-deptrac` — passed
- [x] `make test-unit` — passed
- [x] `make test-integration-<scope>` — passed
```
