---
name: b24phpsdk-maintainer
description: "Maintainer tools and workflows for bitrix24/b24phpsdk (OpenAPI schema refresh, code generators, issue lifecycle, TDD implementation, quality gates, and release PRs). Use when working on GitHub issues, adding Bitrix24 REST API endpoints, generating result items or builders, preparing release PRs, or updating CHANGELOG in bitrix24/b24phpsdk. Differentiator: strictly enforces SDK v3 architecture, AbstractAnnotatedItem contracts, Deptrac boundaries, and 2-phase quality gates."
metadata:
  category: automation
  version: 3.0.0
  last_updated: 2026-09-21
---

# b24phpsdk Maintainer

Target Repository: **bitrix24/b24phpsdk** (`owner: bitrix24`, `repo: b24phpsdk`)

This skill orchestrates the end-to-end development and maintenance lifecycle for the official Bitrix24 PHP SDK following Progressive Disclosure (L1 discovery → L2 workflow orchestration → L3 domain references).

---

## On Skill Invocation: Refresh OpenAPI Schema

**Required**: before executing any workflow or writing code, rebuild the OpenAPI schema:

```bash
make oa-schema-build
```

This synchronizes `docs/open-api/openapi.json` with the current Bitrix24 REST API contract. Do not proceed until this command completes with exit code 0.

---

## Core Issue Implementation Checklist

When tasked with resolving or closing an issue (`#NNN`), execute these steps in strict sequence:

```
Issue Lifecycle Checklist:
- [ ] 1. Load issue: fetch title, body, and labels via GitHub MCP or `gh` CLI
- [ ] 2. Expand API context: query bitrix24 MCP tools for exact method parameters & payloads
- [ ] 3. Classify issue: determine if `feature` (enhancement) or `bugfix` (bug)
- [ ] 4. Confirm API version: ask user (`v3` -> `v3-dev`, `v1` -> `dev`) via AskUserQuestion
- [ ] 5. Branch checkout: create `<type>/<issue-number>-<short-slug>` from target base
- [ ] 6. Task plan creation: initialize `.tasks/<issue-number>/plan.md` from template
- [ ] 7. Architecture review: check generators, AbstractAnnotatedItem & Deptrac rules
- [ ] 8. TDD implementation: write failing unit/integration tests before production code
- [ ] 9. Quality gate: run Phase 1 (light linters) + Phase 2 (integration suite)
- [ ] 10. Release & PR: update CHANGELOG.md, push branch, create PR, and monitor CI
```

---

## Step-by-Step Execution Protocol

### 1. Load Issue Details
Read the issue via `mcp__github__get_issue` (or `gh search issues` fallback). All issue discussions, plans, and commits must be in **English only**.
> See [references/issue-lifecycle.md](references/issue-lifecycle.md)

### 2. Fetch Documentation & Payloads
Query official Bitrix24 API documentation using:
- `mcp__bitrix24__bitrix-search` / `mcp__bitrix24__bitrix-method-details`
- Verify exact method name, v1 vs v3 differences, parameter types, and response envelope (`result` vs `result.item` vs `result.items`).
> See [references/implementation-conventions.md](references/implementation-conventions.md)

### 3. Determine Base Branch & Checkout
Branch off according to target API version:
- REST v3 (modern): base branch `v3-dev`
- REST v1 (legacy): base branch `dev`
- *Note for cross-version bugfixes*: implement on `v3-dev` first, merge, then backport to `dev`.
```bash
git checkout <base-branch> && git pull
git checkout -b <type>/<issue-number>-<short-slug>
```
> See [references/release-and-git.md](references/release-and-git.md)

### 4. Create Task Plan File
Create directory `.tasks/<issue-number>/` and file `.tasks/<issue-number>/plan.md`.
Use template from [resources/templates/issue-plan-template.md](resources/templates/issue-plan-template.md).
Self-review the plan against 3 gates before user presentation:
1. **Unambiguity**: exact paths, classes, and method signatures specified.
2. **Non-contradiction**: test skeletons match production class signatures.
3. **No gaps**: all acceptance criteria mapped to steps; `make lint-rector` included.

### 5. Code Generators & Response Classes
Before manually coding SDK classes, invoke relevant code generators:
- Result items: `php bin/console b24-dev:result-item-generator <method.name> --stage=all`
- Select builders: `php bin/console b24-dev:generate-select-builder ...`
- Item builders: `php bin/console b24-dev:generate-item-builder ...`
- All service `*ItemResult` classes MUST extend `Bitrix24\SDK\Core\Result\AbstractAnnotatedItem`.
> See [references/code-generators.md](references/code-generators.md)

### 6. Widget Placements (If Applicable)
When adding widget placement locations (`placement.list`), bind/unbind facades, or option builders:
> See [references/placements.md](references/placements.md)

### 7. Run 2-Phase Quality Gate
Do not commit or open a PR until both phases pass:

**Phase 1 (Light checks):**
```bash
make lint-cs-fixer
make lint-rector
make lint-phpstan
make lint-deptrac
make test-unit
```

**Phase 2 (Heavy integration checks):**
```bash
make test-integration-<scope>
```
> See [references/quality-gate.md](references/quality-gate.md)

### 8. PR Creation, CHANGELOG & CI Monitoring
1. Update `CHANGELOG.md` under `## X.Y.Z Unreleased` with issue link.
2. Push branch: `git push -u origin <branch-name>`
3. Read `.github/PULL_REQUEST_TEMPLATE.md` fresh from disk and open PR against `<base-branch>`.
4. Poll CI status with `gh pr checks <PR number> --watch` until complete.
> See [references/release-and-git.md](references/release-and-git.md)

---

## Domain Reference Index (L3)

| Reference Document | Scope & Contents |
|---|---|
| [references/code-generators.md](references/code-generators.md) | Console generators, response contract reuse, `AbstractAnnotatedItem` |
| [references/issue-lifecycle.md](references/issue-lifecycle.md) | English issue rules, GitHub CLI fallback, discovery of unsupported methods |
| [references/implementation-conventions.md](references/implementation-conventions.md) | Date/time typing (`CarbonImmutable`), field metadata services, curl webhooks |
| [references/quality-gate.md](references/quality-gate.md) | Phase 1 & 2 verification commands, `lint-rector` invariant, reporting format |
| [references/release-and-git.md](references/release-and-git.md) | Branching, commit format, release API coverage tables in CHANGELOG, CI polling |
| [references/placements.md](references/placements.md) | Placement codes, typed scope facades, localization DTOs, option builders |
| [resources/templates/issue-plan-template.md](resources/templates/issue-plan-template.md) | Blueprint for `.tasks/<issue-number>/plan.md` |
