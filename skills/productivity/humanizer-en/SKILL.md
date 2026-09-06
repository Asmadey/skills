---
name: Humanizer (en)
description: Removes signs of AI-generated writing to produce natural, human-sounding text. Based on Wikipedia's AI Cleanup guidelines.
category: knowledge
source: https://github.com/blader/humanizer
version: 2.5.1
last_updated: 2026-04-04
---

# Humanizer: Anti-AI Writing System

This skill identifies and removes "statistical tells" of AI-generated text, replacing them with natural, opinionated, and varied human prose.

## 1. When to Use
- **Trigger**: Editing or reviewing AI-generated content (markdown, essays, emails, docs).
- **Trigger**: When text feels "sterile," "formulaic," or "too perfect."
- **Trigger**: When matching a specific author's voice is required.

## 2. Validation & Prerequisites
- [ ] **Context Loading**: Verify `references/patterns.md` is loaded for pattern matching.
- [ ] **Voice Sample**: Check if a writing sample is provided (optional but recommended).
- [ ] **Original Text**: Ensure the source text is clearly defined.

## 3. Humanization Workflow

1. **Voice Analysis** (Optional): If a sample exists, use `references/voice-matching.md`.
2. **Pattern Scanning**: Check against the 29 patterns in `references/patterns.md`.
3. **Rewrite Pass**: Apply "Personality and Soul" rules (see below).
4. **Validation Audit**: Run the "What makes this obviously AI?" pass.
5. **Final Refinement**: Polish based on the audit results.

## 4. Personality and Soul (Heuristics)
*Stop being "helpful" and start being "human."*

- **Have Opinions**: Don't neutrally list pros/cons. React to them. ("I'm not sure I buy this argument...")
- **Vary Rhythm**: Mix short, punchy sentences with longer, flowing ones.
- **Acknowledge Complexity**: Humans have mixed feelings. AI has "balanced perspectives."
- **Use "I" (when fit)**: First-person perspective signals a real thinking subject.
- **Let the Mess In**: Tangents and half-formed thoughts are human; perfect structure is algorithmic.
- **Simple Copulas**: Prefer "is/are" over "serves as," "represents," or "stands as."

## 5. Validation Gates (MANDATORY)

> [!IMPORTANT]
> You MUST check these after every rewrite.

- **Gate 1: The "Actually" Check**: Did you use excessive AI words? (Check `references/patterns.md#7`).
- **Gate 2: The -ing Test**: Are there dangling present participle phrases? (Check `references/patterns.md#3`).
- **Gate 3: The Audit Pass**: Did you ask yourself "What makes this still look like AI?" before finishing?
- **Gate 4: The Rhythm Check**: Read it aloud. Does it sound like a robot or a person in a coffee shop?

## 6. Resources
- [Patterns (29 Tells)](references/patterns.md)
- [Voice Matching Guide](references/voice-matching.md)
- [Refinement Examples](references/examples.md)
- [Original Resource (WARP)](resources/WARP.md)
- [Project Background](references/wiki-source.md)
