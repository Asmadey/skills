# Plan: <issue title> (issue #NNN)

## Context

<Background: what the issue is about, relevant API details, how it fits into the existing SDK structure, any constraints or decisions made upfront>

---

## Files to Create

### 1. `src/...`

<Full class skeleton with namespace, imports, and key method signatures>

### 2. `tests/Unit/...`

<Test class skeleton>

### 3. `tests/Integration/...`

<Integration test class skeleton>

---

## Files to Modify

### 1. `src/Services/ServiceBuilder.php` (or scope builder)

<Exact method to add, line reference if known>

### 2. `phpunit.xml.dist`

<Exact XML block to add>

### 3. `Makefile`

<Exact make target to add>

### 4. `CHANGELOG.md`

<Exact line to add under `## X.Y.Z Unreleased` → `### Added / Fixed / Changed`>

---

## Deptrac compliance

<Confirm which layers the new code depends on and that no new violations are introduced>

---

## Verification

```bash
make lint-cs-fixer
make lint-rector
make lint-phpstan
make lint-deptrac
make test-unit
make test-integration-<scope>
```
