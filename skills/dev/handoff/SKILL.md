---
name: handoff
description: "Фиксация и передача контекста текущей сессии (Session Handoff) в компактный чекпоинт-документ (HANDOFF.md) при смене контекста, исчерпании контекстного окна или переключении агентов. Триггеры: 'handoff', 'хэндофф', 'передай контекст', 'сохрани контекст сессии', 'смена смены', 'сдача смены'."
argument-hint: "Для чего будет использоваться следующая сессия?"
category: dev
version: 1.0.0
source: https://github.com/mattpocock/skills
metadata:
  author: Matt Pocock
  framework: Agent Context Preservation & Continuity
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
