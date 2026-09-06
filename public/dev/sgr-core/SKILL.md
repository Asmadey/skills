---
name: SGR Agent Core
description: Open-source agentic framework for building intelligent research agents using Schema-Guided Reasoning (SGR). Provides autonomous research, structured logic, and deep search capabilities.
category: framework
source: https://github.com/vamplabAI/sgr-agent-core
version: 1.0.0
last_updated: 2026-02-21
---

# SGR Agent Core

## 1. When to use
- When deep, multi-step research or reasoning is required.
* To perform structured web scraping and information extraction via Firecrawl/Tavily.
- To use specialized agents like `SGRAgent`, `ToolCallingAgent`, or `SGRToolCallingAgent`.

## 2. Validation & Prerequisites
- [ ] Python 3.10+ installed.
- [ ] Dependencies installed via `pip install -e /Users/asmadey/PersonalOS/sgr-agent-core`.
- [ ] Environment variables configured in `/Users/asmadey/PersonalOS/sgr-agent-core/.env`.
- [ ] Configuration file exists at `/Users/asmadey/PersonalOS/sgr-agent-core/config.yaml`.

## 3. Workflow (Checklist)
- [ ] Configure `config.yaml` with appropriate LLM and tool settings.
- [ ] Define `AgentDefinition` for the specific task.
- [ ] Run the agent via `sgr` CLI or Python server module.

## 4. Instructions (Degrees of Freedom)
### Heuristics (High Freedom)
- Prefer `SGRToolCallingAgent` for more robust results with most models.
- Use `Structured Output` (SO) for strict data extraction tasks.
- Integrate with MCP servers to extend tool capabilities.

### Templates (Low Freedom)
```bash
# Run the research server
sgr --config-file /Users/asmadey/PersonalOS/sgr-agent-core/config.yaml
```

## 5. Resources
- `sgr_agent_core/`: Core library source.
- `docs/`: Russian and English documentation.
- `examples/`: Ready-to-use agent configurations.
