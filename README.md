# ⚡ Asmadey's Agent Skills

[![skills.sh](https://skills.sh/b/Asmadey/skills)](https://skills.sh/Asmadey/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Asmadey/skills?style=social)](https://github.com/Asmadey/skills)

A curated collection of production-grade agent skills for **AI engineering, architecture, autonomous execution, and high-agency productivity**.

These skills are designed to override LLM performance biases (such as AI laziness, generic code templates, and robotic hallucinations), grounding agents in strict engineering disciplines, verifiable mathematical models, and authentic human voice standards.

Compatible with **Claude Code, Codex, Antigravity, Cursor, and any Agent Skills CLI environment**.

---

## 🚀 Quick Setup (30-Second Installation)

Pick the installation philosophy that fits your workflow:

### 1. Universal Skills CLI (Recommended for Codex, Antigravity, Cursor)

Install individual skills or the entire repository using the universal skills package manager:

```bash
npx skills@latest add Asmadey/skills
```

The interactive selector lets you pick the exact skills you want and automatically configures your target AI harness.

To pull updates later:

```bash
npx skills@latest update
```

---

### 2. Claude Code Plugin

Install the managed plugin bundle directly into Claude Code:

```bash
claude plugins install asmadey-skills
```

Or from inside an active Claude Code session:

```text
/plugin install asmadey-skills
```

---

### 3. Local Link (For Contributors & Pair-Programmers)

To symlink skills directly into your local agent directories (`~/.claude/skills` and `~/.agents/skills`):

```bash
git clone https://github.com/Asmadey/skills.git
cd skills
bash scripts/link-skills.sh
```

---

## 🏛 Core Architecture Principles

1. **Progressive Disclosure (L1 / L2 / L3):**
   - **Level 1 (Metadata):** Sharp YAML frontmatter with exact positive and negative triggers (prevents context dilution and token waste).
   - **Level 2 (Workflow):** Human-readable Markdown body defining execution steps and strict Validation Gates.
   - **Level 3 (Resources):** Executable deterministic scripts (`scripts/`) and deep knowledge packets (`resources/`), loaded on demand.
2. **Zero-Hallucination Mathematics:**
   - Financial, economic, and quantitative models are executed via specialized Python engines rather than left to LLM token prediction.
3. **Anti-AI-Slop Protocol:**
   - Strict linguistic and stylistic linters that eliminate robotic cliché patterns, unearned jargon, and synthetic tells.

---

## 📚 Complete Skills Reference

Skills split on one axis: **who can invoke them**.
- **User-invoked:** reachable when explicitly typed by the human engineer as slash-commands (orchestration and strategic control).
- **Model-invoked:** reachable autonomously by the agent upon matching task triggers, or called explicitly.

---

### 🛠 1. Engineering & Technical Architecture (`skills/engineering/`)

Skills used for daily code work, systems architecture, design tokens, PDF parsing, PPTX generation, and technical modeling.

#### User-invoked

- **[biznes-plan-architect](./skills/engineering/biznes-plan-architect/SKILL.md)**: Institutional business plan and financial model architect (CAPEX, OPEX, P&L, Cash Flow, NPV, IRR, BEP).
- **[claude-md-writer](./skills/engineering/claude-md-writer/SKILL.md)**: Context optimizer supporting a 3-tier modular documentation system for CLAUDE.md and AGENTS.md.

#### Model-invoked

- **[neuroarxiv](./skills/engineering/neuroarxiv/SKILL.md)**: Grounds architecture and algorithmic decisions in real arXiv prior art before building new systems.
- **[pdf-parsing](./skills/engineering/pdf-parsing/SKILL.md)**: Structured text, table, and data extraction from PDF documents into Markdown.
- **[pptx-generator](./skills/engineering/pptx-generator/SKILL.md)**: Programmatic generation of professional presentations, carousels, and pitch decks.
- **[presentation-frameworks](./skills/engineering/presentation-frameworks/SKILL.md)**: Interactive slide creation using code-based frameworks (Slidev, Reveal.js).
- **[design-md](./skills/engineering/design-md/SKILL.md)**: Single source of truth for design tokens, visual constraints, and design-system rules.
- **[frontend-design](./skills/engineering/frontend-design/SKILL.md)**: Creative UI engine avoiding AI template sameness and generic components.
- **[taste-skill](./skills/engineering/taste-skill/SKILL.md)**: Senior UI engineering standards delivering Apple- and Vercel-grade visual polish.
- **[ui-ux-pro-max](./skills/engineering/ui-ux-pro-max/SKILL.md)**: Encyclopedia of 50+ UI styles, palettes, font pairings, and responsive patterns.
- **[web-design-guidelines](./skills/engineering/web-design-guidelines/SKILL.md)**: Accessibility, performance, and UX audit against modern Web standards.
- **[shadcn](./skills/engineering/shadcn/SKILL.md)**: Production component engineering using Shadcn UI, Radix primitives, and Tailwind CSS.
- **[claude-engineer](./skills/engineering/claude-engineer/SKILL.md)**: Deep software engineering workflows, disciplined refactoring, and test-driven architecture.
- **[code-reviewer](./skills/engineering/code-reviewer/SKILL.md)**: Two-axis code review evaluating both repo standards adherence and issue specification fidelity.
- **[rust-development](./skills/engineering/rust-development/SKILL.md)**: High-performance Rust programming idioms, safety patterns, and Cargo workflows.
- **[supabase-postgres-best-practices](./skills/engineering/supabase-postgres-best-practices/SKILL.md)**: Production PostgreSQL schema design, indexing, RLS security policies, and Supabase integration.

---

### 🎯 2. Productivity & High-Agency Execution (`skills/productivity/`)

General workflow tools, autonomous goal tracking, de-slopping, text humanization, second brain, and market intelligence.

#### User-invoked

- **[goal-buddy](./skills/productivity/goal-buddy/SKILL.md)**: Autonomous goal orchestration engine (Goal Oracle, Scout/Worker/Judge roles, state.yaml Kanban).
- **[slop-monster](./skills/productivity/slop-monster/SKILL.md)**: Multi-pass AI-slop elimination, cliché linting with `deslop.py`, and rival-model cleansing.
- **[second-brain](./skills/productivity/second-brain/SKILL.md)**: Dynamic LLM Wiki Engine for Obsidian (graph queries, cross-linking, synthesis).
- **[book-to-skill](./skills/productivity/book-to-skill/SKILL.md)**: Converts full books, papers, and long-form documents into structured agent skills.
- **[skill-creator](./skills/productivity/skill-creator/SKILL.md)**: Skills Librarian Agent that turns cloned repos and raw scripts into standardized skills.
- **[find-skills](./skills/productivity/find-skills/SKILL.md)**: Discovers, evaluates, and installs agent skills for any requested capability.

#### Model-invoked

- **[humanizer-ru](./skills/productivity/humanizer-ru/SKILL.md)**: Rewrites Russian drafts into natural, human-sounding speech free of AI bureaucratic jargon.
- **[humanizer-en](./skills/productivity/humanizer-en/SKILL.md)**: Humanizes English copy preserving personal tone and eliminating ChatGPT voice tells.
- **[watermarks-remover](./skills/productivity/watermarks-remover/SKILL.md)**: Strips invisible AI watermarks, zero-width Unicode characters, and synthetic metadata.
- **[simple-english](./skills/productivity/simple-english/SKILL.md)**: Rewrites complex English into clear, concise, punchy prose.
- **[slop-detector](./skills/productivity/slop-detector/SKILL.md)**: Audits text for telltale AI markers, repetition loops, and syntactical tells.
- **[brand-voice](./skills/productivity/brand-voice/SKILL.md)**: Calibrates and locks in consistent brand personality and copywriting tone.
- **[prd-taskmaster](./skills/productivity/prd-taskmaster/SKILL.md)**: Decomposes complex Product Requirement Documents into bite-sized traceable tasks.
- **[geo-seo-claude](./skills/productivity/geo-seo-claude/SKILL.md)**: Geographic and local search engine optimization strategies.
- **[tavily-intelligence](./skills/productivity/tavily-intelligence/SKILL.md)**: Real-time, noise-free AI search and web extraction.
- **[yandex-search-api](./skills/productivity/yandex-search-api/SKILL.md)**: Deep search across the Russian web via official Yandex Search API.
- **[yandex-wordstat](./skills/productivity/yandex-wordstat/SKILL.md)**: Search volume, query frequency, and keyword demand analytics.
- **[yandex-metrika](./skills/productivity/yandex-metrika/SKILL.md)**: Analytics tracking, goal conversion, and user behavior auditing.

---

### 🔌 3. Integrations & Utilities (`skills/misc/`)

Automations and SaaS connectors for managing external services and communication channels.

- **[telegram-automation](./skills/misc/telegram-automation/SKILL.md)**: Telegram bot management, broadcasts, and notification dispatching.
- **[notion-automation](./skills/misc/notion-automation/SKILL.md)**: Notion database query, page generation, and workspace synchronization.
- **[airtable-automation](./skills/misc/airtable-automation/SKILL.md)**: Reading, writing, and filtering tabular records in Airtable bases.
- **[jira-automation](./skills/misc/jira-automation/SKILL.md)**: Jira ticket automation, backlog management, and sprint issue transitions.
- **[linear-automation](./skills/misc/linear-automation/SKILL.md)**: Issue triage, label management, and workflow automation in Linear.
- **[google-calendar-automation](./skills/misc/google-calendar-automation/SKILL.md)**: Event scheduling, meeting coordination, and agenda management.
- **[google-drive-automation](./skills/misc/google-drive-automation/SKILL.md)**: Cloud file organization, uploads, downloads, and permission audits.
- **[googlesheets-automation](./skills/misc/googlesheets-automation/SKILL.md)**: Advanced Google Spreadsheet reading, formatting, and batch calculations.
- **[youtube-downloader](./skills/misc/youtube-downloader/SKILL.md)**: Video, audio, and transcript extraction from YouTube URLs.
- **[youtube-automation](./skills/misc/youtube-automation/SKILL.md)**: Channel content management, metadata optimization, and publishing workflows.
- **[anticaptcha-solver-rest](./skills/misc/anticaptcha-solver-rest/SKILL.md)**: Automated CAPTCHA solving (reCAPTCHA, hCaptcha, Turnstile) via REST API.
- **[activecampaign-automation](./skills/misc/activecampaign-automation/SKILL.md)**: Contact CRM tagging, email marketing, and automation funnels.
- **[confluence-automation](./skills/misc/confluence-automation/SKILL.md)**: Confluence space management, documentation syncing, and knowledge base ops.
- **[connect-apps](./skills/misc/connect-apps/SKILL.md)**: Unified multi-service gateway connecting AI to Gmail, Slack, and GitHub.
- **[vercel-automation](./skills/misc/vercel-automation/SKILL.md)**: Frontend cloud deployment, environment variable management, and domain routing.
- **[whatsup](./skills/misc/whatsup/SKILL.md)**: Operations and health monitoring status check utility.

---

### 🧪 4. In-Progress & Beta (`skills/in-progress/`)

Experimental skills under active development:

- **[synthetic-personas](./skills/in-progress/synthetic-personas/SKILL.md)**: High-fidelity user persona generation for behavioral simulation.
- **[synthetic-exploration](./skills/in-progress/synthetic-exploration/SKILL.md)**: Hypothesis validation by simulating agent persona interactions.
- **[growth-expert](./skills/in-progress/growth-expert/SKILL.md)**: Growth hacking, conversion rate optimization, and pricing experiments engine.
- **[banner-design](./skills/in-progress/banner-design/SKILL.md)**: Automated design and layout generation for marketing banners.
- **[html5-banner](./skills/in-progress/html5-banner/SKILL.md)**: Animated HTML5 responsive banners with CSS/JS timelines.
- **[static-banner](./skills/in-progress/static-banner/SKILL.md)**: High-impact static visual banner compositions.
- **[notte-web-agent](./skills/in-progress/notte-web-agent/SKILL.md)**: Headless browser automation with unified perception layers.
- **[agent-swarm](./skills/in-progress/agent-swarm/SKILL.md)**: Parallel multi-agent task execution and swarm coordination.
- **[optiblog-ai](./skills/in-progress/optiblog-ai/SKILL.md)**: End-to-end SEO article generation and content pipeline.

---

## 📜 Repository Management

- **List all skills by category:**
  ```bash
  npm run list
  ```
- **Symlink all skills into local agent directories:**
  ```bash
  npm run link
  ```

---

## 📄 License

MIT License. Copyright (c) 2026 Asmadey. See [LICENSE](./LICENSE) for details.
