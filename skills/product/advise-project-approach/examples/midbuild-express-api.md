# Example: Mid-Build Express API

## Prompt

```text
I'm halfway through building a task manager API in Node.js/Express. I've got routes and a MongoDB connection working but no auth, no tests, and I'm not sure if my folder structure will scale.
```

## Expected Skill Behavior

- Select **mid-build course correction** mode because the user says they are already building.
- Mark evidence status as **description only** unless a repo or code sample is provided.
- Avoid pretending to inspect files.
- Prioritize auth, authorization/ownership rules, validation, integration tests, and a structure that makes route behavior testable.
- Avoid prescribing folder structure as a fashion preference; explain the maintainability reason.
- Explain what would change if the app is personal-only, multi-user, team-facing, or production-bound.

## Good Output Shape

```text
## Project Approach Review: Node.js Task Manager API

### TL;DR
Keep or adjust the stack, then name the most important course correction.

### Evidence Reviewed
- Commands run: none
- Files inspected: none
- External references: official Express security docs, testing docs, comparable API patterns
- Evidence status: description only

### Recommended Changes
High priority items should focus on auth/ownership, validation, tests, and error handling.

### Stack and Architecture Verdict
State whether Express + MongoDB is still appropriate and when it stops being appropriate.
```
