# Example: Post-Build FastAPI Template Review

## Prompt

```text
Review this completed full-stack FastAPI template before I use it for a SaaS project.
```

## Expected Skill Behavior

- Select **post-build review** mode if the user provides a repo, folder, or GitHub URL and frames it as completed or launch-ready.
- Inspect local files or public repo evidence before making file-level claims.
- Distinguish "this is a good template" from "this is right for this user's product, team, and scale."
- Check backend, frontend, tests, CI/deploy, auth, config, secrets handling, generated clients, database/migrations, and operational defaults.
- Recommend what to keep, what to simplify, and what to harden before shipping.

## Good Output Shape

```text
## Project Approach Review: Full-Stack FastAPI Template

### TL;DR
Give a verdict that separates template quality from project fit.

### Evidence Reviewed
Commands, files, external references, and evidence status.

### What Is Working
Concrete strengths backed by files.

### Gap Analysis
Gaps relative to the intended SaaS use case, not generic "best practices."

### Recommended Changes
High/medium/low priority changes with expected impact.

### Stack and Architecture Verdict
Keep, adjust, or reconsider, including migration and operational tradeoffs.
```
