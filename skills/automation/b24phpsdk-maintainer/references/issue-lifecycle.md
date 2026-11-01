# Issue Lifecycle & Unsupported API Discovery

## Contents
- Issue language rule
- Working with an existing issue
- GitHub CLI fallback
- Creating a new issue
- Discovering unsupported API methods (gap analysis)

---

## Issue language rule

**Rule**: every GitHub issue in `bitrix24/b24phpsdk` — title, body, and checklists — MUST be written in **English only**, regardless of the language used in conversation with the user.

Applies to:
- Creating a new issue (`mcp__github__create_issue`, `gh issue create`)
- Updating an existing issue body or title (`mcp__github__update_issue`)
- Adding issue comments (`mcp__github__add_issue_comment`)

If conversation is in another language, translate the content to English before writing to GitHub. Do not mix languages inside a single issue. Proper nouns (method names, file paths, URLs) stay as-is.

---

## Working with an existing issue

When given an issue number, load it first via `mcp__github__get_issue`:

```yaml
owner: bitrix24
repo: b24phpsdk
issue_number: <N>
```

Read the title, body, and labels — they define scope and context.

---

## GitHub CLI fallback

When `mcp__github__*` tools return authentication errors or are unavailable, use `gh` CLI via `Bash`:

```bash
# Search issues
gh search issues "<query>" --repo bitrix24/b24phpsdk --state open

# List labels
gh label list --repo bitrix24/b24phpsdk

# Create issue
gh issue create --repo bitrix24/b24phpsdk --title "..." --label "..." --body "..."

# Create PR (body MUST follow .github/PULL_REQUEST_TEMPLATE.md)
gh pr create --repo bitrix24/b24phpsdk --title "..." --body "$(cat <<'EOF'
<filled-in template content>
EOF
)" --base <branch>
```

---

## Creating a new issue

Before creating, search via `mcp__github__search_issues` (or `gh search issues` fallback) to verify a similar issue does not exist.
Run `gh label list --repo bitrix24/b24phpsdk` to verify label names.

### Body structure
```markdown
## Problem

<Clear description of the problem or missing functionality>

## Proposed solution

<Description of the proposed solution>

## Acceptance criteria

- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>
```

### Title rules
- New functionality: `Add <feature description>`
- Bug fix: `Fix <what is broken>`
- Refactoring: `Refactor <what and why>`
- Maximum 72 characters

### Labels
| Label | When to use |
|---|---|
| `enhancement` | new functionality |
| `bug` | bug fix |
| `documentation` | documentation only |
| `refactoring` | internal changes without API changes |

---

## Discovering unsupported API methods (gap analysis)

Workflow to identify Bitrix24 REST API methods missing from the SDK and generate tracking issues.

### Step 1 — Select API version
Use `AskUserQuestion`:
- `v3`: REST API v3 — modern endpoints (`tasks.task.*`, `catalog.*`, etc.)
- `v1`: REST API v1 — legacy endpoints

### Step 2 — Scope or pattern filter
Ask whether to narrow search:
- `All scopes`: analyze all methods for version
- `Specific scope`: e.g. `tasks`, `crm`, `calendar`
- `Specific methods`: e.g. `tasks.task.file.*`

### Step 3 — Discover methods from documentation
1. Search via `mcp__bitrix24__bitrix-search`.
2. Inspect details via `mcp__bitrix24__bitrix-method-details`:
   - Exact method name
   - API version (v1 or v3)
   - Deprecation status (skip deprecated methods)
3. Form list **«API methods from docs»**.

### Step 4 — Scan SDK-supported methods
Grep for `ApiEndpointMetadata` in `src/Services/`:
```bash
# Glob: *.php in src/Services/
# Pattern: ApiEndpointMetadata
```
Extract first string argument from `#[ApiEndpointMetadata('method.name', ...)]`.
Form list **«SDK-supported methods»**.

### Step 5 — Compute gap
```
Unsupported = «API methods from docs» − «SDK-supported methods»
```
Present numbered list to the user:
```
Found N unsupported methods:
1. scope.entity.action
2. scope.entity.otheraction
```

### Step 6 — User confirmation
Ask user whether to file issues for:
- All N unsupported methods
- Selected subset (user provides list)

### Step 7 — Deduplicate against existing issues
Search via `mcp__github__search_issues`:
```
q: "<method.name> in:title repo:bitrix24/b24phpsdk is:open"
```
Skip methods with open issues.

### Step 8 — Create issues
Create issue with:
- Labels: `["enhancement"]`
- Title: `Add support for <method.name>`
- Body:
```markdown
## Problem

The Bitrix24 REST API method `<method.name>` is not yet supported by the SDK.

## Proposed solution

Add a service method that wraps `<method.name>` following the existing patterns in `src/Services/<Scope>/Service/`.

## Acceptance criteria

- [ ] Service class implements `<method.name>` with correct parameter mapping
- [ ] Result item `@property-read` annotations cover all response fields
- [ ] Unit test passes (`make test-unit`)
- [ ] Integration test passes, including annotation and type-cast checks
- [ ] `CHANGELOG.md` is updated with an issue link
```
Report created issue URLs.
