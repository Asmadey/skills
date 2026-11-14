# Prefab digest g5: actions_* and reactive_* pages

> **Read first.** Condensed from prefab.prefect.io (Apache-2.0, PrefectHQ/prefab) for prefab-ui 0.21.x. Code is copied from the docs and was NOT all re-run. Known drift in 0.21.1: bare `{{ field }}` inside `ForEach` renders empty, so use `with ForEach("rows") as r: Text(r.field)` or `{{ $item.field }}`; charts import from `prefab_ui.components.charts`. See `gotchas.md`.

Source: local copies of https://prefab.prefect.io/docs pages. All Python examples below are copied verbatim from the docs (JSON "Protocol" duplicates omitted except short wire-format notes). Common facts across actions:
- Callback params `on_success` / `on_error` are typed `Action | list[Action] | None` (default None) wherever listed. `$result`/`RESULT` only in `on_success`; `$error`/`ERROR` only in `on_error`.
- `{{ key }}` interpolation is supported in string params (documented per action).
- Lists of actions run in order; a failing action short-circuits the rest of the chain (see Fetch).

---

## CallHandler
Purpose: invoke a client-side JavaScript function registered by the app developer. Runs instantly in the browser (no network), unlike CallTool. Good for state transformations, constraint enforcement, computed fields. Handlers are registered via `js_actions` on `PrefabApp` (see docs "Custom Handlers": /docs/concepts/custom-handlers.md).
Import: `from prefab_ui.actions import CallHandler`

Parameters:
- **handler** `str` *required* - Name of the registered handler function. Can be positional.
- **arguments** `dict[str, Any] | None` (default: None) - Extra arguments passed to the handler via `ctx.arguments`. Values support `{{ key }}` interpolation.
- **on_success** `Action | list[Action] | None` (default: None) - Run when the handler returns. Return value available as `$result`.
- **on_error** `Action | list[Action] | None` (default: None) - Run when the handler throws. Error message available as `$error`.

Wire format: `{"action": "callHandler", "handler": "string (required)", "arguments?": "object"}`

Examples:
```python
from prefab_ui.components import Slider
from prefab_ui.actions import CallHandler

Slider(name="infra", on_change=CallHandler("constrainBudget"))
```
Passing arguments:
```python
from prefab_ui.components import Button
from prefab_ui.actions import CallHandler

Button("Recalculate", on_click=CallHandler(
    "recalculate",
    arguments={"mode": "aggressive", "total": "{{ budget }}"},
))
```
Handler side (JS in js_actions):
```javascript
// In js_actions
"recalculate": (ctx) => {
    const mode = ctx.arguments.mode;  // "aggressive"
    const total = ctx.arguments.total;  // resolved budget value
    // ... compute and return state updates
}
```
Handling results:
```python
from prefab_ui.actions import CallHandler, ShowToast

Button("Validate", on_click=CallHandler(
    "validate",
    on_success=ShowToast("Valid!", variant="success"),
    on_error=ShowToast("Validation failed", variant="error"),
))
```
Chaining in a list:
```python
from prefab_ui.actions import CallHandler, SetState

Slider(name="infra", on_change=[
    SetState("dirty", True),
    CallHandler("constrainBudget"),
])
```
Gotchas: handler's return value is `$result` in `on_success`; a thrown exception triggers `on_error` with message in `$error`. Handler must be registered through `js_actions` on `PrefabApp`.

---

## CallTool
Purpose: bridge from UI to server logic; invokes a server (MCP) tool (the kind defined with `@mcp.tool()`) with specified arguments. The renderer proxies the call through the Prefab SDK; the tool runs server-side with full backend access. MCP-only action (lives in `prefab_ui.actions.mcp`). To let an agent perform the same operation on the open app, define an "app-provided tool" (docs: /docs/mcp/overview.md#app-provided-tools); it combines backend call, app-specific arguments, response actions and a result for the agent; a button can invoke the same definition with `.invoke()`.
Import: `from prefab_ui.actions.mcp import CallTool`

Parameters:
- **tool** `str | Callable` *required* - Name of the server tool, or a callable reference to the tool function. Can be positional.
- **arguments** `dict[str, Any]` (default: {}) - Arguments to pass. Values support `{{ key }}` interpolation to reference client state at call time.
- **on_success** `Action | list[Action] | None` (default: None) - Run on success; returned value as `$result`.
- **on_error** `Action | list[Action] | None` (default: None) - Run on failure; error message as `$error`.

Wire format: `{"action": "toolCall", "tool": "string (required)", "arguments?": "object"}` (plus `unwrapResult` flag, see below).

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions.mcp import CallTool

Button("Refresh Data", on_click=CallTool("get_latest_data"))
```
Passing client state (form controls with a `name` auto-sync to state; `Input(name="city")` updates `city` on every keystroke, no SetState needed; use `.rx` or `Rx("key")`):
```python
from prefab_ui.components import Input, Button, Column
from prefab_ui.actions.mcp import CallTool

with Column(gap=3):
    city = Input(name="city", placeholder="Enter a city...")
    Button(
        "Get Weather",
        on_click=CallTool(
            "get_weather",
            arguments={"location": city.rx},
        ),
    )
```
Combined with client actions (SetState runs first, instantly, then CallTool fires):
```python
from prefab_ui.components import Button
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import Rx

dataset = Rx("dataset")

Button("Analyze", on_click=[
    SetState("status", "analyzing..."),
    CallTool("run_analysis", arguments={"data": dataset}),
])
```
Result to state (RESULT = `$result`):
```python
from prefab_ui.components import Button
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import RESULT

Button(
    "Search",
    on_click=CallTool(
        "search",
        arguments={"q": "{{ query }}"},
        on_success=SetState("results", RESULT),
    ),
)
```
Callback chaining with success list and error toast:
```python
from prefab_ui.components import Button
from prefab_ui.actions import AppendState, SetState, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import ERROR, RESULT

Button(
    "Add Item",
    on_click=CallTool(
        "create_item",
        arguments={"name": "{{ item_name }}"},
        on_success=[
            AppendState("items", RESULT),
            ShowToast("Item created!", variant="success"),
        ],
        on_error=ShowToast(ERROR, variant="error"),
    ),
)
```
Callable references (FastMCP): when using Prefab with FastMCP (docs /docs/running/fastmcp.md) pass a function reference instead of a name string; resolved to the correct tool name at serialization time incl. namespace prefixes / global keys:
```python
from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import RESULT

app = FastMCPApp("My App")

@app.tool()
def search(q: str) -> list[dict]:
    return [{"name": "Arthur"}, {"name": "Ford"}]

@app.ui()
def browse():
    # Function reference — resolved automatically
    Button("Search", on_click=CallTool(
        search,
        arguments={"q": "{{ query }}"},
        on_success=SetState("results", RESULT),
    ))
```
Gotchas / details:
- Callable refs: (1) resolver handles name mangling so code needn't know the final tool name; (2) resolver can inspect tool metadata and inject hints into the serialized action, e.g. `unwrapResult`.
- String names also go through the resolver when one is active: `CallTool("save_contact")` can map to a global key like `"save_contact-a1b2c3d4"`. Useful in FastMCPApp context when no direct function reference exists (e.g. tools in mounted sub-apps).
- Automatic result unwrapping: MCP requires `structuredContent` to be a JSON object, so FastMCP wraps non-object returns (lists, strings, numbers) in `{"result": X}`. With a callable reference the resolver detects this and sets `unwrapResult: true`; the renderer extracts the inner value so `$result` equals what the tool returned. String names get the same benefit only if the resolver recognizes them; a dynamically constructed/unrecognized string name may not be unwrapped (envelope may leak into `$result`).
- `$result` and `$error` are mutually exclusive by callback.

---

## Fetch
Purpose: HTTP requests from the browser using native `fetch()`. Call REST endpoints, load external data, submit forms; no MCP server needed. Response parsed automatically: JSON -> object, everything else -> string; available as `$result`/`RESULT` in `on_success`.
Import: `from prefab_ui.actions import Fetch`

Classmethods: `Fetch.get(url, params=..., ...)` (GET accepts query `params`), `Fetch.post/put/patch(url, body=..., ...)`, `Fetch.delete(url, ...)`. Or construct `Fetch(...)` directly.

Parameters:
- **url** `str` *required* - supports `{{ key }}` interpolation; positional.
- **method** `str` (default: GET) - `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`.
- **headers** `dict[str, str]` - request headers; values support `{{ key }}` interpolation.
- **body** `dict | str` - request body. Dicts JSON-serialized automatically. Ignored for GET.
- **on_success** `Action | list[Action] | None` (default: None) - parsed response as `$result`.
- **on_error** `Action | list[Action] | None` (default: None) - error message as `$error`.

Wire format: `{"action": "fetch", "url": "string (required)", "method?": "GET | POST | PUT | PATCH | DELETE", "headers?": "object", "body?": "object | string"}`

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions import Fetch, SetState, ShowToast
from prefab_ui.rx import RESULT

Button(
    "Load Users",
    on_click=Fetch.get(
        "/api/users",
        on_success=[
            SetState("users", RESULT),
            ShowToast("Users loaded!", variant="success"),
        ],
    ),
)
```
```python
from prefab_ui.rx import Rx

query = Rx("query")
Fetch.get("/api/search", params={"q": query, "page": "1"})
```
```python
from prefab_ui.rx import Rx

name, email = Rx("name"), Rx("email")
Fetch.post("/api/users", body={"name": name, "email": email})
```
```python
from prefab_ui.rx import Rx

user_id = Rx("user_id")
Fetch.delete(f"/api/users/{user_id}")
```
Full form:
```python
from prefab_ui.actions import Fetch, SetState
from prefab_ui.rx import RESULT, Rx

form_data = Rx("form_data")

Fetch(
    "/api/submit",
    method="POST",
    headers={"X-Custom": "value"},
    body={"data": form_data},
    on_success=SetState("response", RESULT),
)
```
Error handling (non-2xx triggers `on_error` with the status line as `$error`; a 404 shows "404 Not Found"):
```python
from prefab_ui.actions import Fetch, ShowToast
from prefab_ui.rx import Rx

item = Rx("item")

Fetch.post(
    "/api/save",
    body={"item": item},
    on_success=ShowToast("Saved!", variant="success"),
    on_error=ShowToast("{{ $error }}", variant="error"),
)
```
Combined actions (loading flag):
```python
from prefab_ui.components import Button
from prefab_ui.actions import Fetch, SetState
from prefab_ui.rx import RESULT, Rx

query = Rx("query")

Button(
    "Submit",
    on_click=[
        SetState("loading", True),
        Fetch.post(
            "/api/submit",
            body={"q": query},
            on_success=SetState("result", RESULT),
        ),
        SetState("loading", False),
    ],
)
```
Gotchas: dict bodies get `Content-Type: application/json` automatically; string bodies sent as-is (form-encoded/raw text); auto Content-Type does not override an explicitly set header. If the request fails, `SetState("loading", False)` in the chain never runs (chain short-circuits) - use `on_error` on the Fetch to reset. Runs in the browser, so relative URLs/CORS are browser concerns (the page does not state host/sandbox restrictions; do not assume).

---

## OpenFilePicker
Purpose: an action (not a component) that opens the browser's native file picker when triggered from any clickable element (`on_click`); reads selected files to base64 and passes them to `on_success` as `$event`. Counterpart of DropZone component (dedicated upload area). Note: all file reading happens in the browser; files are never sent to a server unless you wire an `on_success` action (e.g. CallTool) to do so.
Import: `from prefab_ui.actions import OpenFilePicker`

Parameters:
- **accept** `str | None` (default: None) - MIME types (`"image/*"`), extensions (`".csv"`), or comma-separated mix.
- **multiple** `bool` (default: False) - allow multi-select. `$event` is always `list[FileUpload]` regardless; this only controls whether the OS picker allows multi-select.
- **max_size** `int | None` (default: None) - max file size in bytes. Oversized files are rejected with a toast notification (silently dropped from `on_success`; tool never sees them).
- **on_success** `Action | list[Action] | None` (default: None) - runs after files selected; `$event` is `list[FileUpload]`.
- **on_error** `Action | list[Action] | None` (default: None) - runs if file reading fails.

Wire format: `{"action": "openFilePicker", "accept?": "string", "multiple?": false, "maxSize?": "number"}`

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenFilePicker

Button("Upload File", on_click=OpenFilePicker())
```
Processing with a tool:
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenFilePicker
from prefab_ui.actions.mcp import CallTool

Button(
    "Upload CSV",
    icon="upload",
    variant="outline",
    on_click=OpenFilePicker(
        accept=".csv",
        on_success=CallTool(
            "process_csv",
            arguments={"file": "{{ $event }}"},
        ),
    ),
)
```
Multiple files:
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenFilePicker
from prefab_ui.actions.mcp import CallTool

Button(
    "Upload Images",
    on_click=OpenFilePicker(
        accept="image/*",
        multiple=True,
        on_success=CallTool(
            "process_images",
            arguments={"images": "{{ $event }}"},
        ),
    ),
)
```
Size limit:
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenFilePicker
from prefab_ui.actions.mcp import CallTool

Button(
    "Upload (max 5MB)",
    on_click=OpenFilePicker(
        max_size=5_000_000,
        on_success=CallTool("upload", arguments={"file": "{{ $event }}"}),
    ),
)
```
Error handling (on_error on the nested CallTool fires when server-side processing fails; message in `$error`):
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenFilePicker, ShowToast
from prefab_ui.actions.mcp import CallTool

Button(
    "Upload",
    on_click=OpenFilePicker(
        accept=".csv",
        on_success=CallTool(
            "process_csv",
            arguments={"file": "{{ $event }}"},
            on_success=ShowToast("File processed!", variant="success"),
            on_error=ShowToast(
                "Processing failed: {{ $error }}",
                variant="error",
            ),
        ),
    ),
)
```
Gotchas:
- `FileUpload` type: both OpenFilePicker and DropZone produce the same `$event` shape; Prefab ships a `FileUpload` type to annotate tool parameters (see DropZone docs, "The FileUpload Type": /docs/components/drop-zone.md#the-fileupload-type). Page does not detail its fields.
- User activation: OpenFilePicker must execute BEFORE any async server actions in the same chain (e.g. CallTool or SendMessage first expires the user-gesture window and the picker silently won't open). Put it first.

---

## OpenLink
Purpose: open a URL through the host application's link handler (navigation buttons, "View docs"). Pair with Button `variant="link"`.
Import: `from prefab_ui.actions import OpenLink`

Parameters:
- **url** `str` *required* - URL to open; positional; supports `{{ key }}` interpolation.

Wire format: `{"action": "openLink", "url": "string (required)"}`

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions import OpenLink

Button("View Documentation", variant="link",
       on_click=OpenLink("https://prefab-ui.dev"))
```
```python
from prefab_ui.components import Button, Row
from prefab_ui.actions import OpenLink

with Row(gap=4):
    Button("GitHub", variant="link",
           on_click=OpenLink("https://github.com/prefecthq/prefab"))
    Button("PyPI", variant="link",
           on_click=OpenLink("https://pypi.org/project/prefab-ui"))
```
Dynamic URL from state (renders `https://github.com/{{ repo }}`):
```python
from prefab_ui.components import Input, Button, Column
from prefab_ui.actions import OpenLink

with Column(gap=3):
    repo = Input(name="repo", placeholder="owner/repo")
    Button(
        "Open on GitHub",
        on_click=OpenLink(f"https://github.com/{repo.rx}"),
    )
```
Gotchas: opening goes via the host's link handler (host decides behavior). Security note (not in docs, derived from the interpolation feature): URLs built from user-typed state are user-controlled; page itself states no sanitization.

---

## RequestDisplayMode
Purpose: ask the MCP host to change app display (inline, fullscreen, picture-in-picture). The host decides whether to honor it; actual mode may differ from requested. MCP-only.
Import: `from prefab_ui.actions.mcp import RequestDisplayMode`

Parameters:
- **mode** `"inline" | "fullscreen" | "pip"` *required* - positional; host may not support every mode.
- **on_success** `Action | list[Action] | None` (default: None) - run when host responds successfully; read `HOST.displayMode` for current mode (may differ from requested).
- **on_error** `Action | list[Action] | None` (default: None) - run when request fails.

Wire format: `{"action": "requestDisplayMode", "mode": "inline | fullscreen | pip (required)"}`

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions.mcp import RequestDisplayMode

Button("Go Fullscreen", on_click=RequestDisplayMode("fullscreen"))
```
Toggle using HOST (`$host` injected into renderer state):
```python
from prefab_ui.components import Button, Column, If, Else
from prefab_ui.actions.mcp import RequestDisplayMode
from prefab_ui.rx.mcp import HOST

with Column():
    with If(HOST.displayMode == "fullscreen"):
        Button("Exit Fullscreen", variant="outline",
               on_click=RequestDisplayMode("inline"))
    with Else():
        Button("Go Fullscreen", variant="outline",
               on_click=RequestDisplayMode("fullscreen"))
```
Gotchas: HOST only populated under an MCP host (see HOST section) - in standalone `prefab serve` preview the toggle has no host to honor it.

---

## SendMessage
Purpose: let a UI control continue the conversation on the user's behalf (e.g. ask the agent to explain a chart, compare selections). The renderer sends the message with the user role; the MCP host controls how it appears in the conversation and whether it starts an agent response. MCP-only. To share a selection for a later turn without asking for a response, use UpdateContext.
Import: `from prefab_ui.actions.mcp import SendMessage`

Parameters:
- **content** `str` *required* - message text; positional; supports `{{ key }}` interpolation.
(No on_success/on_error documented.)

Wire format: `{"action": "sendMessage", "content": "string (required)"}`

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions.mcp import SendMessage

Button("Summarize", on_click=SendMessage("Please summarize the data above."))
```
Quick action buttons:
```python
from prefab_ui.components import Button, Row, H3, Column
from prefab_ui.actions.mcp import SendMessage

with Column(gap=3):
    H3("Quick Actions")
    with Row(gap=2):
        Button("Summarize", variant="outline",
               on_click=SendMessage("Summarize these results."))
        Button("Explain Further", variant="outline",
               on_click=SendMessage("Explain these results in more detail."))
        Button("Compare Options", variant="outline",
               on_click=SendMessage("Compare the top options and recommend one."))
```
Dynamic message:
```python
from prefab_ui.components import Input, Button, Column
from prefab_ui.actions.mcp import SendMessage

with Column(gap=3):
    question = Input(name="question", placeholder="Ask a follow-up question...")
    Button("Ask", on_click=SendMessage(question.rx))
```
Gotchas: ordering with OpenFilePicker (SendMessage before the picker kills user activation). Security note: message is injected as a user-role message, so state-derived text becomes user-authored text in the chat (derived from doc statement that it is sent with the user role).

---

## SetInterval
Purpose: run actions on a repeating timer. Each tick fires `on_tick`; timer stops automatically when `while_` becomes false, `count` reached, or both; `on_complete` then fires once. Also serves as a one-shot delay (`count=1`).
Import: `from prefab_ui.actions import SetInterval`

Parameters:
- **duration** `int` *required* - milliseconds between ticks; positional. (Protocol allows `number | string`.)
- **while_** `str | None` (default: None) - condition expression re-evaluated each tick against current state; when falsy, interval stops and `on_complete` fires. Serializes as `"while"` on the wire.
- **count** `int | None` (default: None) - max number of ticks; stops after this many.
- **on_tick** `Action | list[Action] | None` (default: None) - run each tick; `$event` is the tick number (1, 2, 3, ...).
- **on_complete** `Action | list[Action] | None` (default: None) - run when interval finishes.

Wire format: `{"action": "setInterval", "duration": "number | string (required)", "while?": "string", "count?": "number", "onTick?": "Action | Action[]", "onComplete?": "Action | Action[]"}`

Examples:
One-shot delay:
```python
from prefab_ui.components import Button
from prefab_ui.actions import SetInterval, SetState, ShowToast
from prefab_ui.rx import Rx

waiting = Rx("waiting")

Button(
    waiting.then("Waiting…", "Start 3 second timer"),
    disabled=waiting.default(False),
    on_click=[
        SetState(waiting, True),
        SetInterval(
            3000,
            count=1,
            on_complete=[
                ShowToast(
                    "Three seconds. An eternity for"
                    " a brain the size of a planet.",
                    variant="info",
                ),
                SetState(waiting, False),
            ],
        ),
    ],
)
```
Countdown:
```python
from prefab_ui.components import Button, Column, Text
from prefab_ui.actions import SetInterval, SetState
from prefab_ui.rx import Rx

seconds = Rx("seconds")

with Column(gap=4, css_class="items-center"):
    Text(
        (seconds > 0).then(
            "T-minus " + seconds + "…",
            "Ready for launch",
        ),
        css_class="text-2xl font-mono",
    )
    Button(
        (seconds > 0).then("Counting down", "Begin countdown"),
        disabled=seconds > 0,
        on_click=[
            SetState(seconds, 10),
            SetInterval(
                1000,
                while_=seconds > 0,
                on_tick=SetState(seconds, seconds - 1),
            ),
        ],
    )
```
Start/stop (flag in state referenced by `while_`; same pattern works for periodic server polling with `CallTool` in `on_tick`):
```python
from prefab_ui.components import Button, Row, Text
from prefab_ui.actions import SetInterval, SetState
from prefab_ui.rx import Rx

running = Rx("running")
ticks = Rx("ticks")

with Row(gap=4, css_class="items-center"):
    Button(
        "Start",
        disabled=running.default(False),
        on_click=[
            SetState(running, True),
            SetState(ticks, 0),
            SetInterval(
                1000,
                while_=running,
                on_tick=SetState(ticks, ticks + 1),
            ),
        ],
    )
    Text(
        ticks.default(0),
        css_class="text-2xl font-mono tabular-nums",
    )
    Button(
        "Stop",
        variant="outline",
        disabled=~running,
        on_click=SetState(running, False),
    )
```
Gotchas: if neither `while_` nor `count` is set, the interval runs indefinitely until the component tree is replaced. The `while_` flag is checked on the next tick (stop is not instant). Note the examples pass an `Rx` object to `SetState` as key (`SetState(waiting, True)`).

---

## ShowToast
Purpose: display a brief notification; client-side only (no server round-trip). Fire directly from a click or use as a `CallTool` callback.
Import: `from prefab_ui.actions import ShowToast`

Parameters:
- **message** `str` *required* - toast text; positional; supports `{{ key }}` interpolation.
- **description** `str | None` (default: None) - optional secondary text below the message.
- **variant** `"default" | "success" | "error" | "warning" | "info" | None` (default: None) - visual style. Omit for neutral default.
- **duration** `int | None` (default: None) - auto-dismiss in milliseconds; when omitted, the host decides.

Wire format: `{"action": "showToast", "message": "string (required)", "description?": "string", "variant?": "default | success | error | warning | info", "duration?": "number"}`

Examples:
```python
from prefab_ui.components import Button, Row
from prefab_ui.actions import ShowToast

with Row(gap=2):
    Button("Notify", on_click=ShowToast("Something happened"))
    Button("Warn me", variant="outline",
           on_click=ShowToast("Improbability levels rising", variant="warning"))
```
Variants:
```python
from prefab_ui.components import Button, Row
from prefab_ui.actions import ShowToast

with Row(gap=2, css_class="flex-wrap"):
    Button("Default", variant="outline",
           on_click=ShowToast("Something happened"))
    Button("Success", variant="success",
           on_click=ShowToast("Towel registered", variant="success"))
    Button("Error", variant="destructive",
           on_click=ShowToast("Towel not found", variant="error"))
    Button("Warning", variant="warning",
           on_click=ShowToast("Improbability drive unstable", variant="warning"))
    Button("Info", variant="info",
           on_click=ShowToast("42 towels in inventory", variant="info"))
```
Description:
```python
from prefab_ui.components import Button
from prefab_ui.actions import ShowToast

Button(
    "Deploy",
    on_click=ShowToast(
        "Deployment complete",
        description="3 agents online",
        variant="success",
    ),
)
```
Duration:
```python
ShowToast("Quick flash", duration=1500)
ShowToast("Read this carefully", duration=10000)
```
Success/error demo buttons:
```python
from prefab_ui.components import Button, Row
from prefab_ui.actions import ShowToast

with Row(gap=2):
    Button("Success callback", variant="success",
           on_click=ShowToast("Saved successfully!", variant="success"))
    Button("Error callback", variant="destructive",
           on_click=ShowToast("Could not save: connection timed out", variant="error"))
```
As CallTool callbacks (`{{ $error }}` captures the server error message):
```python
from prefab_ui.rx import Rx

item = Rx("item")

Button(
    "Save",
    on_click=CallTool(
        "save_item",
        arguments={"data": item},
        on_success=ShowToast("Saved successfully!", variant="success"),
        on_error=ShowToast("{{ $error }}", variant="error"),
    ),
)
```
Gotchas: Button variants `success`, `warning`, `info`, `destructive` appear in the examples (Button variant is separate from toast variant). Toast variant name is `"error"` (not "destructive").

---

## UpdateContext
Purpose: silently update the model's context from a UI interaction, to inform future turns. Does NOT ask the agent to respond (use SendMessage for that). You choose which fields; the MCP host decides how to include them in the model's context. MCP-only.
Import: `from prefab_ui.actions.mcp import UpdateContext`

Parameters:
- **content** `str | None` (default: None) - text added to model context; positional.
- **structured_content** `dict[str, Any] | None` (default: None) - structured data added to model context.

Wire format: `{"action": "updateContext", "content?": "string", "structuredContent?": "object"}`

When to use (from page): user selects a preference/mode that should influence later answers; form submission captures structured data the model should reference later; background state changes that provide context for the next turn.

Examples:
```python
from prefab_ui.components import Button
from prefab_ui.actions.mcp import UpdateContext

Button(
    "Use Advanced Mode",
    on_click=UpdateContext(
        content="User has selected advanced mode. Provide detailed technical responses."
    ),
)
```
Structured:
```python
from prefab_ui.components import Button, Select, SelectOption, Column
from prefab_ui.actions.mcp import UpdateContext

with Column(gap=3):
    with Select(name="thinking", placeholder="Thinking level...") as thinking:
        SelectOption(value="low", label="Low")
        SelectOption(value="medium", label="Medium")
        SelectOption(value="high", label="High")
    Button(
        "Set Preference",
        on_click=UpdateContext(
            structured_content={"preference": {"thinking": thinking.rx}},
        ),
    )
```

---

## SetState / ToggleState / AppendState / PopState (page "Update State")
Purpose: client-side state actions: set values, toggle booleans, manipulate lists; updates are instant, no server call. State is client-side data components read via `Rx()` references or template expressions.
Import: `from prefab_ui.actions import SetState, ToggleState, AppendState, PopState`

Setting up state: pass initial state to `PrefabApp` via the `state` parameter. Form controls (Input, Checkbox, Switch, Select, Slider, etc.) with `name=` automatically read/write that state key. Example:
```python
from prefab_ui.components import Slider, Muted, Column
from prefab_ui.rx import Rx

brightness = Rx("brightness")

with Column(gap=3):
    Slider(name="brightness", min=0, max=100)
    Muted(f"Brightness: {brightness}%")
```
For MCP tools, initial state via `AppResult.state`:
```python
from prefab_ui import AppResult

@mcp.tool()
async def settings() -> AppResult:
    return AppResult(
        view=...,
        state={"volume": 75, "muted": False},
    )
```

Parameters:
- **SetState**: `key` `str | Rx | StatefulComponent` *required* (state key, dot-path, Rx reference, or a stateful component like Slider/Input/Pages - its state key is extracted automatically); `value` `Any` (default: EVENT) - defaults to `EVENT`, the value from the triggering interaction (slider position, input text, checkbox state, etc.).
- **ToggleState**: `key` `str | Rx | StatefulComponent` *required*.
- **AppendState**: `key` `str | Rx | StatefulComponent` *required*; `value` `Any` (default: EVENT); `index` `int | str | None` (default: None) - insert position, None appends to end; supports negative indices and template strings like `"{{ $index }}"`.
- **PopState**: `key` `str | Rx | StatefulComponent` *required*; `index` `int | str` *required* - index to remove; supports negative indices and template strings like `"{{ $index }}"`.

Wire formats:
- `{"action": "setState", "key": "string (required)", "value": "any (required)"}`
- `{"action": "toggleState", "key": "string (required)"}`
- `{"action": "appendState", "key": "string (required)", "value": "any (required)", "index?": "number | string"}`
- `{"action": "popState", "key": "string (required)", "index": "number | string (required)"}`

Examples:
SetState (key and value both required in practice per prose):
```python
from prefab_ui.components import Badge, Button, Column, Row
from prefab_ui.actions import SetState
from prefab_ui.rx import Rx

drive = Rx("drive")

with Column(gap=3):
    with Row(gap=2):
        Button("Improbability", variant="outline",
               on_click=SetState("drive", "improbability"))
        Button("Conventional", variant="outline",
               on_click=SetState("drive", "conventional"))
        Button("Bistromath", variant="outline",
               on_click=SetState("drive", "bistromath"))
    Badge(f"Active drive: {drive}")
```
Dot-paths (`profile.name`; numeric segment = array index, e.g. `todos.0.done`; `name` prop works with dot-paths):
```python
from prefab_ui.components import (
    Card, CardDescription, CardHeader, CardTitle,
    Column, Input,
)
from prefab_ui.rx import Rx

profile = Rx("profile")

with Column(gap=3):
    with Card():
        with CardHeader():
            CardTitle(profile.name)
            CardDescription(profile.title)
    Input(name="profile.name", placeholder="Name")
    Input(name="profile.title", placeholder="Title")
```
Array paths in ForEach with `{{ $index }}` (`SetState("todos.0.done", True)` works for a hardcoded index; `{{ $index }}` targets the interacted row):
```python
from prefab_ui.components import Checkbox, Text
from prefab_ui.components.control_flow import ForEach

with ForEach("todos"):
    Checkbox(name="todos.{{ $index }}.done")
    Text("{{ $item.text }}")
```
ToggleState with If:
```python
from prefab_ui.components import Alert, AlertTitle, Button, Column
from prefab_ui.components.control_flow import If
from prefab_ui.actions import ToggleState
from prefab_ui.rx import Rx

showDetails = Rx("showDetails")

with Column(gap=2):
    Button("Toggle Details", variant="outline",
           on_click=ToggleState("showDetails"))
    with If(showDetails):
        with Alert():
            AlertTitle("Here are the details!")
```
AppendState + PopState + ForEach (dynamic list, chained Append then Set to clear the input):
```python
from prefab_ui.components import (
    Button, Column, ForEach, Input, Muted, Row, Text,
)
from prefab_ui.actions import AppendState, PopState, SetState
from prefab_ui.rx import Rx

new_member = Rx("new_member")
crew = Rx("crew")

with Column(gap=3):
    with ForEach("crew"):
        with Row(gap=2, align="center"):
            Text("{{ $item }}")
            Button(
                "×", variant="ghost", size="sm",
                on_click=PopState("crew", "{{ $index }}"),
            )
    with Row(gap=2):
        Input(name="new_member", placeholder="Crew member name...")
        Button("Add", on_click=[
            AppendState("crew", new_member),
            SetState("new_member", ""),
        ])
    Muted(f"{crew.length()} crew members")
```
Gotchas:
- WARNING: if an intermediate path segment is missing or wrong type (e.g. integer segment pointing at non-array), the update is a no-op with a console warning.
- `AppendState` with `index=0` prepends; negative indices count from the end; if key doesn't exist it creates a new array.
- Valid state keys: identifiers - letters, numbers, underscores, starting with a letter or underscore (`volume`, `_count`, `item_2`). No hyphens (conflict with expressions), no periods in a key name (dot is the path separator). Validated in Python when creating the action.
- For form controls with `name`, state auto-updates; explicit `SetState(..., EVENT)` only needed to write somewhere else.

---

## ERROR (reactive)
Purpose: reactive reference to `$error` - the error message string available inside `on_error` callbacks. Only meaningful inside `on_error`; outside it `$error` is undefined. Every action with callbacks (`on_success`/`on_error`) provides it when the action fails. `$result` is the success counterpart; neither exists outside its callback scope.
Import: `from prefab_ui.rx import ERROR`
Parameters: none (constant).
```python
from prefab_ui.components import Button
from prefab_ui.actions import ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import ERROR

Button(
    "Save",
    on_click=CallTool(
        "save_data",
        on_error=ShowToast(
            f"Failed: {ERROR}",
            variant="error",
        ),
    ),
)
```
Write to state for UI display:
```python
from prefab_ui.actions import SetState

CallTool(
    "fetch_data",
    on_error=SetState("error_message", ERROR),
)
```

## EVENT (reactive)
Purpose: reactive reference to `$event` - value produced by the interaction that triggered the action handler.
Import: `from prefab_ui.rx import EVENT`
`$event` by component: Input/Textarea = current text (string); Slider = current position (number); Checkbox/Switch = checked state (boolean); Select = selected value (string); RadioGroup = selected value (string); Button = `undefined`.
(Other pages: OpenFilePicker `$event` = `list[FileUpload]`; SetInterval `on_tick` `$event` = tick number 1,2,3...)
Usage (capture value under a different key or pass to a server action; the control's own `name` key updates automatically):
```python
from prefab_ui.components import Slider
from prefab_ui.actions import SetState
from prefab_ui.rx import EVENT

Slider(
    name="volume",
    on_change=SetState("last_adjusted", EVENT),
)
```
In raw templates use `$event` directly:
```python
from prefab_ui.components import Input
from prefab_ui.actions import ShowToast

Input(
    name="search",
    on_change=ShowToast("Searching for: {{ $event }}"),
)
```

## HOST (reactive)
Purpose: reactive reference to `$host` - MCP host context injected by the MCP Apps runtime: display mode, available display modes, theme, container dimensions.
Import: `from prefab_ui.rx.mcp import HOST` (note: NOT `prefab_ui.rx`; it is MCP-runtime specific).
```python
from prefab_ui.rx.mcp import HOST

HOST.displayMode             # → {{ $host.displayMode }}
HOST.theme                   # → {{ $host.theme }}
HOST.availableDisplayModes   # → {{ $host.availableDisplayModes }}
HOST.containerDimensions     # → {{ $host.containerDimensions }}
```
Fields (all dependent on what the MCP host provides): `displayMode` string `"inline"|"fullscreen"|"pip"`; `availableDisplayModes` `string[]`; `theme` string `"light"|"dark"`; `containerDimensions` object with `width` and `height`.
Display-mode toggle:
```python
from prefab_ui.components import Button, Column, If, Else
from prefab_ui.actions.mcp import RequestDisplayMode
from prefab_ui.rx.mcp import HOST

with Column():
    with If(HOST.displayMode == "fullscreen"):
        Button("Exit Fullscreen", variant="outline",
               on_click=RequestDisplayMode("inline"))
    with Else():
        Button("Go Fullscreen", variant="outline",
               on_click=RequestDisplayMode("fullscreen"))
```
MCP only / standalone limits: `HOST` is only populated when the renderer is connected to an MCP host. In standalone mode (via `prefab serve`), `$host` is undefined. Handle with the `default` pipe:
```python
from prefab_ui.rx.mcp import HOST

HOST.displayMode.default("inline")  # → {{ $host.displayMode | default:inline }}
```

## INDEX (reactive)
Purpose: reactive reference to `$index` - zero-based position of the current item in a ForEach loop; key for targeting specific items in state arrays.
Import: `from prefab_ui.rx import INDEX`
```python
from prefab_ui.components import Text, ForEach
from prefab_ui.rx import INDEX

with ForEach("items"):
    Text(f"{INDEX + 1}. {{{{ name }}}}")
```
Targeting array items:
```python
from prefab_ui.components import Checkbox, ForEach
from prefab_ui.rx import INDEX

with ForEach("todos"):
    Checkbox(name=f"todos.{INDEX}.done")
```
Nested loops: inner loop shadows `$index`; capture the outer index with `let` first:
```python
from prefab_ui.components import Text, ForEach

with ForEach("groups", let={"gi": "{{ $index }}"}):
    with ForEach("groups.{{ gi }}.todos"):
        Text("Group {{ gi }}, item {{ $index }}")
```
Arithmetic (like any Rx):
```python
from prefab_ui.rx import INDEX

INDEX + 1          # → {{ $index + 1 }}
INDEX == 0         # → {{ $index == 0 }}
```

## ITEM (reactive)
Purpose: reactive reference to `$item` - current element in a ForEach iteration (entire item object). Usually not needed: inside ForEach, fields are directly available (`{{ name }}` equals `{{ $item.name }}`). Useful when passing the whole object to an action, or to disambiguate nested structures where a field name collides with a `let` binding or outer state key.
Import: `from prefab_ui.rx import ITEM`
```python
from prefab_ui.components import Text, ForEach
from prefab_ui.rx import ITEM

with ForEach("crew"):
    Text(f"Name: {ITEM.name}")
```
Passing whole object:
```python
from prefab_ui.components import Button, ForEach
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import ITEM

with ForEach("users"):
    Button(
        "Edit",
        on_click=CallTool(
            "edit_user",
            arguments={"user": str(ITEM)},
        ),
    )
```
Dot paths:
```python
from prefab_ui.rx import ITEM

ITEM.name          # → {{ $item.name }}
ITEM.address.city  # → {{ $item.address.city }}
```

## RESULT (reactive)
Purpose: reactive reference to `$result` - action return value available inside `on_success` callbacks. Only meaningful inside `on_success` (undefined outside); counterpart of `$error`. For `CallTool`: tool's return value (parsed as JSON when possible); with `unwrapResult: true` (set automatically by callable references) the renderer extracts the value from a `{"result": X}` envelope first. For `Fetch`: the parsed response body.
Import: `from prefab_ui.rx import RESULT`
```python
from prefab_ui.components import Button
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import RESULT

Button(
    "Search",
    on_click=CallTool(
        "search",
        arguments={"q": "{{ query }}"},
        on_success=SetState("results", RESULT),
    ),
)
```
```python
from prefab_ui.actions import AppendState, SetState, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import RESULT

CallTool(
    "create_item",
    arguments={"name": "{{ item_name }}"},
    on_success=[
        AppendState("items", RESULT),
        ShowToast("Created!", variant="success"),
    ],
)
```

## STATE (reactive)
Purpose: proxy giving reactive references to state keys via attribute access; `STATE.count` equals `Rx("count")`. Useful for keys created dynamically by form controls/actions without a separate `Rx` declaration.
Import: `from prefab_ui.rx import STATE`
```python
from prefab_ui.rx import STATE

STATE.count       # → {{ count }}
STATE.user.name   # → {{ user.name }}
```
```python
from prefab_ui.rx import STATE
from prefab_ui.components import Input, Text

Input(name="query", placeholder="Search...")
Text(f"You typed: {STATE.query}")
```
Dot paths (each `.` adds a segment):
```python
from prefab_ui.rx import STATE

STATE.user.address.city    # → {{ user.address.city }}
STATE.todos.length()       # → {{ todos | length }}
```

---
Cross-cutting notes
- Import locations: client-side actions from `prefab_ui.actions` (CallHandler, Fetch, OpenFilePicker, OpenLink, SetInterval, ShowToast, SetState, ToggleState, AppendState, PopState); MCP-only actions from `prefab_ui.actions.mcp` (CallTool, RequestDisplayMode, SendMessage, UpdateContext); reactive vars from `prefab_ui.rx` (ERROR, EVENT, INDEX, ITEM, RESULT, STATE, Rx) except `HOST` from `prefab_ui.rx.mcp`.
- Reactive-variable template names: `$error`, `$event`, `$host`, `$index`, `$item`, `$result`.
- Standalone preview (`prefab serve`): only documented limit is `$host` undefined; MCP-only actions (CallTool/SendMessage/UpdateContext/RequestDisplayMode) need an MCP host - pages say "MCP-only"/"MCP host" but do not describe standalone behavior for these beyond HOST.
- Security: pages contain no dedicated security section. Documented data-flow facts: OpenFilePicker reads files in-browser and sends nothing unless wired to CallTool; SendMessage posts a user-role message; UpdateContext injects data into model context at the host's discretion.
