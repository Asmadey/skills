---
name: Presentation Frameworks
description: creates developer-friendly presentations using Slidev (Vue/MD) or Reveal.js (HTML/JS) frameworks, strictly adhering to Brand/Black design system.
category: framework
source: https://github.com/slidevjs/slidev, https://github.com/hakimel/reveal.js
version: 2.0.0
last_updated: 2026-02-18
created: 2026-02-08
---

# Presentation Frameworks

## 1. When to use
- **Slidev**: For sophisticated "slides-as-code", live coding, Vue components, and deep customization via UnoCSS.
- **Reveal.js**: For standard HTML/JS presentations, wider browser compatibility without build steps (CDN), or legacy integrations.
- **Brand/Black**: User requests strict adherence to the dark, glossy, premium design system.

## 2. Validation & Prerequisites
- [ ] Check Node.js: `node -v` (Required for Slidev).
- [ ] Check directory structure: `skills/presentation-frameworks/templates/{slidev,revealjs}`.

## 3. Workflow (Checklist)

### Option A: Slidev (Recommended for Devs)
- [ ] **Initialize**: `npm init slidev@latest .`
- [ ] **Apply Theme**: Copy `templates/slidev/*` to project root.
- [ ] **Run**: `npm run dev`

### Option B: Reveal.js (Recommended for Simplicity)
- [ ] **Create Folder**: `mkdir my-deck`
- [ ] **Copy Template**: Copy `templates/revealjs/*` to `my-deck/`.
- [ ] **Run**: Open `index.html` in browser (or serve with `npx serve`).

## 4. Instructions (Degrees of Freedom)

### Heuristics
- Use **Slidev** if the user mentions "Vue", "Component", or "UnoCSS".
- Use **Reveal.js** if the user mentions "HTML", "Legacy", "CDN", or "Lightweight".

### Template Commands

**Slidev Setup**
```bash
# 1. Init
npm init slidev@latest .

# 2. Inject Brand/Black Theme
cp /Users/asmadey/PersonalOS/skills/presentation-frameworks/templates/slidev/uno.config.ts ./
cp -r /Users/asmadey/PersonalOS/skills/presentation-frameworks/templates/slidev/styles ./
cp /Users/asmadey/PersonalOS/skills/presentation-frameworks/templates/slidev/slides.md ./
```

**Reveal.js Setup**
```bash
# 1. Create Directory
mkdir reveal-deck

# 2. Inject Brand/Black Template
cp -r /Users/asmadey/PersonalOS/skills/presentation-frameworks/templates/revealjs/* reveal-deck/
```

## 5. Resources

### Slidev Templates (`templates/slidev`)
- `uno.config.ts`: Brand colors & shortcuts.
- `slides.md`: Markdown structure.

### Reveal.js Templates (`templates/revealjs`)
- `index.html`: Base HTML with CDN imports.
- `theme/black.css`: Custom CSS overrides for Reveal.js default theme.
