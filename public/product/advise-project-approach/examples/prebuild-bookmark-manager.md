# Example: Pre-Build Bookmark Manager

## Prompt

```text
I want to build a self-hosted bookmark manager with tagging, full-text search, and a browser extension. Solo developer, comfortable with Python and basic React. What's the best way to approach this?
```

## Expected Skill Behavior

- Select **pre-build strategy** mode because no repo, code, or URL was provided.
- Treat the user's description as the source of truth and list assumptions.
- Research direct comparables such as linkding, Linkwarden, and LinkAce.
- Verify time-sensitive claims like stars, release dates, and last commits at review time.
- Recommend a stack based on the user's Python skill, self-hosting goal, and personal/small-scale use case.
- Explain when the recommendation becomes wrong, for example if collaboration, archiving, multi-user scale, or rich SPA workflows become core requirements.

## Good Output Shape

```text
## Project Approach: Self-Hosted Bookmark Manager

### TL;DR
Recommend a Python-first, low-ops architecture and name the main tradeoff.

### Project Frame
Goal, users, constraints, assumptions, success criteria, and evidence status.

### Comparable Projects and References
Verified public projects and docs with dates or adoption signals.

### Recommended Stack
Backend, database/search, frontend, browser extension, auth, deployment, testing.

### Architecture Direction
Single-app architecture with clear extension API and search/indexing path.

### Alternatives Considered
Heavier full-stack app, lighter Flask/FastAPI option, and managed/search-service option.

### Build Plan
First vertical slice, search/tagging, browser extension, deployment hardening.
```
