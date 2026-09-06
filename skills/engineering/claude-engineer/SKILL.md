---
name: Claude Engineer
description: Multi-agent autonomous software engineering harness. Use when you need long-running autonomous coding sessions with project management (Linear), version control (GitHub), and team communication (Slack). Orchestrates specialized subagents - Linear Agent, Coding Agent, GitHub Agent, Slack Agent. Enables extended sessions without context exhaustion. Requires Arcade MCP gateway for OAuth authentication.
category: integration
source: https://github.com/coleam00/your-claude-engineer
version: latest
last_updated: 2026-02-18
created: 2026-02-08
---

# Claude Engineer

**Your own AI software engineer that manages projects, writes code, and communicates progress — autonomously.**

## Overview

Multi-agent harness built on Claude Agent SDK that turns Claude into a long-running software engineer capable of tackling complex, multi-step tasks.

### Key Capabilities

| Agent | Responsibility |
|-------|---------------|
| **Orchestrator** | Coordinates all agents, manages workflow |
| **Linear Agent** | Creates/tracks issues, updates status |
| **Coding Agent** | Writes, tests, iterates on code |
| **GitHub Agent** | Commits, branches, opens PRs |
| **Slack Agent** | Progress updates to team |

---

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy and edit environment
cp .env.example .env

# Required variables:
# - ARCADE_API_KEY: https://api.arcade.dev/dashboard/api-keys
# - ARCADE_GATEWAY_SLUG: https://api.arcade.dev/dashboard/mcp-gateways
# - ARCADE_USER_ID: Your email

# Authorize (once)
python authorize_arcade.py
```

### 3. Run

```bash
# Basic usage
python autonomous_agent_demo.py --project-dir my-app

# With Linear project
python autonomous_agent_demo.py --project-dir my-app --linear

# Continue previous session
python autonomous_agent_demo.py --project-dir my-app --continue
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│              ORCHESTRATOR               │
│  (Coordinates workflow, manages state)  │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│Linear │  │Coding │  │GitHub │  │ Slack │
│Agent  │  │Agent  │  │Agent  │  │ Agent │
└───────┘  └───────┘  └───────┘  └───────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
                    │
            ┌───────▼───────┐
            │  Arcade MCP   │
            │   Gateway     │
            └───────────────┘
```

---

## File Structure

```
claude-engineer/
├── SKILL.md                    # This file
├── agent.py                    # Main agent harness
├── autonomous_agent_demo.py    # Demo entry point
├── client.py                   # Anthropic client wrapper
├── agents/
│   ├── definitions.py          # Agent definitions
│   └── orchestrator.py         # Orchestrator logic
├── prompts/
│   ├── orchestrator_prompt.md  # System prompt for orchestrator
│   ├── coding_agent_prompt.md  # Coding agent instructions
│   ├── linear_agent_prompt.md  # Linear integration
│   ├── github_agent_prompt.md  # GitHub integration
│   ├── slack_agent_prompt.md   # Slack notifications
│   └── example_app_specs/      # Example specifications
├── arcade_config.py            # Arcade MCP configuration
├── authorize_arcade.py         # OAuth authorization
├── security.py                 # Security guardrails
└── requirements.txt            # Python dependencies
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ARCADE_API_KEY` | Arcade API key | Yes |
| `ARCADE_GATEWAY_SLUG` | MCP gateway slug | Yes |
| `ARCADE_USER_ID` | Your email | Recommended |
| `GITHUB_REPO` | `owner/repo` for auto-push | No |
| `SLACK_CHANNEL` | Channel for notifications | No |
| `ORCHESTRATOR_MODEL` | haiku/sonnet/opus | No |
| `CODING_AGENT_MODEL` | Model for coding | No |

---

## Integration with Superpowers Workflow

This skill enhances the Superpowers workflow:

1. **Brainstorming** → Define app specification
2. **Writing Plans** → Store in `prompts/app_spec.txt`
3. **Claude Engineer** → Autonomous execution with subagents
4. **Code Review** → Review generated PRs

### Example Workflow

```bash
# 1. Define spec
cat > prompts/app_spec.txt << 'EOF'
Build a REST API with user authentication...
EOF

# 2. Run autonomous agent
python autonomous_agent_demo.py \
  --project-dir user-auth-api \
  --linear \
  --slack

# 3. Monitor in Slack, review PRs in GitHub
```

---

## Prompt Templates

### Agent Prompts Location

- `prompts/orchestrator_prompt.md` — Main coordinator
- `prompts/coding_agent_prompt.md` — Code generation
- `prompts/linear_agent_prompt.md` — Issue tracking
- `prompts/github_agent_prompt.md` — Version control
- `prompts/slack_agent_prompt.md` — Notifications

### Customizing Prompts

Edit prompts to match your project conventions, coding standards, and workflow preferences.

---

## Limitations

- ⚠️ **Not Windows compatible** (use WSL or Linux VM)
- Requires Arcade account for MCP gateway
- Long-running sessions consume tokens

---

## Related Skills

- `superpowers/writing-plans` — Create specifications for the agent
- `superpowers/subagent-driven-development` — Similar multi-agent pattern
- `code-reviewer` — Review agent-generated code

---

## Resources

- [Claude Agent SDK](https://github.com/anthropics/claude-code/tree/main/agent-sdk-python)
- [Arcade MCP](https://arcade.dev)
- [Original Repository](https://github.com/coleam00/your-claude-engineer)
