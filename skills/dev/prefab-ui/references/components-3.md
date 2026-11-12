# Prefab UI digest, group 3

> **Read first.** Condensed from prefab.prefect.io (Apache-2.0, PrefectHQ/prefab) for prefab-ui 0.21.x. Code is copied from the docs and was NOT all re-run. Known drift in 0.21.1: bare `{{ field }}` inside `ForEach` renders empty, so use `with ForEach("rows") as r: Text(r.field)` or `{{ $item.field }}`; charts import from `prefab_ui.components.charts`. See `gotchas.md`.

## AreaChart
Purpose: filled-region chart for volume/trends; supports stacking.

Import: `from prefab_ui.components.charts import AreaChart, ChartSeries`

| Prop | Type | Default |
|---|---|---|
| data (required) | `list[dict] \| str` (list of dicts, or `{{ field }}` interpolation ref) | - |
| series (required) | `list[ChartSeries]` (each becomes a filled area) | - |
| x_axis | `str \| None` (data key for x-axis labels) | None |
| height | `int` (px) | 300 |
| stacked | `bool` | False |
| curve | `Literal["linear","smooth","step"]` | "linear" |
| show_dots | `bool` | False |
| show_legend | `bool` (legend below chart) | False |
| show_tooltip | `bool` | True |
| show_grid | `bool` (horizontal grid lines) | True |
| show_y_axis | `bool` (False = compact axis-free) | True |
| value_format | `str` (pipe string: `currency`, `currency:EUR`, `percent:1`, `compact:0`) | "auto" |
| css_class | `str \| None` (Tailwind) | None |

ChartSeries: `data_key: str` (required; must match a key in data dicts), `label: str | None` (legend/tooltip; defaults to data_key), `color: str | None` (CSS color override; default cycles theme palette `--chart-1`..`--chart-5`).

Example (basic):
```python
from prefab_ui.components.charts import AreaChart, ChartSeries

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
    {"month": "Apr", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "Jun", "desktop": 214, "mobile": 140},
]

AreaChart(
    data=data,
    series=[
        ChartSeries(data_key="desktop", label="Desktop"),
        ChartSeries(data_key="mobile", label="Mobile"),
    ],
    x_axis="month",
    show_legend=True,
)
```
Example (stacked + value format):
```python
from prefab_ui.components.charts import AreaChart, ChartSeries

data = [
    {"month": "Jan", "hosting": 34_000, "storage": 12_000},
    {"month": "Feb", "hosting": 41_000, "storage": 13_500},
    {"month": "Mar", "hosting": 46_000, "storage": 15_000},
    {"month": "Apr", "hosting": 52_000, "storage": 16_500},
]

AreaChart(
    data=data,
    series=[
        ChartSeries(data_key="hosting", label="Hosting"),
        ChartSeries(data_key="storage", label="Storage"),
    ],
    x_axis="month",
    stacked=True,
    value_format="currency",
    show_legend=True,
)
```
Variants (same data): `stacked=True` (topmost line = combined total); `show_grid=False` (minimal single-silhouette trend card); `curve="smooth"`; `curve="step"` (fill follows curve/steps).

Notes: shared model in "Charts" page. Protocol also has `animate` (default true, no Python prop documented in API table) and `onMount`/`id`. Raw data untouched by value_format; only display is formatted.

## BarChart
Purpose: vertical (or horizontal) bars for categorical data.

Import: `from prefab_ui.components.charts import BarChart, ChartSeries`

| Prop | Type | Default |
|---|---|---|
| data (required) | `list[dict] \| str` | - |
| series (required) | `list[ChartSeries]` (each becomes a group of bars) | - |
| x_axis | `str \| None` (category labels key) | None |
| x_axis_label | `RxStr \| None` (category-axis title; horizontal places it on left) | None |
| y_axis_label | `RxStr \| None` (value-axis title; hidden when show_y_axis=False) | None |
| height | `int` px | 300 |
| stacked | `bool` | False |
| horizontal | `bool` | False |
| bar_radius | `int` px | 4 |
| show_legend | `bool` | False |
| show_tooltip | `bool` | True |
| show_grid | `bool` | True |
| show_y_axis | `bool` | True |
| value_format | `str` | "auto" |
| css_class | `str \| None` | None |

ChartSeries: same as AreaChart (data_key required, label, color).

Example (basic):
```python
from prefab_ui.components.charts import BarChart, ChartSeries

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
    {"month": "Apr", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "Jun", "desktop": 214, "mobile": 140},
]

BarChart(
    data=data,
    series=[
        ChartSeries(data_key="desktop", label="Desktop"),
        ChartSeries(data_key="mobile", label="Mobile"),
    ],
    x_axis="month",
    show_legend=True,
)
```
Example (axis labels + horizontal):
```python
from prefab_ui.components.charts import BarChart, ChartSeries

BarChart(
    data=[{"month": "Jan", "users": 10}, {"month": "Feb", "users": 20}],
    series=[ChartSeries(data_key="users")],
    x_axis="month",
    x_axis_label="Month",
    y_axis_label="Users",
    horizontal=True,
)
```
Variants: `stacked=True`; `show_grid=False` (bars carry own baseline); `horizontal=True` (categories on y-axis, values extend right); `value_format="currency"` (e.g. data revenue 86_000..198_000).

Notes: colors auto-assigned from theme chart palette. With horizontal=True category title appears left, value title below. `show_y_axis=False` hides value-axis title too.

## Calendar
Purpose: month-view date picker; single, multiple, range modes. Selected dates stored in client state as ISO strings.

Import: `from prefab_ui.components import Calendar`

| Prop | Type | Default |
|---|---|---|
| mode | `str`: "single" \| "multiple" \| "range" | single |
| value | `date \| Rx \| dict \| list[date] \| None` (single: date; range: `{"from": date, "to": date}`; multiple: list of dates; any position accepts Rx) | None |
| name | `str \| None` (state key; single stores ISO string; range stores `{"from": "...", "to": "..."}`) | None |
| on_change | `Action \| list[Action] \| None` | None |
| css_class | `str \| None` | None |

Example (reading value reactively):
```python
import datetime
from prefab_ui.components import Calendar, Column, Input, Label, Row

with Row(gap=6):
    cal = Calendar(value=datetime.date(2026, 7, 4))
    with Column(gap=2, justify="center"):
        Label("Selected date")
        Input(value=cal.rx.date("long"), read_only=True)
```
Example (range):
```python
import datetime
from prefab_ui.components import Calendar

Calendar(
    mode="range",
    value={
        "from": datetime.date(2025, 6, 10),
        "to": datetime.date(2025, 6, 20),
    },
)
```
Also: `Calendar()` basic; `Calendar(value=datetime.date(2026, 7, 4))`; multiple mode `Calendar(mode="multiple", value=[datetime.date(2025, 6, 10), datetime.date(2025, 6, 15), datetime.date(2025, 6, 22)])`.

Notes: `.rx` holds ISO string (single), `{"from":..., "to":...}` object (range), array of ISO strings (multiple). `.date("long")` pipe formats a single ISO string ("2025-01-15" -> "January 15, 2025"). Auto-generated state name like `calendar_1` unless `name` set. Protocol shows values serialized as `2026-07-04T12:00:00.000Z`.

## Charts (shared chart model)
Purpose: shared data/series/formatting model behind every Prefab chart (bar, line, area, scatter, radar, etc.). Not a component itself.

Import: `from prefab_ui.components.charts import BarChart, ChartSeries` (chart classes live in `prefab_ui.components.charts`).

Model:
- `data`: list of dicts, one per row (category label + one value per series).
- `ChartSeries(data_key=..., label=..., color=...)`: one drawn series; `data_key` only required field; `color` accepts any CSS color or theme variable e.g. `var(--chart-1)`. Default colors follow theme palette in order; use `color` when a series carries meaning (danger red, brand, muted baseline).
- Axis: cartesian charts (bar, line, area, scatter) use `x_axis`; radar uses `axis_key`. Pie, radial, sparkline, waterfall take a single series and skip explicit axis; waterfall uses `data_key`/`name_key` (like PieChart, RadialChart).
- `data` can be live state: pass an `Rx` or `{{ key }}` string; chart re-renders when key changes (e.g. server action loads data).
- `value_format`: same pipe strings as expression pipes and data table columns (`currency`, `currency:EUR`, `percent:1`, `compact:0`, ...); raw data untouched; e.g. raw `42000000` + `value_format="compact"` renders `42M`.
- Display toggles: `show_legend` (off by default), `show_tooltip` (on), `show_grid` (on), `show_y_axis` (on; hide for sparkline-like contexts).
- Chart-specific props: `stacked`/`curve` (area), `horizontal` (bar), `inner_radius` (radial).

Example:
```python
from prefab_ui.components.charts import BarChart, ChartSeries

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
]

BarChart(
    data=data,
    series=[
        ChartSeries(data_key="desktop", label="Desktop"),
        ChartSeries(data_key="mobile", label="Mobile"),
    ],
    x_axis="month",
)
```
```python
from prefab_ui.components.charts import ChartSeries

ChartSeries(data_key="revenue", label="Revenue", color="var(--chart-1)")
```
```python
BarChart(data=data, series=series, x_axis="month", value_format="currency")
```

## Code
Purpose: code block with syntax highlighting.

Import: `from prefab_ui.components import Code`

| Prop | Type | Default |
|---|---|---|
| content (required) | `str` (can be positional) | - |
| language | `str \| None`: `python`, `javascript`/`js`, `typescript`/`ts`, `json`, `bash`/`sh`, `sql`, `html`, `xml`, `css`, `yaml`/`yml`, `markdown`/`md` | None |
| css_class | `str \| None` | None |

Example:
```python
from prefab_ui.components import Code

Code("""
def answer() -> int:
    \"\"\"Return the Answer to the Ultimate Question
    of Life, the Universe, and Everything.\"\"\"
    return 42
""".strip(), language="python")
```
Example (dynamic content):
```python
from prefab_ui.components import Code
from prefab_ui.rx import Rx

query_result = Rx("query_result")
Code(query_result, language="sql")
```
Notes: content supports expression interpolation (display server-generated output).

## If / Elif / Else (conditional)
Purpose: conditionally render components based on expressions; mirrors Python if/elif/else syntax.

Import: `from prefab_ui.components.control_flow import If, Elif, Else`

| Class | Params |
|---|---|
| If | `condition: str` (required; expression, renders children when truthy; positional OK) |
| Elif | `condition: str` (required; must follow an `If` or another `Elif`; positional OK) |
| Else | no args; renders children when no preceding If/Elif matched |

Example (If/Elif/Else):
```python
from prefab_ui.components import (
    STATE as state,
    Badge,
    Column,
    Select,
    SelectOption,
)
from prefab_ui.components.control_flow import Elif, Else, If


with Column(gap=3):
    with Select(name="status", placeholder="Choose a status..."):
        SelectOption("Active", value="active")
        SelectOption("Warning", value="warning")
        SelectOption("Error", value="error")
        SelectOption("Something else", value="other")
    with If(state.status == "error"):
        Badge("Error — system down", variant="destructive")
    with Elif(state.status == "warning"):
        Badge("Warning — degraded", variant="warning")
    with Elif(state.status == "active"):
        Badge("Active — all systems go", variant="success")
    with Else():
        Badge(f"Unknown status: {state.status}", variant="secondary")
```
Example (lone If with Rx):
```python
from prefab_ui.components import Alert, AlertTitle, Column, Row, Switch, Text
from prefab_ui.components.control_flow import If
from prefab_ui.rx import Rx

outOfStock = Rx("outOfStock")

with Column(gap=3):
    with Row(gap=2, align="center"):
        Switch(name="outOfStock")
        Text("Out of stock")
    with If(outOfStock):
        with Alert(variant="destructive"):
            AlertTitle("This item is unavailable")
```
Expression examples:
```python
from prefab_ui.rx import Rx

status = Rx("status")
count = Rx("count")
items = Rx("items")

with If(status == "active"):
    ...

with If((count > 0) & items.length()):
    ...
```
Chain rules example:
```python
with Column():
    # Chain 1: If / Elif / Else → one Condition node
    with If(status == "error"):
        Badge("Error", variant="destructive")
    with Elif(status == "warning"):
        Badge("Warning", variant="secondary")
    with Else():
        Badge("OK")

    Text("---")  # breaks the chain

    # Chain 2: standalone If → separate Condition node
    with If(showDetails):
        Text("Details here...")

    # Chain 3: another If starts a new chain (not an Elif!)
    with If(showFooter):
        Text("Footer content")
```
Gotchas:
- Conditions are reactive expressions; Rx Python operators work (`==`, `>`, `&`); comparisons, boolean logic, pipes all work.
- Chain rules: chain starts with `If`, extends through consecutive `Elif`/`Else` siblings; Elif/Else optional (lone If valid); `Else` must be last; any non-conditional sibling breaks the chain, including another `If` (starts a new independent chain).
- Renderer evaluates in order, renders first match; Else if none match; lone falsy If renders nothing.
- Wire format: siblings are grouped into a single `Condition` node (`cases` with `when`, plus `else`); `If`/`Elif` never appear in JSON directly (authoring constructs only).
- Page also uses `STATE as state` from `prefab_ui.components` as an alternative to `Rx(...)` (`state.status == "error"`, f-string `{state.status}` interpolates).

## DataTable
Purpose: high-level interactive table (wraps tanstack/react-table) with sorting, search, pagination, formatting. For static tables use `Table` instead.

Import: `from prefab_ui.components import DataTable, DataTableColumn` (also `ExpandableRow`, `EVENT` from `prefab_ui.components`; `Sparkline` from `prefab_ui.components.charts`).

DataTable:
| Prop | Type | Default |
|---|---|---|
| columns (required) | `list[DataTableColumn]` (auto-generated from DataFrame column names when rows is a DataFrame and columns omitted) | - |
| rows | `list[dict \| ExpandableRow] \| str \| DataFrame` (str = `{{ field }}` ref; pandas/polars) | [] |
| search | `bool` | False |
| search_placeholder | `str \| None` (renderer uses "Filter..." when omitted/None) | None |
| paginated | `bool` | False |
| page_size | `int` | 10 |
| on_row_click | `Action \| list[Action] \| None` (`$event` = row data dict; `$event.<field>`) | None |
| css_class | `str \| None` (table wrapper) | None |

DataTableColumn:
| Prop | Type | Default |
|---|---|---|
| key (required) | `str` (matches row dict keys) | - |
| header (required) | `str` | - |
| sortable | `bool` | False |
| format | `str \| None` (expression pipe, e.g. "currency", "percent:1", "date:long", "number:2"; ignored when cell value is a component) | None |
| width | `str \| None` CSS value ("200px", "30%") | None |
| min_width / max_width | `str \| None` | None |
| align | `str \| None`: "left" \| "center" \| "right" (applies to header + cells; resolves to header_class/cell_class Python-side) | None |
| header_class | `str \| None` Tailwind | None |
| cell_class | `str \| None` Tailwind | None |

ExpandableRow: `data: dict[str, Any]` (required), `detail: Component` (required; full-width area when expanded).

Example (basic):
```python
from prefab_ui.components import DataTable, DataTableColumn

DataTable(
    columns=[
        DataTableColumn(key="name", header="Name", sortable=True),
        DataTableColumn(key="email", header="Email"),
        DataTableColumn(key="role", header="Role", sortable=True),
    ],
    rows=[
        {"name": "Alice Johnson", "email": "alice@example.com", "role": "Admin"},
        {"name": "Bob Smith", "email": "bob@example.com", "role": "Editor"},
        {"name": "Carol White", "email": "carol@example.com", "role": "Viewer"},
    ],
)
```
Example (row click action with EVENT):
```python
from prefab_ui.components import DataTable, DataTableColumn, EVENT
from prefab_ui.actions.ui import ShowToast

DataTable(
    columns=[
        DataTableColumn(key="name", header="Name", sortable=True),
        DataTableColumn(key="email", header="Email"),
        DataTableColumn(key="role", header="Role"),
    ],
    rows=[
        {"name": "Arthur Dent", "email": "arthur@earth.com", "role": "Admin"},
        {"name": "Ford Prefect", "email": "ford@betelgeuse.com", "role": "Editor"},
        {"name": "Trillian", "email": "trillian@hog.com", "role": "Viewer"},
    ],
    on_row_click=ShowToast(f"{EVENT.name} ({EVENT.email})"),
)
```
Example (format):
```python
from prefab_ui.components import DataTable, DataTableColumn

DataTable(
    columns=[
        DataTableColumn(key="product", header="Product"),
        DataTableColumn(
            key="revenue", header="Revenue",
            sortable=True, format="currency",
        ),
        DataTableColumn(
            key="growth", header="Growth",
            sortable=True, format="percent:1",
        ),
        DataTableColumn(
            key="units", header="Units",
            sortable=True, format="number",
        ),
    ],
    rows=[
        {"product": "Widget Pro", "revenue": 128450, "growth": 0.142, "units": 3210},
        {"product": "Gadget Plus", "revenue": 84200, "growth": 0.087, "units": 1980},
        {"product": "Doohickey", "revenue": 52100, "growth": -0.031, "units": 870},
    ],
)
```
Example (pagination + search):
```python
from prefab_ui.components import DataTable, DataTableColumn

DataTable(
    columns=[
        DataTableColumn(key="id", header="ID"),
        DataTableColumn(key="task", header="Task", sortable=True),
        DataTableColumn(key="status", header="Status"),
    ],
    rows=[
        {"id": "T-001", "task": "Design system", "status": "Complete"},
        {"id": "T-002", "task": "API integration", "status": "In Progress"},
        {"id": "T-003", "task": "Testing", "status": "Pending"},
        {"id": "T-004", "task": "Documentation", "status": "In Progress"},
        {"id": "T-005", "task": "Deployment", "status": "Pending"},
    ],
    paginated=True,
    page_size=3,
)
```
```python
from prefab_ui.components import DataTable, DataTableColumn

DataTable(
    columns=[
        DataTableColumn(key="name", header="Name", sortable=True),
        DataTableColumn(key="species", header="Species"),
        DataTableColumn(key="status", header="Status"),
    ],
    rows=[
        {"name": "Arthur Dent", "species": "Human", "status": "Confused"},
        {"name": "Ford Prefect", "species": "Betelgeusian", "status": "Drinking"},
        {"name": "Zaphod", "species": "Betelgeusian", "status": "Presidential"},
        {"name": "Trillian", "species": "Human", "status": "Navigating"},
        {"name": "Marvin", "species": "Android", "status": "Depressed"},
    ],
    search=True,
    search_placeholder="Search the crew...",
)
```
Example (expandable rows):
```python
from prefab_ui.components import (
    DataTable,
    DataTableColumn,
    ExpandableRow,
    Badge,
    Text,
)

DataTable(
    columns=[
        DataTableColumn(key="time", header="Time", sortable=True),
        DataTableColumn(key="title", header="Title"),
        DataTableColumn(key="speaker", header="Speaker"),
    ],
    rows=[
        ExpandableRow(
            {"time": "9:00 AM", "title": "Opening Keynote", "speaker": "Jane Smith"},
            detail=Text("A sweeping overview of where the industry is headed and what to watch for in the coming year."),
        ),
        ExpandableRow(
            {"time": "10:30 AM", "title": "Building Dashboards", "speaker": "Bob Lee"},
            detail=Text("Hands-on workshop covering layout patterns, reactive data binding, and chart integration."),
        ),
        {"time": "12:00 PM", "title": "Lunch Break", "speaker": "—"},
        ExpandableRow(
            {"time": "1:00 PM", "title": "State Management Deep Dive", "speaker": "Carol White"},
            detail=Text("Explores client-side state, server sync, and how to keep your UI responsive under load."),
        ),
    ],
)
```
Example (component cells):
```python
from prefab_ui.components import DataTable, DataTableColumn, Badge
from prefab_ui.components.charts import Sparkline

DataTable(
    columns=[
        DataTableColumn(key="metric", header="Metric", sortable=True),
        DataTableColumn(key="trend", header="Trend"),
        DataTableColumn(key="status", header="Status"),
    ],
    rows=[
        {
            "metric": "Revenue",
            "trend": Sparkline(
                data=[45, 52, 49, 60, 55, 72, 68, 75],
                variant="success", fill=True, css_class="w-24",
            ),
            "status": Badge("Growing", variant="success"),
        },
        {
            "metric": "Churn",
            "trend": Sparkline(
                data=[12, 15, 18, 14, 20, 22, 19, 25],
                variant="destructive", css_class="w-24",
            ),
            "status": Badge("At risk", variant="destructive"),
        },
    ],
)
```
(page also has a third "Users" row with `variant="info", fill=True`, `Badge("Stable", variant="secondary")`.)
Example (widths/alignment/styling):
```python
from prefab_ui.components import DataTable, DataTableColumn

DataTable(
    columns=[
        DataTableColumn(key="id", header="ID", width="80px"),
        DataTableColumn(
            key="name", header="Name",
            min_width="150px", max_width="300px",
        ),
        DataTableColumn(
            key="amount", header="Amount",
            width="120px", align="right",
        ),
    ],
    rows=[
        {"id": "001", "name": "Arthur Dent", "amount": "$1,200.00"},
        {"id": "002", "name": "Ford Prefect", "amount": "$850.50"},
        {"id": "003", "name": "Trillian", "amount": "$2,100.00"},
    ],
)
```
```python
DataTableColumn(
    key="name", header="Name",
    header_class="text-emerald-600",
    cell_class="font-semibold text-emerald-600",
),
DataTableColumn(
    key="email", header="Email",
    cell_class="text-muted-foreground",
),
DataTableColumn(
    key="amount", header="Amount",
    align="right", cell_class="font-mono",
),
```
Example (DataFrame):
```python
import pandas as pd
from prefab_ui.components import DataTable, DataTableColumn

df = pd.DataFrame({
    "name": ["Arthur Dent", "Ford Prefect", "Trillian"],
    "score": [42, 87, 99],
    "region": ["Earth", "Betelgeuse", "Earth"],
})

# Auto-generate columns from df.columns
DataTable(rows=df)

# Custom columns — you control headers, sorting, formatting
DataTable(
    columns=[
        DataTableColumn(key="name", header="Hitchhiker", sortable=True),
        DataTableColumn(key="score", header="Score", align="right", format="number"),
    ],
    rows=df,
)
```
Gotchas:
- Sorting: click header cycles asc, desc, unsorted; multiple sortable columns independent, last-clicked determines order.
- Pagination: sorting/filtering work across full dataset; pagination only limits visible rows. Order: search first, then sort, then page boundaries.
- Without widths, columns auto-size to content.
- `align` compiles to header_class/cell_class; protocol only sees CSS classes.
- on_row_click: whole row highlights and fires action; row data as `$event` (`{{ $event.email }}`); `EVENT` from `prefab_ui.components` (page says `prefab_ui.rx`) gives cleaner syntax.
- ExpandableRow: multiple rows can be expanded simultaneously; expanded state follows row through sort/pagination; plain dict rows mix freely; detail is a single full-width canvas (any layout, nested tables, charts); works with sort, search, pagination, row click, component cells. Wire form: `_detail` key on row.
- `format` uses same pipes as `{{ value | pipe }}`; ignored when cell value is a component.
- DataFrame: when explicit columns given, `key` must match DataFrame column name. Works with any object having `.columns` and `.to_dict(orient="records")` (pandas) or `.to_dicts()` (polars).

## Dialog
Purpose: modal overlay; first child = trigger element, remaining children = dialog body; optional title/description in header.

Import: `from prefab_ui.components import Dialog` ; `from prefab_ui.actions import CloseOverlay, SetState, ShowToast` ; `from prefab_ui.actions.mcp import CallTool`

| Prop | Type | Default |
|---|---|---|
| title | `str \| None` | None |
| description | `str \| None` | None |
| name | `str \| None` (state key binding open state; `SetState(name, True)` opens; no initial state setup needed, defaults closed) | None |
| dismissible | `bool` (click outside / Escape / X button close it; False = only `CloseOverlay()` action) | True |
| css_class | `str \| None` | None |

Example (basic):
```python
from prefab_ui.components import (
    Button,
    Column,
    Dialog,
    Input,
    Label,
    Row,
)
from prefab_ui.actions import CloseOverlay

with Dialog(
    title="Crew Profile",
    description="Update your details for the Heart of Gold crew manifest.",
):
    Button("Edit Profile", variant="outline")
    with Column(gap=3):
        Label("Name")
        Input(placeholder="Arthur Dent")
        Label("Designation")
        Input(placeholder="Sandwich Maker")
    with Row(gap=2, css_class="justify-end"):
        Button("Save changes", on_click=CloseOverlay())
```
Example (state-controlled):
```python
from prefab_ui.components import Button, Column, Dialog, Row, Text
from prefab_ui.actions import SetState

with Column(gap=3):
    with Dialog(title="Help", name="show_help"):
        Button("Open via trigger", variant="outline")
        Text("This dialog can be opened by clicking the trigger or by any action that sets show_help to true.")
    Button(
        "Open via SetState",
        variant="secondary",
        on_click=SetState("show_help", True),
    )
```
Example (confirmation with feedback):
```python
from prefab_ui.components import Button, Dialog, Row, Text
from prefab_ui.actions import CloseOverlay, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import Rx

user_name = Rx("user_name")
user_id = Rx("user_id")

with Dialog(title="Remove User", description="This will revoke all access."):
    Button("Remove", variant="destructive")
    Text(f"User {user_name} will lose access to all projects.")
    with Row(gap=2, css_class="justify-end"):
        Button("Cancel", variant="outline", on_click=CloseOverlay())
        Button(
            "Remove User",
            variant="destructive",
            on_click=CallTool(
                "remove_user",
                arguments={"user_id": user_id},
                on_success=[
                    ShowToast("User removed", variant="success"),
                    CloseOverlay(),
                ],
                on_error=ShowToast("{{ $error }}", variant="error"),
            ),
        )
```
Example (non-dismissible):
```python
from prefab_ui.components import Button, Column, Dialog, Row, Text
from prefab_ui.actions import CloseOverlay

with Dialog(
    title="Terms of Service",
    description="You must accept to continue.",
    dismissible=False,
):
    Button("Review Terms")
    Text("By clicking Accept, you agree to the Galactic Terms of Service.")
    with Row(gap=2, css_class="justify-end"):
        Button("Accept", on_click=CloseOverlay())
```
Also: confirmation pattern with `on_click=[CallTool("delete_item", arguments={"id": item_id}), CloseOverlay()]` on a destructive button; Cancel button uses `on_click=CloseOverlay()`.

Gotchas:
- Clicking outside to dismiss may not work in doc previews (sandboxed); works in deployed apps.
- `CloseOverlay()` is the action to close from inside; use on Cancel and after confirm.
- With `name` set: `SetState(name, False)` closes it; trigger still works; closing via X/Escape/outside writes `False` back to state. Basis for keyboard shortcuts (bind key to `SetState(name, True)`).
- `dismissible=False` disables outside click, Escape, and X; need explicit `CloseOverlay()` button.
- In `on_success`/`on_error` of CallTool: `on_error` keeps dialog open for retry; `$error` available in error handler.

## DropZone
Purpose: drag-and-drop / click-to-browse file upload area. Files are read client-side, base64-encoded, passed via action system as `$event`; never sent to a server unless you wire an action (e.g. CallTool).

Import: `from prefab_ui.components import DropZone` ; `from prefab_ui.actions import FileUpload` (type for tool params)

| Prop | Type | Default |
|---|---|---|
| icon | `str \| None` (Lucide icon kebab-case, e.g. "cloud-upload", "image"; default upload icon) | None |
| label | `str \| None` (primary prompt) | None |
| description | `str \| None` (helper text under label) | None |
| accept | `str \| None` (MIME `"image/*"`, extensions `".csv"`, or comma-separated mix `".pdf,.docx,.txt"`) | None |
| multiple | `bool` (True: files accumulate across drops; False: each upload replaces) | False |
| max_size | `int \| None` (bytes per file; exceeding files rejected with toast) | None |
| disabled | `bool` | False |
| name | `str \| None` (state key; when set without on_change, file data stored under key) | None |
| on_change | `Action \| list[Action] \| None` (`$event` always `list[FileUpload]`) | None |
| css_class | `str \| None` | None |

Example (minimal):
```python
from prefab_ui.components import DropZone

DropZone()
```
Example (upload to tool):
```python
from prefab_ui.components import DropZone
from prefab_ui.actions.mcp import CallTool

DropZone(
    label="Upload CSV",
    accept=".csv",
    on_change=CallTool(
        "process_csv",
        arguments={"file": "{{ $event }}"},
    ),
)
```
Example (chained actions):
```python
from prefab_ui.components import DropZone
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool

DropZone(
    label="Upload data file",
    on_change=[
        SetState("uploading", True),
        CallTool("upload_file", arguments={"file": "{{ $event }}"}),
        SetState("uploading", False),
    ],
)
```
Example (reading value reactively with ForEach):
```python
from prefab_ui.components import (
    Badge, Column, DropZone, ForEach,
    If, Else, Muted, Row, Small, Text,
)

with Column(gap=3):
    zone = DropZone(
        label="Drop files to try it",
        multiple=True,
    )
    with If(f"{zone.rx.length()}"):
        with Column(gap=2):
            Text(
                f"{zone.rx.length()} file(s) selected",
                css_class="text-sm font-medium",
            )
            with ForEach(zone.rx):
                with Row(gap=2, align="center"):
                    Badge("{{ $item.type }}", variant="secondary")
                    Small("{{ $item.name }}")
                    Muted("{{ $item.size }} bytes")
    with Else():
        Muted("No files selected yet")
```
Example (typing the tool param):
```python
from prefab_ui.actions import FileUpload

@server.tool()
def process_csv(files: list[FileUpload]):
    import base64
    for f in files:
        contents = base64.b64decode(f.data)
        # f.name, f.size, f.type also available
        ...
```
Other examples: `DropZone(icon="image", label="Drop images here", description="PNG, JPG, or GIF up to 10MB")`; `DropZone(label="Upload documents", description="PDF, DOCX, or TXT", accept=".pdf,.docx,.txt")`; `DropZone(label="Upload files", description="Select as many as you like", multiple=True)`; `DropZone(label="Uploads disabled", disabled=True)`.

Gotchas:
- `$event` (and state value) is always `list[FileUpload]`, even for single file (one-element array); defaults `[]`. FileUpload fields: `name`, `size` (bytes), `type` (MIME), `data` (raw base64, NO `data:` URL prefix).
- Inside ForEach use `$item.name`, `$item.type`, `$item.size`; `.rx` references state; `.length()` pipe counts entries.
- For just an "Upload" button instead, use `OpenFilePicker` action (any clickable element becomes a file input).
- Auto state name like `dropzone_1` unless `name` set.

## ForEach
Purpose: render children once per item in a list from state; context manager gives handle to current item.

Import: `from prefab_ui.components.control_flow import ForEach`

| Prop | Type | Default |
|---|---|---|
| key (required) | `str` (data field/state key with the list; positional OK) | - |
| css_class | `str \| None` (wrapper element) | None |

Used as `with ForEach("crew") as member:` (item handle), `as (i, step)` (index, item; enumerate convention).

Example (objects):
```python
from prefab_ui.components import (
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    Badge,
    Column,
    Row,
)
from prefab_ui.components.control_flow import ForEach


with Column(gap=2):
    with ForEach("crew") as member:
        with Card():
            with CardHeader():
                with Row(gap=2, align="center"):
                    CardTitle(member.name)
                    Badge(member.designation, variant="secondary")
                CardDescription(member.email)
```
Example (primitives):
```python
from prefab_ui.components import Badge, Row
from prefab_ui.components.control_flow import ForEach


with Row(gap=2):
    with ForEach("tags") as tag:
        Badge(tag, variant="secondary")
```
Example (index destructuring):
```python
from prefab_ui.components import Column, Text, H4
from prefab_ui.components.control_flow import ForEach


with Column(gap=1, css_class="w-fit mx-auto"):
    H4("The Plan:")
    with ForEach("steps") as (i, step):
        Text(f"{i + 1}. {step}")
```
Example (nested loops):
```python
from prefab_ui.components import Checkbox, Column, Input
from prefab_ui.components.control_flow import ForEach

with ForEach("groups") as (gi, group):
    with Column():
        Input(name=f"groups.{gi}.name")
        with ForEach(f"groups.{gi}.todos") as (ti, todo):
            Checkbox(name=f"groups.{gi}.todos.{ti}.done")
```
Also: nested dot paths `CardDescription(f"Owner: {project.owner.name}")`.

Gotchas:
- Item variable is a reactive ref; attribute access becomes dot paths (`member.name` -> `{{ _loop_1.name }}`); can embed in f-strings. For simple values (strings/numbers) the variable is the value itself, no dot access.
- Index useful for display (`i + 1`) and building state paths for mutations, e.g. `SetState(f"items.{i}.done", True)`.
- Nested loops: each level captures `$item`/`$index` into uniquely scoped `let` bindings (`_loop_N`); outer vars remain valid in inner body; no manual scoping. Wire: `"let": {"_loop_3": "{{ $item }}", "_loop_3_idx": "{{ $index }}"}`.
- Raw template vars `$item`, `$index` usable in string templates (e.g. `"{{ $item.name }}"`).
- Can iterate `ForEach(zone.rx)` (an Rx) as well as a string key.
- Full nested-loop app: Todo List example page.


## Histogram
Purpose: bins raw numeric values and renders a bar chart of counts (distribution). Binning done in Python at construction time; wire payload is a standard `BarChart` (type "BarChart", series `[{"dataKey": "count"}]`, xAxis "bin").

Import: `from prefab_ui.components import Histogram`

| Prop | Type | Default |
|---|---|---|
| values (required) | `list[int \| float]` | - |
| bins | `int` (equal-width bins; ignored when bin_edges set) | 10 |
| bin_edges | `list[float] \| None` (explicit boundaries; overrides bins) | None |
| color | `str \| None` (CSS color; applies to all bars) | None |
| height | `int` px | 300 |
| bar_radius | `int` px | 4 |
| show_tooltip | `bool` | True |
| show_legend | `bool` | False |
| show_grid | `bool` | True |
| css_class | `str \| None` | None |

Example (basic):
```python
from prefab_ui.components import Histogram

response_times = [
    50, 65, 75, 80, 85, 90, 95, 98,
    100, 105, 108, 110, 112, 115, 118, 120, 122, 125,
    128, 130, 132, 135, 140, 145, 148, 150, 155, 160,
    165, 170, 175, 180, 185, 190, 195, 200, 210, 220,
    230, 250, 275, 300, 320, 350, 380, 400, 425, 450,
    475, 500,
]

Histogram(values=response_times)
```
Example (explicit edges):
```python
from prefab_ui.components import Histogram

Histogram(
    values=response_times,
    bin_edges=[50, 100, 150, 200, 300, 500],
)
```
Example (styled):
```python
Histogram(
    values=response_times,
    bins=6,
    color="#6d28d9",
    height=250,
)
```
Also: `Histogram(values=response_times, bins=5)`.

Gotchas: N edges produce N-1 bins; values outside the edge range are excluded; `bin_edges` allows unequal widths (e.g. SLA thresholds). Bin labels like "50–95" (en dash). No x_axis/series/value_format props.

## Image
Purpose: `<img>` element with `{{ field }}` interpolation on `src` and `alt`.

Import: `from prefab_ui.components import Image`

| Prop | Type | Default |
|---|---|---|
| src (required) | `str` (URL) | - |
| alt | `str` | "" |
| width | `str \| None` (CSS value with units, e.g. "200px", "100%"; inline style) | None |
| height | `str \| None` (CSS with units) | None |
| css_class | `str \| None` | None |

Example:
```python
from prefab_ui.components import Image

Image(src="https://picsum.photos/400/300", alt="Example image", width="400px")
```
Example (dynamic, in card):
```python
from prefab_ui.components import (
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Image,
    P,
)

with Card():
    with CardHeader():
        CardTitle("{{ name }}")
    with CardContent():
        Image(src="{{ photo_url }}", alt="{{ name }}", width="100%")
        P("{{ bio }}")
```
Gotchas: width/height are CSS strings with units (not ints).

## Label
Purpose: accessible text label for form inputs/controls; can contain text directly or wrap other components.

Import: `from prefab_ui.components import Label`

| Prop | Type | Default |
|---|---|---|
| text | `str \| None` (positional OK) | None |
| for_id | `str \| None` (ID of associated form field element) | None |
| optional | `bool` (muted "optional" indicator after text) | False |
| css_class | `str \| None` (appended to built-in styles) | None |

Example:
```python
from prefab_ui.components import (
    Column,
    Input,
    Label,
)

with Column(gap=2):
    Label("Username", for_id="username")
    Input(placeholder="Enter username", name="username")
```
Example (optional):
```python
from prefab_ui.components import Column, Input, Label

with Column(gap=2):
    Label("Phone", optional=True)
    Input(input_type="tel", name="phone", placeholder="+1 (555) 000-0000")
```
Gotchas: `Form.from_model()` sets `optional` automatically for non-required fields; set it yourself in manual forms. Protocol allows `children` (wrapping other components). Basic: `Label("Email address")`.

## Markdown
Purpose: renders full markdown (headings, bold, italic, lists, links, code blocks, tables, blockquotes).

Import: `from prefab_ui.components import Markdown`

| Prop | Type | Default |
|---|---|---|
| content (required) | `str` (positional OK) | - |
| css_class | `str \| None` | None |

Example:
```python
from prefab_ui.components import Markdown

Markdown("""
# Release Notes

Version **2.5.0** brings several improvements:

## New Features

- **Dark mode** with automatic system detection
- Keyboard shortcuts for *all* actions
- Inline `code` formatting support

## Migration Guide

> Update your config file before upgrading.

| Setting | Old | New |
|---------|-----|-----|
| theme | `light` | `auto` |
| timeout | `30s` | `60s` |
""")
```
Notes: page title says "template interpolation" but the page shows no interpolation example.

## Pages / Page
Purpose: multi-page layout where only the active page renders; navigation is via client state (no built-in tab bar; you build buttons/select/links yourself). Good for wizards/multi-step forms without server round-trip.

Import: `from prefab_ui.components import Page, Pages` ; `from prefab_ui.actions import SetState` ; `EVENT` from `prefab_ui.rx`

Pages:
| Prop | Type | Default |
|---|---|---|
| value | `str \| None` (initially active page value) | None |
| name | `str \| None` (state key for active page; other components write via SetState) | None |
| css_class | `str \| None` | None |

Page:
| Prop | Type | Default |
|---|---|---|
| title (required) | `str` (page identifier; positional OK) | - |
| value | `str \| None` (unique value; defaults to title) | None |

Example (name-bound state):
```python
from prefab_ui.components import (
    Button,
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Page,
    Pages,
    Row,
)
from prefab_ui.actions import SetState

with Column(gap=4):
    with Row(gap=2):
        Button("Earth", on_click=SetState("entry", "earth"))
        Button("Magrathea", variant="outline", on_click=SetState("entry", "magrathea"))
        Button("Milliways", variant="outline", on_click=SetState("entry", "milliways"))

    with Pages(name="entry", value="earth"):
        with Page("Earth", value="earth"):
            with Card():
                with CardHeader():
                    CardTitle("Earth")
                    CardDescription("Mostly harmless.")
        with Page("Magrathea", value="magrathea"):
            with Card():
                with CardHeader():
                    CardTitle("Magrathea")
                    CardDescription(
                        "Ancient planet-building civilization. "
                        "Custom-built luxury planets for the ultra-rich."
                    )
        with Page("Milliways", value="milliways"):
            with Card():
                with CardHeader():
                    CardTitle("Milliways")
                    CardDescription(
                        "The Restaurant at the End of the Universe. "
                        "Reservations recommended."
                    )
```
Example (wizard, `as pages` handle, `pages.rx`):
```python
from prefab_ui.components import Button, Column, Page, Pages, Row, Text
from prefab_ui.actions import SetState

with Column(gap=4):
    with Pages(value="setup") as pages:
        with Page("Setup", value="setup"):
            with Column(gap=4):
                Text("Configure your settings.")
                with Row():
                    Button("Next", on_click=SetState(pages, "review"))
        with Page("Review", value="review"):
            with Column(gap=4):
                Text("Review your choices.")
                with Row(gap=2):
                    Button("Back", variant="outline", on_click=SetState(pages, "setup"))
                    Button("Next", on_click=SetState(pages, "complete"))
        with Page("Complete", value="complete"):
            Text("All done!")
    Text(f"Current step: {pages.rx}", css_class="text-muted-foreground text-sm")
```
Example (Select driving Pages with EVENT):
```python
from prefab_ui.components import (
    Column, Heading, Page, Pages, Row, Select, SelectOption, Text,
)
from prefab_ui.actions import SetState
from prefab_ui.rx import EVENT

with Row(justify="around", css_class="w-full"):
    with Column(gap=4, css_class="w-auto"):
        with Pages(value="profile") as pages:
            with Page("Profile", value="profile"):
                Heading("Profile", level=4)
                Text("Update your display name and avatar.")
            with Page("Notifications", value="notifications"):
                Heading("Notifications", level=4)
                Text("Choose what triggers an alert.")
            with Page("Security", value="security"):
                Heading("Security", level=4)
                Text("Two-factor authentication and sessions.")

    with Column(gap=4, css_class="w-auto"):
        with Select(
            placeholder="Jump to...",
            on_change=SetState(pages, EVENT),
        ):
            SelectOption("Profile", value="profile")
            SelectOption("Notifications", value="notifications")
            SelectOption("Security", value="security")
        Text(
            f"Section: {pages.rx}",
            css_class="text-muted-foreground text-sm",
        )
```
Gotchas:
- `name` connects Pages to client state; changing key via `SetState` swaps the rendered page. If `name` omitted, an auto name like `pages_1` is generated.
- `SetState` accepts a stateful component directly (`SetState(pages, "review")`) and extracts its state key automatically; `EVENT` resolves to value from triggering component.
- `pages.rx` = reactive ref to active page's value string.
- Not a tab bar (see Tabs for that).


## Progress
Purpose: progress bar showing completion; fills left-to-right (or bottom-up if vertical) as `value` approaches `max`.

Import: `from prefab_ui.components import Progress`

| Prop | Type | Default |
|---|---|---|
| value | `float \| str` (str = template expression for dynamic binding) | 0 |
| min | `float` (renderer normalizes `(value - min) / (max - min)` to 0-100%) | 0 |
| max | `float` | 100 |
| variant | `str`: "default" \| "success" \| "warning" \| "destructive" \| "info" \| "muted" | default |
| size | `str`: "sm" (4px) \| "default" (6px) \| "lg" (10px) | default |
| target | `float \| str \| None` (vertical marker line at this value within min/max; template expr OK) | None |
| indicator_class | `str \| None` (Tailwind for fill bar; overrides variant coloring) | None |
| target_class | `str \| None` (Tailwind for target marker) | None |
| orientation | `str`: "horizontal" \| "vertical" | horizontal |
| gradient | `bool \| None` (None inherits theme default; True forces gradient; False solid) | None |
| css_class | `str \| None` (Tailwind for the track/outer container) | None |

Example (basic):
```python
from prefab_ui.components import Progress

Progress(value=60)
```
Example (range/variant):
```python
from prefab_ui.components import Column, Label, Progress

with Column(gap=4):
    with Column(gap=2):
        Label("3 of 5 steps")
        Progress(value=3, max=5)
    with Column(gap=2):
        Label("Temperature: 72°F (range 60–100)")
        Progress(value=72, min=60, max=100, variant="warning")
```
Example (reactive binding to Slider, forward-declared Rx):
```python
from prefab_ui.components import Column, Progress, Row, Slider, Text
from prefab_ui.rx import Rx

val = Rx(lambda: slider)

with Column(gap=3):
    with Row(css_class="justify-between items-center"):
        Text("Upload progress")
        Text(val.percent(), bold=True)
    Progress(value=val, max=1)
    slider = Slider(min=0, max=1, step=0.01, value=0.65)
```
Example (target marker + custom colors):
```python
from prefab_ui.components import Column, Label, Progress

with Column(gap=4):
    with Column(gap=2):
        Label("Below target")
        Progress(value=55, target=75)
    with Column(gap=2):
        Label("Custom target style")
        Progress(
            value=50, 
            target=75,
            indicator_class="bg-pink-400",
            target_class="bg-pink-400",
        )
```
Example (vertical):
```python
from prefab_ui.components import Progress, Row

with Row(css_class="gap-8 h-48 items-end justify-center"):
    Progress(value=75, orientation="vertical")
    Progress(value=50, target=80, variant="success", orientation="vertical")
    Progress(value=25, variant="info", orientation="vertical")
```
Also: `Progress(value=60, size="sm")`/`size="lg"`; `Progress(value=85, indicator_class="bg-red-500")`.

Gotchas:
- Set `max` to the gauge ceiling so `value` and `target` land at meaningful positions.
- Fractional values: use `max=1` (e.g. with a 0-1 slider) and `.percent()` pipe on Rx for the label.
- Forward-declare Rx with `Rx(lambda: slider)` to use before the Slider appears in the tree.
- `indicator_class` adds `pf-progress-flat` css class (protocol detail); overrides variant coloring.
- Vertical default height is theme-set; wrap in a sized container (e.g. `h-48`) for custom heights.
- `css_class` styles the track, not the fill.

## Radio / RadioGroup
Purpose: mutually exclusive single choice; each `Radio` is one option, wrapped in `RadioGroup` which tracks the selected value.

Import: `from prefab_ui.components import Radio, RadioGroup`

RadioGroup:
| Prop | Type | Default |
|---|---|---|
| name | `str \| None` (state key for selected value; auto-generated) | None |
| on_change | `Action \| list[Action] \| None` (`$event` = selected radio's `option` string) | None |
| css_class | `str \| None` | None |
| aria_labelledby | (used in page example; names the group by DOM ID of existing label; not in API table) | - |

Radio:
| Prop | Type | Default |
|---|---|---|
| option (required) | `str` (identifier stored in group's state when selected; page also says "Defaults to the label") | - |
| label | `str \| None` | None |
| value | `bool` (initially selected) | False |
| disabled | `bool` | False |
| required | `bool` (selection required for form submission) | False |
| css_class | `str \| None` | None |
| id | (used in page example `Radio(label="Basic", id="basic-plan")`; not in API table) | - |

Example (basic):
```python
from prefab_ui.components import Radio, RadioGroup

with RadioGroup(css_class="w-fit mx-auto"):
    Radio(option="sm", label="Small")
    Radio(option="md", label="Medium")
    Radio(option="lg", label="Large")
```
Example (reading value via .rx):
```python
from prefab_ui.components import Column, Radio, RadioGroup, Text

with Column(gap=4, css_class="w-fit mx-auto"):
    with RadioGroup() as group:
        Radio(option="heart-of-gold", label="Heart of Gold")
        Radio(option="bistromath", label="Bistromath")
        Radio(option="vogon-cruiser", label="Vogon Constructor Fleet")
    Text(f"Selected ship: {group.rx}")
```
Example (on_change action):
```python
from prefab_ui.components import Column, Radio, RadioGroup, Text
from prefab_ui.actions import SetState

with Column(gap=4, css_class="w-fit mx-auto"):
    with RadioGroup(
        on_change=SetState("choice", "You picked: {{ $event }}"),
    ):
        Radio(option="light", label="Light")
        Radio(option="dark", label="Dark")
        Radio(option="system", label="System", value=True)
    Text(
        "{{ choice | default:'Make a selection' }}",
        css_class="text-muted-foreground",
    )
```
Example (accessible labels):
```python
from prefab_ui import PrefabApp
from prefab_ui.components import Column, Label, Radio, RadioGroup

with PrefabApp() as app:
    with Column():
        Label("Plan", id="plan-label")
        with RadioGroup(name="plan", aria_labelledby="plan-label"):
            Radio(label="Basic", id="basic-plan")
            Radio(label="Pro", id="pro-plan")
```
Also: preselect `Radio(option="md", label="Medium", value=True)`; disabled `Radio(option="enterprise", label="Enterprise", disabled=True)`.

Gotchas:
- `.rx` on the RadioGroup holds the `option` string (e.g. "heart-of-gold"), NOT the label.
- Prefer `.rx` for "show current selection"; use `on_change` when transforming the value or side effects.
- Group name = state key; `id` identifies a DOM element (different things). `Label(for_id="plan")` alone cannot label a generic radiogroup container; use `aria_labelledby` with the label's DOM ID. Radio `label=` labels the individual option. Option IDs target native radio inputs; omitted IDs are generated uniquely and stable across rerenders.
- Each Radio also gets an auto state name (`radio_1`, ...; value bool) in protocol.

## ScatterChart
Purpose: points positioned by two numeric axes to show correlation; optional third dimension (bubble size).

Import: `from prefab_ui.components.charts import ScatterChart, ChartSeries`

| Prop | Type | Default |
|---|---|---|
| data (required) | `list[dict] \| str` (each dict = a point; for multiple series include `_series` field matching series data_key) | - |
| series (required) | `list[ChartSeries]` | - |
| x_axis (required) | `str` (key for x numeric values) | - |
| y_axis (required) | `str` (key for y numeric values) | - |
| z_axis | `str \| None` (bubble size key; radii scale proportionally) | None |
| height | `int` px | 300 |
| show_legend | `bool` | False |
| show_tooltip | `bool` | True |
| show_grid | `bool` | True |
| css_class | `str \| None` | None |

ChartSeries: `data_key` (required; identifier for color/legend; for multi-series must match `_series` values in data), `label`, `color` (CSS color; default cycles `--chart-1`..`--chart-5`).

Example (basic):
```python
from prefab_ui.components.charts import ScatterChart, ChartSeries

data = [
    {"hours": 2, "score": 45},
    {"hours": 4, "score": 62},
    {"hours": 5, "score": 58},
    {"hours": 6, "score": 71},
    {"hours": 8, "score": 78},
    {"hours": 10, "score": 85},
    {"hours": 12, "score": 82},
    {"hours": 14, "score": 91},
    {"hours": 16, "score": 88},
    {"hours": 18, "score": 95},
]

ScatterChart(
    data=data,
    series=[ChartSeries(data_key="students", label="Students")],
    x_axis="hours",
    y_axis="score",
)
```
Example (multiple series via `_series`):
```python
from prefab_ui.components.charts import ScatterChart, ChartSeries

data = [
    {"hours": 2, "score": 45, "_series": "morning"},
    {"hours": 5, "score": 58, "_series": "morning"},
    {"hours": 8, "score": 78, "_series": "morning"},
    {"hours": 10, "score": 85, "_series": "morning"},
    {"hours": 14, "score": 91, "_series": "morning"},
    {"hours": 18, "score": 95, "_series": "morning"},
    {"hours": 3, "score": 52, "_series": "evening"},
    {"hours": 6, "score": 60, "_series": "evening"},
    {"hours": 9, "score": 68, "_series": "evening"},
    {"hours": 11, "score": 72, "_series": "evening"},
    {"hours": 15, "score": 80, "_series": "evening"},
    {"hours": 17, "score": 84, "_series": "evening"},
]

ScatterChart(
    data=data,
    series=[
        ChartSeries(data_key="morning", label="Morning Class", color="#2563eb"),
        ChartSeries(data_key="evening", label="Evening Class", color="#e76e50"),
    ],
    x_axis="hours",
    y_axis="score",
    show_legend=True,
)
```
Example (bubble):
```python
from prefab_ui.components.charts import ScatterChart, ChartSeries

ScatterChart(
    data=[
        {"revenue": 120, "growth": 8, "employees": 50},
        {"revenue": 340, "growth": 12, "employees": 150},
        {"revenue": 210, "growth": 5, "employees": 80},
        {"revenue": 580, "growth": 18, "employees": 300},
        {"revenue": 90, "growth": 25, "employees": 20},
        {"revenue": 450, "growth": 10, "employees": 200},
        {"revenue": 160, "growth": 30, "employees": 35},
        {"revenue": 720, "growth": 7, "employees": 400},
    ],
    series=[ChartSeries(data_key="companies", label="Companies")],
    x_axis="revenue",
    y_axis="growth",
    z_axis="employees",
)
```
Gotchas: `x_axis` and `y_axis` are REQUIRED (unlike other cartesian charts), both numeric. Single-series: `data_key` is just an identifier (need not exist in data). Multi-series requires the `_series` field per point. No stacked/curve/value_format/show_y_axis props documented for scatter.

## Slider
Purpose: numeric range input (drag handle); default range 0-100.

Import: `from prefab_ui.components import Slider`

| Prop | Type | Default |
|---|---|---|
| value | `float \| None` (initial value) | None |
| name | `str \| None` (state key; bind to state for display/form submission) | None |
| min | `float` | 0 |
| max | `float` | 100 |
| step | `float \| None` (None = continuous) | None |
| disabled | `bool` | False |
| variant | `str`: "default" \| "success" \| "warning" \| "destructive" \| "info" \| "muted" (filled track) | default |
| size | `str`: "sm" (4px) \| "default" (6px) \| "lg" (10px) | default |
| indicator_class | `str \| None` (Tailwind for filled track; overrides variant coloring) | None |
| orientation | `str`: "horizontal" \| "vertical" (vertical fills container height) | horizontal |
| handle_style | `str`: "circle" \| "bar" (tall rounded rectangle) | circle |
| on_change | `Action \| list[Action] \| None` (`$event` = current numeric value) | None |
| css_class | `str \| None` | None |

(Protocol additionally lists `range`, `handleClass`, `gradient`; value may be `number | number[] | string`; not in Python API table.)

Example (display value via .rx):
```python
from prefab_ui.components import Column, Label, Slider, Text

with Column(gap=2):
    Label("Volume")
    volume = Slider(value=0.75, min=0, max=1)
    Text(volume.rx.percent(), bold=True)
```
Example (forward reference, display above slider):
```python
from prefab_ui.components import Column, Label, Progress, Row, Slider, Text
from prefab_ui.rx import Rx

val = Rx(lambda: s)

with Column(gap=4):
    with Row(css_class="justify-between"):
        Label("Brightness")
        Text(val.percent(), bold=True)
    Progress(value=val, min=0, max=1)
    s = Slider(value=0.42, min=0, max=1)
```
Example (range/step with name):
```python
from prefab_ui.components import Column, Label, Slider, Text

with Column(gap=2):
    Label("Rating")
    rating = Slider(value=4, name="rating", min=0, max=5, step=0.5)
    Text(rating.rx, bold=True)
```
Example (on_change action with EVENT):
```python
from prefab_ui.actions import SetState
from prefab_ui.components import Column, Slider, Text
from prefab_ui.rx import EVENT, Rx

level = Rx("level")

with Column(gap=4):
    Slider(
        value=50,
        on_change=SetState("level", EVENT),
    )
    Text(
        level.default("Drag the slider"),
        css_class="text-muted-foreground",
    )
```
Also: `Slider(value=50)`; `Slider(value=30, disabled=True)`; `Slider(value=100, variant="success")`; `Slider(value=60, size="sm")`; `Slider(value=85, indicator_class="bg-red-500")`; `Slider(value=50, handle_style="bar")`; vertical:
```python
from prefab_ui.components import Row, Slider

with Row(css_class="gap-8 h-48 items-center justify-center"):
    Slider(value=75, orientation="vertical")
    Slider(value=50, orientation="vertical", variant="success")
    Slider(value=25, orientation="vertical", variant="info")
```
Gotchas:
- Every form control has `.rx` (reactive ref to current value); for Slider it's a number; pipes like `.percent()` apply.
- Forward-declare with `Rx(lambda: slider_var)` when display appears above the slider in the layout (resolves at render time). See "Forward References" in concepts/components.
- Tip: for just displaying value, `.rx` is easier; use `on_change` for custom logic (tool call, updating multiple state keys).
- Vertical sliders fill container height: wrap in fixed-height parent (e.g. `h-48`).
- Auto state key like `slider_1` unless `name` set.

## Svg
Purpose: inline SVG markup, auto-sanitized with DOMPurify (strips `<script>`, event handlers like onload/onclick, etc.); safe for LLM-generated diagrams/charts/illustrations. Renders inline in DOM (unlike `Embed`), participates in layout, stylable with CSS classes.

Import: `from prefab_ui.components import Svg`

| Prop | Type | Default |
|---|---|---|
| content (required) | `str` (SVG markup; first positional) | - |
| width | `str \| None` (CSS value with units) | None |
| height | `str \| None` (CSS value with units) | None |
| css_class | `str \| None` | None |

Example:
```python
from prefab_ui.components import Svg

Svg(
    """\
<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="100" rx="10" fill="#4cc9f0"/>
  <text x="100" y="58" text-anchor="middle"
        font-size="20" fill="white">Hello SVG</text>
</svg>""",
    width="200px",
)
```
Sizing example:
```python
from prefab_ui.components import Svg

Svg(content=diagram_svg, width="400px", height="300px")
```
Gotchas: default size is intrinsic (from `viewBox`); safe features (paths, shapes, gradients, filters, text) pass through unchanged.

## Tabs / Tab
Purpose: tabbed interface; each `Tab` child defines trigger label and content for when active.

Import: `from prefab_ui.components import Tab, Tabs`

Tabs:
| Prop | Type | Default |
|---|---|---|
| variant | `str`: "default" (pill background) \| "line" (underline indicator) | default |
| orientation | `str`: "horizontal" (triggers above content) \| "vertical" (triggers beside content) | horizontal |
| value | `str \| None` (initially active tab; if omitted, first tab active) | None |
| name | `str \| None` (state key tracking the active tab; read/write from other components) | None |
| on_change | `Action \| list[Action] \| None` | None |
| css_class | `str \| None` | None |

Tab:
| Prop | Type | Default |
|---|---|---|
| title (required) | `str` (trigger label; positional OK) | - |
| value | `str \| None` (unique id; defaults to title) | None |
| disabled | `bool` | False |

Example (basic):
```python
from prefab_ui.components import (
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Input,
    Label,
    Tab,
    Tabs,
)

with Tabs(value="account"):
    with Tab("Account", value="account"):
        with Card():
            with CardHeader():
                CardTitle("Account")
                CardDescription("Make changes to your account here.")
            with CardContent():
                with Column(gap=3):
                    Label("Name")
                    Input(placeholder="Your name")
    with Tab("Password", value="password"):
        with Card():
            with CardHeader():
                CardTitle("Password")
                CardDescription("Change your password here.")
            with CardContent():
                with Column(gap=3):
                    Label("Current Password")
                    Input(input_type="password")
                    Label("New Password")
                    Input(input_type="password")
```
Example (state tracking):
```python
from prefab_ui.components import Button, Column, Row, Tab, Tabs, Text
from prefab_ui.actions import SetState

with Column(gap=4):
    with Tabs(name="activeTab", value="general"):
        with Tab("General", value="general"):
            Text("General settings here.")
        with Tab("Advanced", value="advanced"):
            Text("Advanced settings here.")

    with Row(gap=2):
        Button("Go to General", on_click=SetState("activeTab", "general"))
        Button("Go to Advanced", on_click=SetState("activeTab", "advanced"))
```
Example (change action):
```python
from prefab_ui.actions import SetState
from prefab_ui.components import Column, Tab, Tabs, Text

with Column(gap=3):
    with Tabs(name="active", value="overview",
              on_change=SetState("last_tab", "{{ active }}")):
        with Tab("Overview", value="overview"):
            Text("Overview content")
        with Tab("Details", value="details"):
            Text("Detailed content")
    Text("Last change: {{ last_tab | 'None yet' }}")
```
Variants/orientation: `Tabs(variant="line", value="one")`, `Tabs(orientation="vertical", value="one")`, `Tabs(variant="line", orientation="vertical", value="one")`.

Gotchas:
- Tabs writes the selected tab's value to its named state BEFORE running `on_change`; actions can read that key or use `$event` (selected tab's value). An explicit `SetState` in the handler can pick a different active tab.
- Auto state key (e.g. `tabs_1`) exists even without `name`.
- Each Tab needs `value` to identify it; Tabs `value` picks the initially open panel.

## Typography (H1-H4, Heading, P, Lead, Large, Small, Muted, Text, BlockQuote, Span, Link)
Purpose: text components for headings, body copy, inline formatting. All take content as positional arg and support `{{ field }}` interpolation; styles adapt to dark mode.

Import: `from prefab_ui.components import H1, H2, H3, H4, Heading, P, Lead, Large, Small, Muted, Text, BlockQuote, Span, Link, Markdown`

| Component | Purpose |
|---|---|
| `H1`..`H4` | Headings decreasing size/weight |
| `Heading(level=n)` | Dynamic heading level from a variable |
| `P` | Standard paragraph |
| `Lead` | Larger, muted intro text |
| `Large` | Emphasized, bolder text |
| `Small` | Smaller text for metadata/fine print |
| `Muted` | Secondary-color text |
| `Text` | Unstyled span, most flexible block |
| `BlockQuote` | Indented border for quotations |
| `Markdown` | Renders markdown syntax |

Common params (all text components):
| Prop | Type | Default |
|---|---|---|
| content (required) | `str` (positional; `{{ field }}` interpolation) | - |
| bold | `bool \| None` | None |
| italic | `bool \| None` | None |
| underline | `bool \| None` | None |
| strikethrough | `bool \| None` | None |
| uppercase | `bool \| None` | None |
| lowercase | `bool \| None` | None |
| align | `"left" \| "center" \| "right" \| "justify" \| None` | None |
| css_class | `str \| None` | None |

Extras:
- `Text`: accepts mixed positional args (strings, Span, Link) for inline formatting; strings auto-wrap as plain spans.
- `Heading`: `level: int` (default 1): 1-4.
- `Span`: `code: bool` (False; inline monospace code with background), `style: dict[str, str] | None` (inline CSS).
- `Link`: `href: str` (required), `target: str | None` (default '_blank'; `_blank` or `_self`), `code: bool` (False), `style: dict[str, str] | None`.

Example:
```python
from prefab_ui.components import H1, H2, H3, P, Lead, Large, Small, Muted, BlockQuote, Column

with Column(gap=3):
    H1("Page Title")
    H2("Section Heading")
    H3("Subsection")
    Lead("Introductory text that sets context for what follows.")
    P("Standard paragraph text for the main content of your UI.")
    Large("Key Takeaway: Components compose naturally.")
    Small("Terms and conditions apply")
    Muted("Last updated 5 minutes ago")
    BlockQuote("The best way to predict the future is to invent it.")
```
Example (inline formatting):
```python
from prefab_ui.components import Text, Span, Link, Column

with Column(gap=2):
    Text("Click ", Span("here", bold=True, underline=True), " to continue")
    Text("Price: ", Span("$9.99", strikethrough=True), " ", Span("$4.99", bold=True))
    Text("Run ", Span("pip install prefab-ui", code=True), " to get started")
    Text("Read the ", Link("documentation", href="https://prefab.prefect.io"), " for more")
```
Example (modifiers):
```python
from prefab_ui.components import Text, Column

with Column(gap=2):
    Text("Bold text", bold=True)
    Text("Italic text", italic=True)
    Text("Underlined", underline=True)
    Text("Strikethrough", strikethrough=True)
    Text("UPPERCASE", uppercase=True)
    Text("Centered", align="center")
```
Gotchas: formatting kwargs compile to Tailwind classes (font-bold, italic, underline, line-through, uppercase, text-center) in `cssClass`. Protocol for Text/Heading lists only bold/italic/align etc. Links open in new tab by default (`target="_blank"`).
