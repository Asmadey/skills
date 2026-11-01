# Git Conventions, PR Protocol & Release API Coverage

## Contents
- Git branching conventions
- Git commit message conventions
- Cross-version bugfixes (v3-dev vs dev)
- Release PR: mandatory API coverage in CHANGELOG
- Pull Request creation protocol
- Polling CI status
- Pushing to existing PRs & finishing branches

---

## Git branching conventions

Branch off the correct base branch depending on API version:

| Target API version | Base branch |
|---|---|
| REST API v3 (modern) | `v3-dev` |
| REST API v1 (legacy) | `dev` |

Branch naming format:
```
feature/<issue-number>-<short-slug>   # For new features
bugfix/<issue-number>-<short-slug>    # For bug fixes
```

Example: `feature/397-add-task-chat-fields`

---

## Git commit message conventions

Use imperative mood, describe changes, and cite the issue number:

```
Add <ClassName> service for `<scope>.<entity>.*` support (#NNN)
Fix <what was broken> in <component> (#NNN)
```

Rules:
- Capital letter at the start
- No period at the end
- Maximum 72 characters
- Do **not** use Conventional Commits prefixes (`feat:`, `fix:`) — the project does not use them

---

## Cross-version bugfixes (v3-dev vs dev)

When a fix or field addition affects **both** 3.x and 1.x release lines:
1. Implement the fix on a branch created from **`v3-dev`** first.
2. Open and merge the PR against `v3-dev`.
3. Backport the change to `dev` via a separate branch and PR against `dev`.
4. Rationale: `v3-dev` is the forward-moving release line; keeping it fixed first prevents regressions in future releases.

---

## Release PR: mandatory API coverage in CHANGELOG

When preparing or updating a **release** pull request, append `### API coverage` as the last subsection of the release entry in `CHANGELOG.md`.

### Measurement commands
```bash
make -s oa-schema-build
make -s sdk-coverage-v3-show
make -s sdk-coverage-v1-show
```

Verify counts from overall summary:
- Total > 0
- 0 <= covered <= total
- covered + uncovered = total
- percentage = covered / total * 100 (rounded to 2 decimal places)

### Markdown table format
```markdown
### API coverage

Measured on <YYYY-MM-DD> (UTC) from the release candidate.

| REST API | Covered methods | Total methods | Uncovered methods | Coverage | Basis |
|---|---:|---:|---:|---:|---|
| v3 (new) | <covered> | <total> | <uncovered> | <percent>% | OpenAPI snapshot: `docs/open-api/openapi.json` |
| v1 (legacy) | <covered> | <total> | <uncovered> | <percent>% | Methods available on the configured portal |

These figures describe SDK method coverage against each baseline, not test coverage or proof that every method was exercised against a live portal.
```

---

## Pull Request creation protocol

Run only after both phases of the quality gate pass and `CHANGELOG.md` is updated.

### Rules
- Open the PR automatically via `mcp__github__create_pull_request` or `gh pr create`. Do not output manual creation URLs.
- Always read `.github/PULL_REQUEST_TEMPLATE.md` fresh before writing the PR description.
- Include the test plan and plain-text `Closes #<issue-number>` at the end of the PR body.

```bash
# Push branch
git push -u origin <branch-name>

# Compose body and create PR
gh pr create --repo bitrix24/b24phpsdk \
  --title "<issue title>" \
  --base <base-branch> \
  --body "$(cat <<'EOF'
<filled template>

## Test plan

- [x] `make lint-cs-fixer` — passed
- [x] `make lint-rector` — passed
- [x] `make lint-phpstan` — passed
- [x] `make lint-deptrac` — passed
- [x] `make test-unit` — passed
- [x] `make test-integration-<scope>` — passed

Closes #<issue-number>
EOF
)"
```

---

## Polling CI status

After creating a PR or pushing commits to an existing PR, poll CI status until all checks complete:

```bash
gh pr checks <PR number> --repo bitrix24/b24phpsdk --watch
```

Wait ~60 seconds between polling calls. Report the final green/red status to the user.

---

## Pushing to existing PRs & finishing branches

- Any push to an existing branch must be accompanied by CI monitoring.
- When finishing a development branch in an interactive prompt, select option 2 (Push and create Pull Request) directly.
