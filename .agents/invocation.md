# Skill Invocation Philosophy

Skills in this repository are divided along a single explicit axis: **who can invoke them**.

## 1. User-invoked Skills

- **Who invokes:** The human engineer, by typing an explicit slash command (e.g. `/goal`, `/bp`, `/slopmonster`, `/second-brain`).
- **Role:** Orchestration, alignment, and high-agency workflow initiation.
- **Rule:** A user-invoked skill may call model-invoked skills as building blocks, but never another user-invoked skill.

## 2. Model-invoked Skills

- **Who invokes:** The model automatically when contextual triggers match (e.g., encountering a bug, analyzing a PDF, designing an interface, reviewing code), OR the user on demand.
- **Role:** Reusable discipline, domain-specific standards, automated pipelines, and strict verification checkpoints.
- **Rule:** Model-invoked skills contain sharp negative triggers ("Do NOT activate when...") to prevent context dilution.
