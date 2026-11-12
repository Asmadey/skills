# Gotchas and verified findings (prefab-ui 0.21.1, fastmcp 4.1.8)

Items marked **(verified)** were reproduced by running the code; the rest come from the docs.

## Things that bite

1. **`ForEach` item fields (verified).** In 0.21.1 bare `{{ name }}` / `{{ dept }}` inside `ForEach` rendered EMPTY even
   though older docs show it. These work:
   ```python
   with ForEach("team") as p:                 # item proxy: p.name, p.dept, p.get_index()
       Text(f"{p.name} / {p.dept}")
   with ForEach("todos") as (i, t):           # (index, item) unpacking
       Button("x", on_click=PopState("todos", i))
   Text("{{ $item.name }} / {{ $index }}")    # explicit special variables
   ```
   Re-test the bare form after upgrading; prefer the explicit forms.
2. **Chart imports.** `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `RadialChart`, `ScatterChart`,
   `WaterfallChart`, `Sparkline`, `ChartSeries` live in `prefab_ui.components.charts`, NOT in `prefab_ui.components`
   (`from prefab_ui.components import *` does not give them; `Histogram` is in `components`). Most common LLM mistake.
3. **Props are strictly typed (pydantic).** `Svg(width=40)` fails: use `width="40"`. A bad prop raises at build time
   with the field name: read the traceback, fix the type.
4. **Options are children.** `Select` needs `SelectOption(value=..., label=...)` children and `Combobox` needs
   `ComboboxOption`; without them the control is empty (verified: the state still shows the seeded value).
5. **Seed every state key you read.** Undefined sole-value template -> literal `{{ key }}` text; boolean props get the
   truthy string (`disabled="{{ waiting }}"`: use `{{ waiting | false }}` or seed `False`).
6. **Python operator precedence** in `Rx` logic: `(a > 0) & (b < 5)`, never `a > 0 & b < 5`.
7. **f-strings stringify.** `Progress(value=f"{x}")` is a string; pass `Progress(value=x)` with the `Rx` alone for
   number/boolean props.
8. **Key hygiene.** Avoid state keys that share a name with fields of looped items (`name`, `id`); use distinct keys
   (`who`, `query`, `new_todo`). This is precaution only: the empty rows in item 1 reproduced even with no collision
   (state keys `team` and `q`), so the bare `{{ field }}` form itself is the problem.
9. **Inputs with `on_change`:** add an explicit `SetState("k", "{{ $event }}")` (docs disagree on auto-sync).
10. **Stateful components auto-name** (`slider_22`). Reference them with `.rx` or give an explicit `name=`.
11. **`Rx` name used before the component exists:** `Rx(lambda: slider)` (forward reference), or `defer()`/`insert()`.
12. **Build-time vs render-time.** Python `if`/`for` run once. Use `If/Elif/Else` and `ForEach` for state-driven UI.
13. **Chained actions stop at the first failure**; clean up flags in BOTH `on_success` and `on_error`.
14. **`CallTool` / `Fetch` / host actions do not work in `prefab serve` preview** (and `CallTool` not in static export).
    Test those against a real server or an MCP host.
15. **`prefab serve` details (verified).** Silently picks the next free port when 5175 is taken: read the printed URL.
    Without `--reload` edits are ignored; with it you still refresh the browser manually.
16. **Charts animate on first render.** A screenshot taken immediately may show empty bars; wait ~1 s before judging.
17. **Pin the version.** `prefab-ui` is pre-1.0; minor bumps break the API. `fastmcp[apps]` pins only a minimum.
18. **Docs are partly stale/inconsistent.** Examples: `Sparkline` curve `linear|step` in the Python table vs
    `linear|smooth|step` in the protocol table; `EVENT` imported from `prefab_ui.components` on one page and from
    `prefab_ui.rx` on others (use `prefab_ui.rx`); Radio examples use `aria_labelledby`/`id` not in its API table.
    When something fails, introspect the installed package:
    ```python
    from prefab_ui.components import Button; print(Button.model_fields.keys())
    import prefab_ui.components as c; print(sorted(n for n in dir(c) if n[0].isupper()))
    ```
19. **Install in a venv, not globally.** `python3 -m venv .venv && .venv/bin/pip install prefab-ui`. A global pip install
    mixes dependencies with unrelated projects.

## Security notes for Python projects that expose a UI

- **State and the JSON payload are visible to the client.** Never put secrets, API keys, tokens or other users' data in
  `PrefabApp(state=...)`, in `view`, or in `structuredContent`. Send each user only what they may see.
- **`CallTool` / `Fetch` arguments come from the browser** and can be edited. Validate and authorise on the server for
  every call (the docs say IDs identify application data and "your backend remains responsible for authorizing access").
  `AppTool(bind=...)` hides a parameter from the agent but does not authorise it.
- **Tool visibility (`visibility=["app"]`) is host-enforced metadata**; `tools/list` still lists the tool. Treat every tool
  as callable by the model.
- **Rendering untrusted text:** `Markdown`, `Svg(content=...)` and `Embed(html=...)` render markup; do not feed them
  unescaped user content. `OpenLink` and `Embed(url=...)` should only point at trusted origins.
- **`Fetch` needs `connect_domains`** for cross-origin calls (CSP `connect-src`); add only the origins you need.
- **Generative UI:** code written by a model runs in the Pyodide/Deno sandbox, which is not a per-request isolation or a
  host security boundary. Do not run model-written Prefab code in the main server process (`exec`/`eval`).
- **Custom JS (`js_pipes`, `js_actions`)** is developer-authored code executed in the page; never build it from user input.
- **File upload:** `DropZone` / `OpenFilePicker` / `FileUpload` send file contents to your tool: enforce size and type
  limits (`max_size`, `accept` on `DropZone` are UX hints, not a security control) and validate server-side.
- **Exported HTML** (`prefab export`) embeds the data it was built with. Check the file before sharing it.
