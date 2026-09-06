## Installation

### 1. Codex, Antigravity, Cursor, and other agents

Install any subset of skills or the full repository using the universal skills CLI:

```bash
npx skills@latest add Asmadey/skills
```

The interactive installer lets you pick individual skills and choose which coding agents to configure.

To update installed skills later:

```bash
npx skills@latest update
```

### 2. Claude Code

Install the managed plugin bundle directly:

```bash
claude plugins install asmadey-skills
```

Or from inside an active Claude Code session:

```text
/plugin install asmadey-skills
```

### 3. Local Link (for repository contributors)

To symlink skills directly into your local agent directories:

```bash
bash scripts/link-skills.sh
```
