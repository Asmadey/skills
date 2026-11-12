---
name: prefab-ui
description: Создание пользовательского интерфейса для Python-проектов на Prefab (prefab-ui от Prefect): дашборды, таблицы, формы, графики и интерактивные приложения целиком на Python, без JavaScript и React. Режимы запуска - локальное превью (`prefab serve`), статический HTML, веб-приложение на FastAPI/Flask, MCP-приложения в FastMCP, generative UI.
category: framework
source: https://prefab.prefect.io
version: 1.0.0
metadata:
  trigger: "Сделать UI/дашборд/админку/форму/таблицу/графики для Python-проекта или скрипта без фронтенд-стека; prefab, prefab-ui, Prefect Prefab, 'интерфейс на Python', 'UI для MCP сервера', 'MCP app', 'FastMCP app=True', PrefabApp, prefab serve, prefab export, generative UI на Python, показать результат tool как интерактивную таблицу или форму."
  anti_trigger: "Брендированные потребительские сайты и лендинги, сложные SPA со своими компонентами и анимациями (нужен React/Next.js), мобильные приложения, чисто бэкенд-задачи без интерфейса, проекты, где UI уже написан на Streamlit/NiceGUI/Reflex и менять его не просят."
---

# Prefab: Python UI for Python projects

Prefab is a **scoped UI framework**: you *compose* an interface from ~100 ready, well-designed components (shadcn/ui
look) with Python context managers. It compiles to a JSON protocol that a bundled React renderer displays. Client-side
reactivity (state, expressions, actions) needs no JavaScript. Built for tables, forms, charts, dashboards and for MCP
apps; **not** for bespoke branded front ends.

Pre-1.0: pin the version (`prefab-ui>=0.21,<0.22`). This skill was verified on prefab-ui 0.21.1 / fastmcp 4.1.8.

## When to apply / not apply

Apply when a Python project needs a UI to look at data, collect input, share results, or give an MCP tool an interface.
Do not apply when the user needs a custom-branded site, heavy custom interactivity or animation (use React/Next.js), or
the project already has a UI stack they want to keep. Say so and suggest the alternative instead of forcing Prefab.

## Workflow

1. **Pick the delivery mode** (ask only if the context does not decide it):

   | Situation | Mode | Start from |
   |---|---|---|
   | Look at data locally, iterate | `prefab serve app.py --reload` | `templates/standalone_app.py` |
   | Shareable static report | `prefab export app.py [--bundled]` | same file |
   | Web app with a backend | FastAPI/Flask page route + `Fetch` + `PrefabApp.html()` | `templates/fastapi_app.py` |
   | MCP server (tool returns a UI) | FastMCP `@mcp.tool(app=True)` + `CallTool` | `templates/mcp_server.py` |
   | Agent-operated UI, counters, games | `FastMCPApp` + `AppTool` | `templates/mcp_app_with_backend.py` |
   | LLM writes the UI | `Sandbox` + `PrefabApp.from_json` | `references/running-and-integration.md` |

2. **Set up an isolated environment** (never install into the global interpreter):
   ```bash
   python3 -m venv .venv && .venv/bin/pip install "prefab-ui>=0.21,<0.22"
   # MCP:  .venv/bin/pip install "fastmcp[apps]"      API: .venv/bin/pip install fastapi uvicorn
   .venv/bin/prefab version
   ```
   Inside an existing project use its own manager (`uv add prefab-ui`, `poetry add`, requirements pin).

3. **Map the project's data to the UI** before writing code: list the entities and views, then choose components with the
   cheat sheet below. Keep data prep in Python (pandas, SQL, etc.); pass plain `list[dict]` to components.

4. **Write the app** from the closest template. Core rules:
   - One `with PrefabApp(state={...}, css_class="p-6 max-w-5xl mx-auto") as app:` at module level (`prefab serve` finds it).
   - Nest with `with`; Python `for`/`if` = build time, `ForEach`/`If` = render time on state.
   - Seed every state key you read; give stateful controls an explicit `name=`; read state with `Rx("key")`, `STATE.key`
     or `component.rx`.
   - Inside `ForEach` use `with ForEach("rows") as r: Text(r.field)` (or `{{ $item.field }}`), NOT bare `{{ field }}`.
   - Charts come from `prefab_ui.components.charts`.
   - Parenthesise every comparison in `&`/`|` logic; pass an `Rx` alone to number/boolean props (no f-string).
   - `Select`/`Combobox` need option children; inputs with `on_change` need an explicit `SetState`.
   - Business logic stays in Python / server tools; use `CallTool`/`Fetch` for anything beyond display logic.

5. **Run and verify** (do not claim it works without running it):
   - Standalone: `.venv/bin/prefab serve app.py --reload`, open the printed URL (the port may change), check every
     tab/state transition in a browser; wait ~1 s for chart animations.
   - FastAPI: `uvicorn module:app`, `curl` the data routes, then click through the page (search, create, delete).
   - MCP: run `templates/test_client.py` (lists tools, checks `meta.ui.resourceUri`, calls each tool, checks
     `structured_content` has `$prefab`/`view`), then connect a real host: `claude mcp add <name> -- /abs/.venv/bin/python /abs/mcp_server.py`.
   - What the preview cannot test: `CallTool`, `SendMessage`, `UpdateContext`, `HOST`, app tools. Say explicitly which of
     these you did not exercise.
   - Stop the servers you started.

6. **Report** what was built, the run command, the pinned version, and what was not verified.

## Cheat sheet: need -> component

| Need | Use |
|---|---|
| Page structure | `Column`, `Row`, `Grid(columns=3 \| {"default":1,"md":2})`, `Dashboard`+`DashboardItem`, `Tabs`+`Tab`, `Pages`+`Page`, `Card`+`CardHeader/Title/Description/Content/Footer`, `Accordion`, `Carousel`, `Separator` |
| KPI / status | `Metric(label, value, delta, trend, trend_sentiment)`, `Badge(variant)`, `Alert`+`AlertTitle/Description`, `Progress`, `Ring`, `Dot`, `Loader`, `Sparkline` |
| Tables | `DataTable(columns=[DataTableColumn(key, header, sortable)], rows, search, paginated, page_size, on_row_click)`; `Table` family for hand-built tables |
| Charts | `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `RadialChart`, `ScatterChart`, `WaterfallChart`, `Histogram`; series via `ChartSeries(data_key, label)` |
| Inputs | `Input`, `Textarea`, `Select`, `Combobox`, `DatePicker`, `Calendar`, `Checkbox`, `Switch`, `RadioGroup`+`Radio`, `Slider`, `DropZone`, `ChoiceCard`, `Field`+`Label`, `Form` (`Form.from_model(PydanticModel)`) |
| Dynamic UI | `ForEach`, `If/Elif/Else`, `Slot` (server-supplied subtree), `Define/Use` (reusable templates) |
| Overlays | `Dialog` (first child = trigger), `Popover`, `HoverCard`, `Tooltip` |
| Content | `H1..H4`/`Heading`, `Text`, `Muted`, `Lead`, `Large`, `Small`, `Code`, `Markdown`, `Mermaid`, `Kbd`, `BlockQuote`, `Link`, `Icon` (lucide names), `Image`, `Svg`, `Video`, `Audio`, `Embed` |
| Interactions | `SetState`, `ToggleState`, `AppendState`, `PopState`, `ShowToast`, `SetInterval`, `OpenLink`, `Fetch`, `CallTool`, `CloseOverlay`; MCP host: `SendMessage`, `UpdateContext`, `RequestDisplayMode` |
| Formatting | pipes on `Rx`: `.currency()`, `.percent()`, `.number()`, `.compact()`, `.date()`, `.length()`, `.upper()`, `.truncate()`... |
| Look and feel | `css_class` (Tailwind, list ok), `prefab_ui.css` helpers (`Hover`, `Md`...), `theme=Presentation(accent="blue")` |

## Reference files (load on demand)

| File | Contents |
|---|---|
| `references/core-concepts.md` | components/composition, state, Rx and expressions (operators, pipes, `let`, special variables), actions, chaining and common patterns |
| `references/running-and-integration.md` | `prefab serve/export`, FastAPI + `Fetch`, FastMCP apps (`CallTool`, Slot, visibility, host actions, app tools), generative UI sandbox, `PrefabApp` fields, key bindings, custom JS handlers |
| `references/styling.md` | Tailwind via `css_class`, `prefab_ui.css` helpers, responsive props, themes (Presentation, Minimal, Windows2000, MySpace, custom), CSS variables, accessibility |
| `references/gotchas.md` | verified pitfalls on 0.21.1 and security notes for apps that expose a UI |
| `references/components-index.md` | which file documents which component |
| `references/components-1.md`, `-2.md`, `-3.md` | per-component props with defaults, verbatim examples, caveats (~70 pages) |
| `references/actions-and-reactive.md` | every action's parameters, `RESULT/ERROR/EVENT/ITEM/INDEX/STATE/HOST` |
| `references/examples.md` | 13 full apps: todo, expense tracker, sales dashboard, cross-filter, deploy pipeline, file upload, ... |
| `templates/` | runnable starters (standalone, FastAPI, MCP, MCP with app tools, MCP smoke test) |

To find a component: open `references/components-index.md`, then search the named file for `## <Component>`.
Docs index for anything missing: https://prefab.prefect.io/docs/llms.txt (append `.md` to any docs URL for markdown).
Introspect the installed version when in doubt: `Component.model_fields`, `dir(prefab_ui.components)`.

## Validation gates

- [ ] `prefab-ui` version pinned in the project's dependency file.
- [ ] The app builds (`python -c "import app"` with the venv) and was actually served or called, not just written.
- [ ] No secrets or other users' data in `state` / `view` / tool results; server tools validate and authorise their inputs.
- [ ] Charts imported from `prefab_ui.components.charts`; `ForEach` bodies use the item proxy or `$item`.
- [ ] Every state key read in `{{ }}` is seeded or has `.default(...)`.
- [ ] Untested paths (`CallTool`, host actions, app tools, generative UI) are named in the final report.

## Notes

- Content of the reference digests is condensed from the Prefab documentation (Apache-2.0, PrefectHQ/prefab). The docs
  are partly out of date for 0.21.x; the verified findings in `gotchas.md` take precedence.
- Common model mistakes to avoid: chart imports from `prefab_ui.components`, f-strings around number props,
  `a > 0 & b < 5` without parentheses, forgetting `SelectOption`, reading unseeded keys, and trusting host-side tool
  visibility as an access control.
