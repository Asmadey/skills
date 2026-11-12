# Running a Prefab UI and wiring a backend

Source: prefab.prefect.io docs (getting-started/*, serve, export, running/*, mcp/overview, concepts/generative-ui,
reference/app, concepts/custom-handlers), verified on prefab-ui 0.21.1 / fastmcp 4.1.8 where marked **(verified)**.

## Choose the delivery mode

| You have | Use | Server action | Renderer |
|---|---|---|---|
| A Python script/library, want to look at data locally | `prefab serve app.py` | none (`CallTool`/`Fetch` do not work in preview) | bundled |
| A static report to share, embed, or deploy to any static host | `prefab export app.py` | `Fetch` only (to a reachable API) | CDN (or `--bundled`) |
| A web app / internal tool with a REST backend (FastAPI, Flask, Django, Starlette...) | `PrefabApp.html()` in a page route | `Fetch` | bundled in the HTML |
| An MCP server (Claude Desktop, ChatGPT, Goose...) | `@mcp.tool(app=True)` in FastMCP | `CallTool` | provided by the MCP host |
| An LLM that should write the UI itself | generative UI + `Sandbox` | any of the above | any |

Prefab has no web-framework dependency. Same components/state/client actions everywhere; only transport differs.
Host-only actions (`SendMessage`, `UpdateContext`, `RequestDisplayMode`, app tools, `HOST`) exist only in MCP hosts.

## Install

```bash
uv add prefab-ui          # or: pip install prefab-ui     (Python 3.10+)
prefab version
# MCP: pip install "fastmcp[apps]"      # FastMCP 4.x pulls prefab-ui with a MINIMUM version only
# API: pip install fastapi uvicorn      # FastAPI is NOT bundled
```

**Pin the version** (pre-1.0; any minor bump 0.x -> 0.(x+1) may break the API; patches are safe):
`prefab-ui>=0.21,<0.22` or `prefab-ui==0.21.1`. Public API = `prefab_ui.components`, `prefab_ui.actions`, `PrefabApp`,
the `prefab` CLI and the JSON schema; everything else may change.

## Local preview: `prefab serve` (verified)

```bash
prefab serve app.py --reload            # http://127.0.0.1:5175 ; next free port if busy
prefab serve app.py:dashboard -p 8080   # pick a PrefabApp when the file has several
```

- The file must define a `PrefabApp` (module-level, e.g. `with PrefabApp(...) as app:` or `app = PrefabApp(...)`).
  If the port is busy it silently picks the next one (read the printed URL).
- `--reload` watches `.py` files in the directory; the browser needs a manual refresh after "Reloaded".
- Works in preview: state, `SetState`/`ToggleState`/`AppendState`/`PopState`, `ForEach`, conditionals, forms,
  charts. Does not work: `CallTool`, `SendMessage`, `UpdateContext`, `HOST`.

## Static export

```bash
prefab export app.py                 # writes app.html (CDN renderer, ~1 KB boilerplate, needs network)
prefab export app.py -o dashboard.html
prefab export app.py:dashboard --bundled          # inline all JS/CSS, ~6 MB, works offline
prefab export app.py --cdn-version 0.21.1         # pin CDN renderer (dev builds default to `latest`)
```

Embed with `<iframe src="dashboard.html" width="100%" height="400" frameborder="0"></iframe>`.
Client features work (state, forms, conditionals, `Fetch`); `CallTool` does not.
In code: `app.html()` returns the same self-contained page string.

## API server (FastAPI + Fetch) **(verified end to end)**

Three kinds of routes: **page** (HTML via `PrefabApp(...).html()`), **data** (plain JSON, written to state with
`SetState(..., RESULT)`), **component** (a tree returned as `component.to_json()`, rendered by a `Slot`).
Ready-to-run template: `templates/fastapi_app.py`. Key snippets:

```python
@app.get("/", response_class=HTMLResponse)
def page():
    with Column(gap=4) as view:
        Input(name="q", placeholder="Search...", on_change=[
            SetState("q", "{{ $event }}"),
            Fetch.get("/api/items", params={"q": "{{ $event }}"}, on_success=SetState("items", RESULT)),
        ])
        with ForEach("items") as it:
            Text(it.name)
    return HTMLResponse(PrefabApp(title="My App", view=view, state={"q": "", "items": []}).html())
```

- `Fetch.get/post/put/delete(url, params=..., body=..., on_success=..., on_error=...)`; the parsed JSON is `RESULT`.
  Non-2xx -> `on_error`; per the docs `ERROR` holds the status line (e.g. "400 Bad Request"). Not checked in 0.21.1.
- When an `Input` has `on_change`, include `SetState("k", "{{ $event }}")` (the docs say the auto-sync is replaced).
- Forms: wrap inputs in `Form(on_submit=Fetch.post(url, body={"name": Rx("name")}, ...))` so Enter submits; seed every
  referenced key in `PrefabApp(state=...)`.
- Dialog: first child is the trigger, the rest is the body. `CloseOverlay()` in the success chain closes it.
- Refresh after mutation: chain `Fetch.get(...)` inside `on_success`. Cleanup after a failed request must be in
  `on_error` (a failure stops the list).
- Delete: `Button("Delete", icon="trash-2", size="icon-xs", variant="ghost", on_click=Fetch.delete("/api/items/{{ id }}", ...))`.
- If the API lives on another origin than the page, add it to `PrefabApp(connect_domains=[...])` (CSP `connect-src`,
  documented "for Fetch actions"); the backend will then also need CORS (standard browser rule, not from the docs).
- Works with Flask/Django/Starlette: anything that can serve HTML and JSON.

## FastMCP: MCP Apps **(verified)**

```python
from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
mcp = FastMCP("My Server")

@mcp.tool(app=True)
def browse() -> PrefabApp:
    """Show all items."""
    with PrefabApp(state={"items": ITEMS}, css_class="p-6") as app:
        Heading("Items")
        with ForEach("items") as it:
            Text(it.name)
    return app
```

- `app=True` on the tool + return a `PrefabApp` **or a bare component** (shorthand, wrapped automatically). FastMCP
  registers a shared `ui://prefab/tool/<hash>/renderer.html` resource, sets the MCP Apps metadata, and serialises the
  return value into `structuredContent` (keys `$prefab`, `view`, `state`, `tools`, ...).
- Return `PrefabApp` when you need initial state, a title, theme or reusable defs; bare component for stateless views.
- **UI -> server:** `CallTool("tool_name", arguments={...}, on_success=..., on_error=...)`; result is `RESULT`
  (`RESULT.status` for a field). It can also take a registered function instead of a name (FastMCP resolves the
  address, incl. routing prefixes).
- **Slot pattern:** entry tool renders a shell with `Slot("detail")`; a helper tool returns a `PrefabApp`/component;
  `on_success=SetState("detail", RESULT)` fills the slot. A `Slot` shows its fallback children until it is filled.
- **Tool visibility:** helper tools called only by the UI should be `@mcp.tool(app=AppConfig(visibility=["app"]))`
  (`from fastmcp.apps import AppConfig`). It is metadata the host must enforce; `tools/list` still returns them.
  A helper that returns `PrefabApp` is auto-wired even without `app=True`.
- **Errors:** `raise ValueError("...")` in the tool -> MCP error -> `on_error=ShowToast(ERROR, variant="error")`.
- **Host actions:** `SendMessage("text")` (user message / new agent turn), `UpdateContext(structured_content={...})`
  (context for future turns; local state alone is NOT shared with the model), `RequestDisplayMode("fullscreen")`;
  `HOST.displayMode.default("inline")` (`from prefab_ui.rx.mcp import HOST`). Support varies by host; `HOST` is absent
  in `prefab serve`, so use `.default(...)`.
- **App-provided tools** (agent operates the open view): `AppTool(...)` in `PrefabApp(app_tools=[...])`, button calls
  `tool.invoke(amount=1)`. Needs host support (limited). With a Python function: `FastMCPApp("Name")`,
  `@app.tool()` for backend functions, `@app.ui()` for entry points, `FastMCP("X", providers=[app])`.
  `bind={"counter_id": STATE.counter_id}` hides a parameter from the agent and fills it from live state.
  Local operations: `AppTool("reset", actions=SetState("count", 0), result={"count": STATE.count})`.
  Template: `templates/mcp_app_with_backend.py` (verified: lists `increment`, `open_counter`; the UI payload carries
  `tools: [get_count, increment]`). For hidden-information games, return only the caller's permitted view.
- **Live data:** `PrefabApp(on_mount=SetInterval(duration=3000, on_tick=CallTool("get_stats", on_success=SetState("stats", RESULT))))`.
- **Pin `prefab-ui` yourself** in the MCP server's dependencies.
- **Test without a host:** FastMCP in-process client (`templates/test_client.py`): list tools, check `meta.ui.resourceUri`,
  call each tool and assert `structured_content` has `$prefab`/`view`. Then connect a real host:
  `claude mcp add prefab-demo -- /abs/.venv/bin/python /abs/mcp_server.py`.
  Interactions that need a host (SendMessage, UpdateContext, display modes, app tools) cannot be checked in `prefab serve`.
- Upload files bypassing the agent: `DropZone` / `FileUpload` / `OpenFilePicker` send the file straight to a tool
  instead of making the agent retype it (see `references/components-*.md` and `references/actions-and-reactive.md`).

## Generative UI (LLM writes Prefab code)

Flow: user prompt -> LLM generates Prefab Python -> sandbox executes -> `PrefabApp` renders. Sending Python is ~70%
smaller than sending the JSON protocol (token cost/latency), so servers stream Python and convert to JSON server-side.

```python
from prefab_ui.sandbox import Sandbox
from prefab_ui.app import PrefabApp

sandbox = Sandbox()           # needs Deno installed; first call ~2 s (Pyodide boot), later ~1 ms
code = '''
from prefab_ui.components import Heading, Slider, Text
from prefab_ui.app import PrefabApp
with PrefabApp(state={"confidence": 75}, css_class="p-6") as app:
    Heading("Revenue Dashboard")
    slider = Slider(value=75, min=0, max=100, name="confidence")
    Text(f"Confidence: {slider.rx}%")
'''
wire = await sandbox.run(code, data={"revenue": 1_200_000})   # data -> global variables in the sandbox
app = PrefabApp.from_json(wire)                                # from_json(wire, state={...}, theme=...) overrides
```

- `async with Sandbox() as sb:` for explicit lifecycle; a crashed Deno process restarts on the next call.
- `run()` has no timeout: `await asyncio.wait_for(sandbox.run(code), timeout=10)` (cancellation closes the worker; a lazy
  start is covered by the same deadline).
- **Security:** Pyodide in a Deno subprocess; fs read/write and network permissions are revoked before code is accepted;
  `deno.lock` pins dependencies (frozen). But each `run()` gets a fresh *namespace* while the interpreter and imported
  modules are shared, so it is NOT per-request Python isolation, and "WASM alone does not establish a host security
  boundary". Do not treat model-written code as trusted; installing extra packages during a call is unsupported.
- MCP pattern (`examples/generative-ui/server.py` in the repo): tool `execute_ui(code: str, data: dict | None = None)
  -> PrefabApp` with `app=True`, plus a searchable `components` reference tool that returns import paths and field
  signatures. The docstring of `execute_ui` should teach: context managers, `.rx`, `prefab_ui.components.charts` for charts.
- LLMs know the conventions: names follow shadcn/ui (`Card`, `CardHeader`, `Badge`, `Alert`), charts follow Recharts
  (`BarChart`, `ChartSeries`, `data_key`). Most common model mistake: importing charts from `prefab_ui.components`
  instead of `prefab_ui.components.charts`.

## PrefabApp reference

```python
PrefabApp(view=..., state={...}, theme=..., css_class="p-6", title="Prefab", mode="light"|"dark",
          app_tools=[...], defs=[Define...], stylesheets=[url], css=["..."], scripts=[url],
          connect_domains=[...], on_mount=Action|[Action], key_bindings={"Shift+?": action},
          js_pipes={...}, js_actions={...})
with PrefabApp(...) as app: ...        # implicit root Column, class pf-app-root
PrefabApp(view=view, state=...)        # pass a separately built tree
PrefabApp.from_json(wire, **overrides) # wrap pre-serialised wire data
app.html()   # complete self-contained page      app.to_json()   # wire envelope: $prefab, view, state, tools, defs, css, stylesheets, mode
app.csp()    # CSP domains computed from assets
```

- `on_mount` is a universal component prop: fires on load for the app; for components inside `Condition`, `Pages` or
  `ForEach` it fires when they enter the DOM (lazy data loading when a tab becomes active).
- `key_bindings`: keys are DOM `KeyboardEvent.key` values with optional `Ctrl+ Shift+ Alt+ Meta+` prefixes
  (`"Ctrl+Shift+S"`, `"ArrowRight"`, `"Shift+?"`). Suppressed while typing in input/textarea/select.
  `from prefab_ui.shortcuts import KeyboardShortcutsDialog`: `help_action = KeyboardShortcutsDialog({"ArrowRight": "Next"})`
  returns a `SetState` action usable in `key_bindings`; also place `KeyboardShortcutsDialog({...})` in the layout as a
  trigger button (state key defaults to `_show_shortcuts`).
- `stylesheets` render as `<link>` and feed `csp()`; `css` renders `<style>` and is included in the wire format.

## Custom handlers (the only place you write JavaScript)

Host-level config, never in the protocol (JSON references handlers by name only).

```python
js_pipes = {"initials": "(value) => String(value).split(' ').map(w => w[0]).join('').toUpperCase()"}
js_actions = {"constrain": """(ctx) => {            // ctx = {state, event, arguments}; return an object of state updates
    const keys = ['infra','people','tools']; const changed = ctx.arguments.key; const others = keys.filter(k => k !== changed);
    const remaining = 100 - ctx.event; const total = others.reduce((s,k) => s + ctx.state[k], 0); const u = {};
    for (const k of others) u[k] = total > 0 ? Math.round(ctx.state[k]/total*remaining) : Math.round(remaining/others.length);
    return u; }"""}
with PrefabApp(js_pipes=js_pipes, js_actions=js_actions) as app:
    Input(name="full_name", value="Arthur Dent")
    Text("{{ full_name | initials }}")
    Slider(name="infra", max=100, step=1, on_change=CallHandler("constrain", arguments={"key": "infra"}))
```

Pipes: pure and synchronous, `(value, arg?)`; built-ins win. Handlers: return nothing = no change; return value is
`RESULT` in `on_success`. Use only when expressions cannot express the logic (linked sliders, domain formatting).

## Playground

prefab.prefect.io/docs/playground lets you edit Prefab Python live with a theme picker. The playground renders the last
created component or `PrefabApp`, or the return value of `def main():` if you define it.
