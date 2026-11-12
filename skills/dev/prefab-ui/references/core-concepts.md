# Prefab: core concepts

Source: prefab.prefect.io docs (concepts/*, reactive/*), checked against prefab-ui 0.21.1.

Prefab is a protocol first: a JSON document describes a UI tree with state, expressions and actions. A bundled
JavaScript (React, shadcn/ui) renderer turns it into a live interface. The Python SDK is only a convenient way to
produce that JSON. Four concepts make everything:

| Concept | Role |
|---|---|
| Components | what the user sees |
| State | the data (client-side key-value store) |
| Expressions | `{{ ... }}` read state and compute display values |
| Actions | respond to events: change state, call the server |

Cycle: components show state via expressions -> user triggers an action -> action updates state -> expressions
re-evaluate -> display updates. All of that is in the browser. The server is involved only on `CallTool` / `Fetch`.

**Build time vs render time.** Your Python runs once and builds the tree. Python `for` / `if` produce a fixed result.
`ForEach` and `If/Elif/Else` live in the tree and react to state at render time. Use Python control flow for static
data, the control-flow components for dynamic state.

## Components and composition

- Every component is a class, called with keyword arguments. Containers are context managers:

```python
with Card():
    with CardContent():
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Active", variant="success")
```

- Code created inside a `with` block attaches to the innermost open container. Nesting in code = nesting on screen.
- Compound components expect specific children: `Card` -> `CardHeader`/`CardContent`/`CardFooter`; `Tabs` -> `Tab`;
  `Accordion` -> `AccordionItem`; `Select` -> `SelectOption`; `Combobox` -> `ComboboxOption`; `Table` ->
  `TableHeader`/`TableBody`/`TableRow`/`TableHead`/`TableCell`.
- `Row` = horizontal, `Column` = vertical, `Grid(columns=3)` = equal columns (`min_column_width` for responsive),
  `Dashboard` = explicit grid placement, `Pages` = page switcher. `gap=4` = `1rem` (Tailwind scale). A `Column`
  stretches to full width; `css_class="w-auto"` shrinks it.
- Every component accepts `css_class` (Tailwind string or list), `id`, `let`, `on_mount`, `aria_label`,
  `aria_labelledby`.
- Python loops are fine for build-time data:

```python
with Grid(columns=3, gap=4):
    for svc in services:          # runs once at build time
        with Card(): ...
```

- `defer()` / `insert()` rearrange structure: build a subtree outside the tree, graft it in later.

```python
from prefab_ui.components import defer, insert
with Column() as page:
    Text("Header")
    with defer():
        sidebar = Column()
        with sidebar:
            Text("Sidebar")
    insert(sidebar)
```

## State

- Flat, global, client-side key-value store. No local component state. Any component reads/writes any key.
- Seed with `PrefabApp(state={...})`. Components with a `value` prop also seed their own key
  (`Input(name="city", value="London")`).
- Interactive components with `name=` write their value to that key on every interaction (Input, Textarea, Slider,
  Checkbox, Switch, Select, RadioGroup, Combobox, DatePicker, Calendar, Tabs...). If `name` is omitted, it is
  auto-generated (`slider_22`) - use `.rx` to reference it.
- Dot paths address nested data: `profile.name`, `todos.0.done`. `Input(name="profile.name")` works. Missing or
  wrong-typed segment: read gives undefined, write is a no-op with a console warning.
- Reading: any string prop may contain `{{ key }}`. In Python use `Rx("key")` or `STATE.key`.
- Writing: controls (via `name`) and actions (`SetState`, `ToggleState`, `AppendState`, `PopState`, `CallTool`
  results via `RESULT`).

```python
from prefab_ui.rx import Rx
from prefab_ui.components import STATE
count = Rx("count")
Text(count)                 # {{ count }}
Text(f"Count: {count}")     # Count: {{ count }}
Text(count + 10)            # {{ count + 10 }}
Text(STATE.count)           # same as Rx, no variable needed
```

- Seed every key you reference. An undefined sole-value template renders as the literal template string; an undefined
  key inside mixed text becomes an empty string.
- Prefer distinct state key names (`who`, `query`, `new_todo`) over names that are also item fields (`name`, `id`).
- Inside `ForEach` use the item proxy (`with ForEach("team") as p: Text(p.name)`) or `{{ $item.name }}`; bare
  `{{ name }}` rendered empty in 0.21.1 (see `references/gotchas.md`).

## Expressions

`{{ }}` is the unit of reactivity. Any string prop may contain it; the renderer tracks dependencies and updates only
what changed. The language is deliberately bounded: arithmetic, comparisons, boolean logic, ternary, pipes.
Business logic stays in Python / server actions.

### Rx DSL (Python -> `{{ }}`)

| Python | Protocol |
|---|---|
| `Rx("count")` | `{{ count }}` |
| `count + 1`, `- * /`, `-score` | arithmetic |
| `count > 0`, `>= < <= == !=` | comparisons |
| `(a > 0) & (b < 5)` | `&&` (AND) |
| `a \| b` | `\|\|` (OR) |
| `~a` | `!a` (NOT) |
| `active.then("On", "Off")` | `active ? 'On' : 'Off'` |
| `Rx("user").address.city` | `user.address.city` |
| `todos.length()` | `todos \| length` |
| `name.default("Anonymous")` | `name \| 'Anonymous'` (null/undefined only) |

- **Precedence gotcha:** Python's `&` / `|` bind tighter than comparisons. ALWAYS parenthesise each comparison:
  `(score > 0) & (score < 100)`.
- F-strings work: each `Rx` inside becomes its own `{{ }}`: `Text(f"Hello, {first} {last}!")`.
- **Type preservation:** if the expression is the *entire* prop value, the renderer keeps its type (number/bool).
  `Progress(value=slider.rx)` -> number. Wrapping in an f-string turns it into a string. For number/boolean props
  (`value`, `min`, `max`, `disabled`, `checked`) pass the `Rx` alone.
- **Boolean prop gotcha:** `disabled="{{ waiting }}"` with undefined `waiting` is the truthy *string*; use
  `{{ waiting | false }}` or seed the key.
- `||` is a falsy default (`''`, `0`, `false`, undefined); `.default()` only null/undefined.

### `.rx` shorthand and forward references

`slider = Slider(value=50); Text(f"{slider.rx}%")` - reference a component's state without knowing its key.
Need `.rx` before the component exists? `vol = Rx(lambda: volume)` defers resolution until render:

```python
vol = Rx(lambda: volume)
with Column(gap=2):
    with Row(css_class="justify-between"):
        Label("Volume")
        Text((vol / 100).percent(), bold=True)
    volume = Slider(value=75)
```

### Pipes (formatting)

Method call on `Rx` = pipe. Chain left to right. Unknown pipe names pass the value through unchanged.

| Group | Pipes |
|---|---|
| Numbers | `currency()` / `currency("EUR")`, `percent()` / `percent(1)` (multiplies by 100), `number()` / `number(2)`, `compact()` (1.8M), `round(2)`, `abs()` |
| Dates | `date()` (medium) / `date("short")` / `date("long")`, `time()`, `datetime()` - input must be ISO string |
| Strings | `upper()`, `lower()`, `truncate(80)`, `pluralize("item")` |
| Arrays | `length()`, `join(", ")`, `first()`, `last()`, `selectattr("done")`, `rejectattr("done")` |

Examples: `(price * quantity).currency()`, `todos.rejectattr("done").length()`,
`Rx("items").length().pluralize("item")`.

Custom pipes: `PrefabApp(js_pipes={"stars": "(value) => '★'.repeat(Number(value))"})` then `{{ rating | stars }}`.
Pure, synchronous; built-in pipes always win. See "Custom handlers" in `references/running-and-integration.md`.

### Local scope: `let`

```python
with Column(gap=2, let={"greeting": "Don't Panic", "name": "Arthur"}):
    Text("{{ greeting }}, {{ name }}")
    with Column(let={"name": "Ford"}):      # shadows name, inherits greeting
        Text("{{ greeting }}, {{ name }}")
```

`let` bindings are read-only. Use `PrefabApp(state=...)` for mutable data.

### Special variables (use inside `{{ }}` strings, or import from `prefab_ui.rx`)

| Variable | Python | Where | Meaning |
|---|---|---|---|
| `$event` | `EVENT` | action handlers | value emitted by the interaction |
| `$result` | `RESULT` | `on_success` | return value of the action that just finished |
| `$error` | `ERROR` | `on_error` | error message |
| `$item` | `ITEM` | `ForEach` | whole current item |
| `$index` | `INDEX` | `ForEach` | zero-based index |
| `HOST` | `from prefab_ui.rx.mcp import HOST` | MCP host | display mode, theme, size (absent in standalone) |

`$event` values: Input/Textarea string, Slider number, Checkbox/Switch bool, Select/RadioGroup selected value,
Button `undefined`. Nested `ForEach` both define `$index`; capture the outer one first:
`ForEach("groups", let={"gi": "{{ $index }}"})` then `ForEach("groups.{{ gi }}.todos")`.

### Grammar (for hand-written protocol)

```
expr -> pipe ; pipe -> ternary ('|' (ident (':' arg)? | literal))*
ternary -> or ('?' expr ':' expr)? ; or -> and ('||' and)* ; and -> not ('&&' not)*
not -> '!' not | comp ; comp -> add (('=='|'!='|'>'|'<'|'>='|'<=') add)?
add -> mul (('+'|'-') mul)* ; mul -> unary (('*'|'/') unary)* ; primary -> '(' expr ')' | number | 'string' | true|false|null | ident
```

Pipe has the lowest precedence. Strings use single quotes inside expressions. `and`/`or`/`not` are accepted keywords.

## Actions

Event handlers (`on_click`, `on_change`, `on_submit`, `on_mount`, ...) take an action, a list of actions, or `None`.

| Kind | Actions |
|---|---|
| Client (browser only) | `SetState`, `ToggleState`, `AppendState`, `PopState`, `ShowToast`, `OpenLink`, `SetInterval`, `CallHandler`, `CloseOverlay` |
| Server | `CallTool` (MCP), `Fetch` (HTTP) |
| Host (MCP only) | `SendMessage`, `UpdateContext`, `RequestDisplayMode` |
| Other | `OpenFilePicker`, `FileUpload`, `InvokeAppTool` |

- Lists run in order and stop at the first failure (after that action's `on_error` ran).
- Every action has `on_success` / `on_error`; both accept one action or a list. `RESULT` / `ERROR` exist only inside
  their callback.
- A named input updates its state **before** `on_change` runs (State/Actions guides); `$event` is the emitted value.
  The API-server guide says a custom `on_change` *replaces* the auto-sync. The two pages disagree, so when you set
  `on_change` on an input also add an explicit `SetState("k", "{{ $event }}")` first (verified working: live search
  with `[SetState("q", "{{ $event }}"), Fetch.get(...)]`). An explicit `SetState` runs afterwards and can override.
- Errors in an `on_success` list end that callback list but the parent keeps its success outcome.
- Import paths in 0.21: `from prefab_ui.actions import SetState, ToggleState, AppendState, PopState, ShowToast,
  SetInterval, OpenLink, CallHandler, CloseOverlay, Fetch, CallTool` and `from prefab_ui.actions.mcp import CallTool,
  SendMessage, UpdateContext, RequestDisplayMode`. Both `CallTool` paths work in 0.21.1 (the first re-exports).
  `from prefab_ui.rx import RESULT, ERROR, EVENT, ITEM, INDEX, STATE, Rx`.

Patterns (verbatim from docs):

```python
# chain: append then clear
Button("Add", on_click=[AppendState("crew", Rx("new_member")), SetState("new_member", "")])

# loading state: set flag, call, clear in BOTH branches
saving = Rx("saving")
Button(saving.then("Saving...", "Save"), disabled=saving, on_click=[
    SetState("saving", True),
    CallTool("save", arguments={"data": Rx("form")},
        on_success=[SetState("saving", False), ShowToast("Saved!", variant="success")],
        on_error=[SetState("saving", False), ShowToast("{{ $error }}", variant="error")]),
])

# populate results
Button("Search", on_click=CallTool("search", arguments={"q": query.rx}, on_success=SetState("results", RESULT)))

# optimistic update with rollback
Checkbox(name="todos.{{ $index }}.done", on_change=[
    SetState("todos.{{ $index }}.done", "{{ $event }}"),
    CallTool("persist_todo", arguments={"id": "{{ $item.id }}", "done": "{{ $event }}"},
        on_error=[SetState("todos.{{ $index }}.done", "{{ !$event }}"), ShowToast("Failed to save", variant="error")]),
])

# dependent server calls
CallTool("get_user", arguments={"id": Rx("user_id")}, on_success=[
    SetState("user", RESULT),
    CallTool("get_permissions", arguments={"role": "{{ user.role }}"}, on_success=SetState("permissions", RESULT)),
])
```

Full action parameter tables and more examples: `references/actions-and-reactive.md`.
