---
name: Heroes GPT Strategy Standard
description: Полный стратегический стандарт (v7.0). Включает весь цикл от анализа (JTBD, Journey Map) до генерации новых офферов, Challenge-тестов и Приоритетной Матрицы внедрения.
category: framework
source: Behavioral Strategy + Landing Analysis
version: 7.0
dependencies: [JTBD Standard 2.0, Firecrawl MCP]
last_updated: 2026-02-18
created: 2026-02-08
---

# Heroes GPT Strategy Standard (v7.0)

## 🔄 Workflow Diagram

```ascii
HeroesGPT Landing Analysis Workflow

📥 INPUT STAGE
├─ Landing URL / Content
├─ Business Context (type, goals)
├─ Target Audience Info (if available)
└─ Analysis Depth (quick / full / focused)

🔍 PREPROCESSING STAGE
├─ Content Extraction
│  ├─ All text elements (headers, body, CTAs)
│  ├─ Visual elements with text
│  ├─ Meta information
│  └─ Technical elements (forms, buttons)
└─ Initial Classification
   ├─ Business type identification
   ├─ Primary offering categorization
   └─ Audience signals detection

📊 CORE ANALYSIS STAGE
├─ Pre-evaluation Offer Inventory
│  ├─ INPUT: All extracted text/offers
│  ├─ PROCESS: Categorize each offer by type (WITHOUT benefit/tax evaluation)
│  │  ├─ Quantitative promises (numbers, metrics)
│  │  ├─ Qualitative benefits (skills, outcomes)
│  │  ├─ Social proof elements (testimonials, stats)
│  │  ├─ Risk reducers / guarantees (money-back, support)
│  │  ├─ Urgency / scarcity signals (limited time / spots)
│  │  └─ Process promises (how it works)
│  ├─ **Reflections**: все ли офферы извлечены? корректна ли категоризация?
│  └─ OUTPUT: Clean offer inventory with types only
│
├─ JTBD Scenario Generation
│  ├─ INPUT: Analyzed offers + business context
│  ├─ PROCESS: Map offers to user jobs
│  │  ├─ Big JTBD (8–12 primary scenarios)
│  │  ├─ Medium JTBD (supporting scenarios)
│  │  ├─ Small JTBD (micro-moments)
│  │  ├─ Functional jobs (what user does)
│  │  ├─ Emotional jobs (what user feels)
│  │  └─ Social jobs (how user appears)
│  ├─ **Reflections**: соответствие количеству JTBD? логична ли иерархия?
│  └─ OUTPUT: Prioritized JTBD table with frequency/impact
│
├─ Segment Definition & Fear Analysis
│  ├─ INPUT: JTBD scenarios
│  ├─ PROCESS: Define segments → Map desires → Identify fears
│  │  ├─ Segment characteristics & pain points
│  │  ├─ Segment Desire Mapping (what each wants to achieve)
│  │  ├─ Segment Fear Analysis (primary/secondary fears)
│  │  ├─ JTBD frequency per segment
│  │  ├─ Viral potential assessment
│  │  └─ Priority ranking (1–5 stars)
│  ├─ **Reflections**: чётко ли определены сегменты? выявлены ли страхи?
│  └─ OUTPUT: Segment–Fear–Desire matrix
│
├─ Authentic Segment Reality Check (3.5)
│  └─ Проверка реальности сегментов и их применимости
│
├─ Decision Journey Mapping
│  ├─ INPUT: Segments + current content
│  ├─ PROCESS: Map content to decision stages
│  │  ├─ B2C Journey (8 stages, 5 sec – 10 min)
│  │  │  ├─ Problem Recognition (5–15 sec)
│  │  │  ├─ Solution Possibility (15–30 sec)
│  │  │  ├─ Personal Relevance (30–60 sec)
│  │  │  ├─ Feasibility Assessment (1–2 min)
│  │  │  ├─ Social Validation (2–3 min)
│  │  │  ├─ Risk Evaluation (3–5 min)
│  │  │  ├─ Urgency Assessment (5–10 min)
│  │  │  └─ Action Simplification (moment)
│  │  └─ B2B Journey (8 stages, committee decisions)
│  │     ├─ Business Impact Recognition
│  │     ├─ Solution–Problem Fit
│  │     ├─ Internal Champion Preparation
│  │     ├─ Stakeholder Alignment
│  │     ├─ Risk Mitigation Planning
│  │     ├─ Budget Justification
│  │     ├─ Implementation Feasibility
│  │     └─ Vendor Reliability Assessment
│  ├─ **Reflections**: покрыты ли все этапы B2C и B2B? учтены тайминги?
│  └─ OUTPUT: Stage-by-stage content gaps with timing
│
├─ Decision Minefield Detection
│  ├─ INPUT: Decision journey gaps + current content
│  ├─ PROCESS: Identify psychological blockers
│  │  ├─ Decision Fatigue Mines (>7±2 choices)
│  │  ├─ Present Bias Mines (future vs immediate value)
│  │  ├─ Status Quo Bias Mines (change resistance)
│  │  ├─ Regret Avoidance Mines (wrong choice fear)
│  │  ├─ Social Proof Vacuum Mines (no peer examples)
│  │  └─ Cognitive Load Overflow (complexity overload)
│  ├─ **Reflections**: проверены ли все 6 типов мин?
│  └─ OUTPUT: Specific mines with mitigation strategies
│
├─ New Offer Generation
│  ├─ INPUT: Segment gaps + JTBD scenarios + fear analysis
│  ├─ PROCESS: Design new offers per segment (address JTBD + fears)
│  │  ├─ Segment-specific new offers
│  │  ├─ JTBD scenario targeting
│  │  ├─ Fear reduction validation
│  │  └─ Narrative coherence check
│  ├─ **Reflections**: адресуют ли офферы JTBD? снижают ли страхи? проверена ли coherence?
│  └─ OUTPUT: Segment-specific new offer recommendations
│
├─ Protocol Challenge Analysis
│  ├─ INPUT: All previous analyses
│  ├─ PROCESS: Multi-perspective evaluation
│  │  ├─ Skeptical user perspective
│  │  ├─ Competitor comparison angle
│  │  ├─ Different segment viewpoints
│  │  └─ Contrarian arguments
│  ├─ **Reflections**: рассмотрены ли альтернативные точки зрения?
│  └─ OUTPUT: Challenge-based insights & blind spots
│
SYNTHESIS STAGE
├─ Priority Matrix Creation
│  ├─ Impact vs Effort scoring (1–5 scale)
│  ├─ Time-based categorization (Week 1 / Week 2)
│  └─ Role assignment (Designer / Copywriter / Developer)
│
├─ Actionable Task Generation
│  ├─ Quick Wins (low effort, high impact)
│  ├─ Strategic Improvements (high effort, high impact)
│  └─ Long-term optimizations
│
└─ Implementation Readiness Check
   ├─ Resource requirement validation
   ├─ Technical feasibility assessment
   └─ Success metrics definition

📤 OUTPUT STAGE
├─ Structured Report Generation
├─ Self-Validation Checklist Execution
├─ Quality Score Calculation (target: 85+/100)
└─ Implementation Timeline with Owners
```

## 1. When to use
- Используй этот стандарт при любой команде `/lp` или запросе на анализ лендинга.
- Цель: Качество стратегии ≥ 85/100.

## 2. Detailed Instructions

*0.* Extraction Strategy Selection
1. **Analyze URL Type:**
   - Если это **Landing Page** (Tilda, LPgenerator, Single Page) -> Используй `Mode A`.
   - Если это **Corporate Site** (Много страниц, разделы Pricing, About) -> Используй `Mode B`.

#### Mode A: Landing Scan (Fast)
- Tool: `firecrawl_scrape`
- Params: `url: {URL}`, `onlyMainContent: false`

#### Mode B: Business Deep Dive (Thorough)
- Tool: `firecrawl_crawl`
- Params: `url: {URL}`, `limit: 5`, `maxDiscoveryDepth: 1`, `scrapeOptions: { onlyMainContent: false }`

2. **Preservation:**
   - Сохрани результат (Markdown) в `Reports HeroesGPT/{Domain}/{Date}_Source.md`.

*1.* Inventory
- Выпиши минимум 20-50 офферов.
- **Reflection:** все ли офферы извлечены? корректна ли категоризация?

*2.* JTBD
- Раздели на Big/Medium/Small/Emotional/Social jobs.
- **Reflection:** соответствие количеству JTBD? логична ли иерархия?

*3.* Segments & Fears
- Определи сегменты, их желания и страхи.
- **Reflection:** чётко ли определены сегменты? выявлены ли страхи?

*4.* Journey Mapping
- Сопоставь контент с этапами принятия решения (B2C/B2B).
- **Reflection**: покрыты ли все этапы? учтены тайминги?

*5.* Decision Minefield
- Найди психологические барьеры (Fatigue, Status Quo, и т.д.).
- **Reflection**: проверены ли все 6 типов мин?

*6.* New Offer Generation
На основе найденных страхов (Step 3) и провалов в пути (Step 4), сгенерируй новые офферы:
- Они должны закрывать конкретный JTBD.
- Они должны снижать выявленный страх.
- **Reflection**: адресуют ли офферы JTBD? снижают ли страхи? проверена ли coherence?

*7.* Protocol Challenge (Адвокат Дьявола)
Проверь свои выводы:
- Скептик: "Это все маркетинг, где доказательства?"
- Конкурент: "У нас дешевле и функций больше".
- **Reflection**: рассмотрены ли альтернативные точки зрения?

*8.* Priority Matrix & Synthesis
Создай таблицу приоритетов:
- Quick Wins: Высокий эффект / Мало усилий.
- Strategy: Высокий эффект / Много усилий.
- Backlog: Малый эффект.

*10.* Output & Quality Check
- Выполни финальный чек-лист валидации.
- Рассчитай Quality Score.

## 3. Output Format

📑 **1. Таблица анализа офферов (Inventory)**
(Минимум 20-50 позиций).

💡 **2. New Offers & Recommendations**
| Сегмент | Проблема/Страх | Новый Оффер (Solution) | JTBD Target |
| :--- | :--- | :--- | :--- |
| ... | ... | ... | ... |

📊 **3. Implementation Priority Matrix**
| Task (Что сделать) | Impact (1-5) | Effort (1-5) | Role | Timeline |
| :--- | :--- | :--- | :--- | :--- |
| Изменить H1 | 5 | 1 | Copywriter | Week 1 |

🛡 **4. Challenge Report**
- Blind Spots identified: ...
- Mitigation: ...

---
**Путь сохранения отчета:** `Reports HeroesGPT/{Domain_Name}/{YYYY-MM-DD}_Analysis.md`
**Путь сохранения исходника:** `Reports HeroesGPT/{Domain_Name}/{YYYY-MM-DD}_Source.md`
