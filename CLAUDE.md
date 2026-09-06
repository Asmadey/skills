# Asmadey Skills Repository Guidelines

Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work, architecture, design tokens, PDF parsing, PPTX generation, and system modeling.
- `productivity/`: daily non-code workflow tools, autonomous goal execution, de-slopping, text humanization, second brain, and research.
- `misc/`: kept around for integrations (Telegram, Notion, Airtable, Jira, Linear, Google Workspace) and utilities.
- `in-progress/`: beta: public on purpose, feedback wanted, not shipped in the promoted plugin set.
- `deprecated/`: no longer used or archived.

Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`'s `skills` array. Skills in `misc/`, `in-progress/`, and `deprecated/` must not appear in `plugin.json`.

Install commands are documented in [.agents/install-block.md](./.agents/install-block.md).

## Conventions

- Every `SKILL.md` is either user-invoked (reachable only when explicitly typed by the human, e.g. `/goal`, `/bp`, `/slopmonster`) or model-invoked (model- or user-reachable via triggers).
- Each skill follows the **L1/L2/L3 architecture**:
  - **L1**: Concise YAML frontmatter with specific positive and negative triggers.
  - **L2**: Structured Markdown body with step-by-step workflows and Validation Gates.
  - **L3**: On-demand executable scripts (`scripts/`) and knowledge packets (`resources/`).
- **Security Invariant**: Never commit `.env` files, actual API keys, or personal tokens. Always use environment variable lookups (`process.env` / `os.getenv`).

To link all promoted skills into your local agent directories (`~/.claude/skills`, `~/.agents/skills`), run:

```bash
bash scripts/link-skills.sh
```

To list all skills by category with current counts:

```bash
bash scripts/list-skills.sh
```
