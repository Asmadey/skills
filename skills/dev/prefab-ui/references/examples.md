# Prefab examples digest (group g4)

> **Read first.** Condensed from prefab.prefect.io (Apache-2.0, PrefectHQ/prefab) for prefab-ui 0.21.x. Code is copied from the docs and was NOT all re-run. Known drift in 0.21.1: bare `{{ field }}` inside `ForEach` renders empty, so use `with ForEach("rows") as r: Text(r.field)` or `{{ $item.field }}`; charts import from `prefab_ui.components.charts`. See `gotchas.md`.

## Action Chains

**Demonstrates:** Several actions chained from one click (list in on_click): counter, toast, progress bar that changes variant, and If/Else swapping a Save button for a Saved badge. No server.

**Final code (verbatim):**

```python
from prefab_ui import PrefabApp
from prefab_ui.actions import SetState, ShowToast, ToggleState
from prefab_ui.components import (
    Badge, Button, Card, CardContent, CardHeader, CardTitle,
    Column, Muted, Progress, Row, Text,
)
from prefab_ui.components.control_flow import Else, If
from prefab_ui.rx import Rx

count = Rx("count")
saved = Rx("saved")

with PrefabApp(state={"count": 0, "saved": False}, css_class="max-w-none p-0"):
    with Card(css_class="w-full"):
        with CardHeader():
            CardTitle("Actions Demo")
            Muted("Chain multiple actions from a single click.")
        with CardContent():
            with Column(gap=4):
                with Row(gap=2, align="center"):
                    Button("Count + 1", on_click=SetState("count", count + 1))
                    Button(
                        "Count + 10", variant="secondary",
                        on_click=[
                            SetState("count", count + 10),
                            ShowToast("Jumped ahead by 10!"),
                        ],
                    )
                    Button(
                        "Reset", variant="outline",
                        on_click=[SetState("count", 0), SetState("saved", False)],
                    )
                Progress(
                    value=count, max=100,
                    variant=(count >= 100).then("success", "default"),
                )
                with Row(gap=2, align="center", css_class="justify-between"):
                    Text(f"Count: {count}")
                    with If(saved):
                        Badge("Saved", variant="success")
                    with Else():
                        Button(
                            "Save", size="sm",
                            on_click=[
                                ToggleState("saved"),
                                ShowToast(f"Saved at {count}!"),
                            ],
                        )
```

**Patterns / gotchas:**
- State seeded via PrefabApp(state={...}); `x = Rx("x")` is the handle for reading AND writing in actions.
- `SetState("count", count + 1)`: `count + 1` compiles to `{{ count + 1 }}` and is evaluated at click time (increments the current value, not a build-time capture).
- Pass a list to on_click to run actions in sequence: `[SetState(...), ShowToast("...")]`; Reset = two SetState calls.
- `ToggleState("saved")` flips a boolean; `ShowToast(f"Saved at {count}!")` interpolates live state at fire time.
- Threshold to variant inline: `(count >= 100).then("success", "default")` passed to Progress `variant`.
- `with If(saved): ... with Else(): ...` swaps components based on a boolean state key.

## Conditional Rendering

**Demonstrates:** If/Else render different components based on switch state, client-side only.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    Alert, AlertDescription, AlertTitle,
    Card, CardContent, CardHeader, CardTitle,
    Column, Switch, Text,
)
from prefab_ui.components.control_flow import Else, If
from prefab_ui.rx import Rx

dark_mode = Rx("dark_mode")
notifications = Rx("notifications")

with Card(css_class="w-full"):
    with CardHeader():
        CardTitle("Preferences")
    with CardContent():
        with Column(gap=4):
            Switch(label="Dark Mode", name="dark_mode", value=False)
            Switch(label="Notifications", name="notifications", value=True)
            with If(dark_mode):
                with Alert(variant="info"):
                    AlertTitle("Dark Mode")
                    AlertDescription("Your eyes will thank you.")
            with Else():
                with Alert(variant="warning"):
                    AlertTitle("Light Mode")
                    AlertDescription("Living dangerously, I see.")
            with If(notifications):
                Text(
                    "You'll receive alerts for all events.",
                    css_class="text-sm text-muted-foreground",
                )
            with Else():
                Text(
                    "Notifications are off. You're on your own.",
                    css_class="text-sm text-muted-foreground",
                )
```

**Patterns / gotchas:**
- `Switch(label=..., name="dark_mode", value=False)`: `name` binds the switch to the state key; `value` is the initial value (the page shows no explicit PrefabApp state; protocol state is {dark_mode:false, notifications:true}).
- `dark_mode = Rx("dark_mode")`; `with If(dark_mode): ... with Else(): ...` - branches mutually exclusive; re-evaluated on state change.
- Multiple independent If/Else pairs can read different keys side by side; no manual subscription.

## Cross-Filtering

**Demonstrates:** One Select filters every metric and chart of a dashboard, no server round-trip. Technique: pre-segment data per filter value into state, pick the active dataset with a ternary chain, compute once via Dashboard `let`.

**Final code (verbatim):**

```python
from prefab_ui import PrefabApp
from prefab_ui.components import (
    Card, CardContent, CardHeader, CardTitle,
    Dashboard, DashboardItem,
    Muted, Row, Select, SelectOption,
)
from prefab_ui.components.charts import BarChart, ChartSeries, LineChart, RadarChart
from prefab_ui.components.metric import Metric
from prefab_ui.rx import Rx

# Pre-segmented data for each region. The Select writes to `region` in state,
# and a `let` binding picks the right dataset via a ternary chain.

REGIONS = ["all", "north", "south", "east", "west"]

metrics = {
    "all":   {"revenue": 284750, "units": 12450, "avg_price": 22.87, "stores": 48},
    "north": {"revenue": 142800, "units": 4200,  "avg_price": 34.00, "stores": 8},
    "south": {"revenue": 38900,  "units": 3850,  "avg_price": 10.10, "stores": 18},
    "east":  {"revenue": 67200,  "units": 1680,  "avg_price": 40.00, "stores": 6},
    "west":  {"revenue": 35850,  "units": 2720,  "avg_price": 13.18, "stores": 16},
}

monthly = {
    "all": [
        {"month": "Jan", "sales": 42000, "returns": 3200},
        {"month": "Feb", "sales": 48500, "returns": 3800},
        {"month": "Mar", "sales": 45200, "returns": 3400},
        {"month": "Apr", "sales": 51800, "returns": 4100},
        {"month": "May", "sales": 47600, "returns": 3600},
        {"month": "Jun", "sales": 53200, "returns": 4200},
    ],
    "north": [
        {"month": "Jan", "sales": 22000, "returns": 800},
        {"month": "Feb", "sales": 25500, "returns": 900},
        {"month": "Mar", "sales": 24200, "returns": 850},
        {"month": "Apr", "sales": 27800, "returns": 1000},
        {"month": "May", "sales": 23100, "returns": 750},
        {"month": "Jun", "sales": 29200, "returns": 1100},
    ],
    "south": [
        {"month": "Jan", "sales": 5800,  "returns": 1200},
        {"month": "Feb", "sales": 6400,  "returns": 1400},
        {"month": "Mar", "sales": 5600,  "returns": 1100},
        {"month": "Apr", "sales": 7200,  "returns": 1600},
        {"month": "May", "sales": 6100,  "returns": 1300},
        {"month": "Jun", "sales": 7800,  "returns": 1700},
    ],
    "east": [
        {"month": "Jan", "sales": 8200,  "returns": 400},
        {"month": "Feb", "sales": 10600, "returns": 500},
        {"month": "Mar", "sales": 9800,  "returns": 450},
        {"month": "Apr", "sales": 11800, "returns": 550},
        {"month": "May", "sales": 12400, "returns": 500},
        {"month": "Jun", "sales": 14200, "returns": 600},
    ],
    "west": [
        {"month": "Jan", "sales": 6000,  "returns": 800},
        {"month": "Feb", "sales": 6000,  "returns": 1000},
        {"month": "Mar", "sales": 5600,  "returns": 1000},
        {"month": "Apr", "sales": 5000,  "returns": 950},
        {"month": "May", "sales": 6000,  "returns": 1050},
        {"month": "Jun", "sales": 2000,  "returns": 800},
    ],
}

categories = {
    "all":   [{"category": "Electronics", "score": 82}, {"category": "Clothing", "score": 75}, {"category": "Home", "score": 80}, {"category": "Books", "score": 65}, {"category": "Sports", "score": 70}],
    "north": [{"category": "Electronics", "score": 98}, {"category": "Clothing", "score": 40}, {"category": "Home", "score": 92}, {"category": "Books", "score": 35}, {"category": "Sports", "score": 45}],
    "south": [{"category": "Electronics", "score": 45}, {"category": "Clothing", "score": 95}, {"category": "Home", "score": 50}, {"category": "Books", "score": 90}, {"category": "Sports", "score": 88}],
    "east":  [{"category": "Electronics", "score": 95}, {"category": "Clothing", "score": 60}, {"category": "Home", "score": 90}, {"category": "Books", "score": 55}, {"category": "Sports", "score": 40}],
    "west":  [{"category": "Electronics", "score": 50}, {"category": "Clothing", "score": 88}, {"category": "Home", "score": 55}, {"category": "Books", "score": 82}, {"category": "Sports", "score": 92}],
}

trend = {
    "all":   [{"month": "Mar", "revenue": 32000}, {"month": "Apr", "revenue": 35000}, {"month": "May", "revenue": 33500}, {"month": "Jun", "revenue": 38000}, {"month": "Jul", "revenue": 41000}, {"month": "Aug", "revenue": 39500}, {"month": "Sep", "revenue": 43000}, {"month": "Oct", "revenue": 45500}, {"month": "Nov", "revenue": 48000}, {"month": "Dec", "revenue": 52000}, {"month": "Jan", "revenue": 49000}, {"month": "Feb", "revenue": 54000}],
    "north": [{"month": "Mar", "revenue": 18000}, {"month": "Apr", "revenue": 20500}, {"month": "May", "revenue": 19000}, {"month": "Jun", "revenue": 22000}, {"month": "Jul", "revenue": 24500}, {"month": "Aug", "revenue": 23000}, {"month": "Sep", "revenue": 26000}, {"month": "Oct", "revenue": 28000}, {"month": "Nov", "revenue": 30000}, {"month": "Dec", "revenue": 35000}, {"month": "Jan", "revenue": 32000}, {"month": "Feb", "revenue": 38000}],
    "south": [{"month": "Mar", "revenue": 4200},  {"month": "Apr", "revenue": 4800},  {"month": "May", "revenue": 5100},  {"month": "Jun", "revenue": 5500},  {"month": "Jul", "revenue": 5200},  {"month": "Aug", "revenue": 5800},  {"month": "Sep", "revenue": 5500},  {"month": "Oct", "revenue": 6000},  {"month": "Nov", "revenue": 5800},  {"month": "Dec", "revenue": 6200},  {"month": "Jan", "revenue": 6000},  {"month": "Feb", "revenue": 6500}],
    "east":  [{"month": "Mar", "revenue": 5500},  {"month": "Apr", "revenue": 6200},  {"month": "May", "revenue": 7000},  {"month": "Jun", "revenue": 7800},  {"month": "Jul", "revenue": 8800},  {"month": "Aug", "revenue": 9500},  {"month": "Sep", "revenue": 10500}, {"month": "Oct", "revenue": 11500}, {"month": "Nov", "revenue": 12800}, {"month": "Dec", "revenue": 14000}, {"month": "Jan", "revenue": 15500}, {"month": "Feb", "revenue": 17000}],
    "west":  [{"month": "Mar", "revenue": 8500},  {"month": "Apr", "revenue": 8200},  {"month": "May", "revenue": 7800},  {"month": "Jun", "revenue": 7200},  {"month": "Jul", "revenue": 6800},  {"month": "Aug", "revenue": 6500},  {"month": "Sep", "revenue": 6000},  {"month": "Oct", "revenue": 5500},  {"month": "Nov", "revenue": 5200},  {"month": "Dec", "revenue": 4800},  {"month": "Jan", "revenue": 4200},  {"month": "Feb", "revenue": 3500}],
}

# Flatten the nested dicts into individual state keys (metrics_north,
# monthly_south, ...) so the ternary chain can resolve them.
state = {"region": "all"}
for prefix, data in (
    ("metrics", metrics),
    ("monthly", monthly),
    ("categories", categories),
    ("trend", trend),
):
    for region in REGIONS:
        state[f"{prefix}_{region}"] = data[region]


# Helper: build a ternary expression that picks the right dataset by region
def pick(prefix):
    return (
        f"{{{{ region == 'north' ? {prefix}_north"
        f" : region == 'south' ? {prefix}_south"
        f" : region == 'east' ? {prefix}_east"
        f" : region == 'west' ? {prefix}_west"
        f" : {prefix}_all }}}}"
    )


# A `let` on the Dashboard computes intermediate values once.
# Everything inside references `m`, `chart`, `cat`, `t` instead
# of repeating the ternary chain for every prop.
with PrefabApp(state=state, css_class="max-w-none p-0"):
    with Dashboard(
        columns=12,
        row_height="auto",
        gap=4,
        let={
            "m": pick("metrics"),
            "chart": pick("monthly"),
            "cat": pick("categories"),
            "t": pick("trend"),
        },
    ):
        # Row 1: Region filter
        with DashboardItem(col=1, row=1, col_span=12):
            with Card():
                with CardContent():
                    with Row(align="center", gap=4):
                        Muted("Region")
                        with Select(name="region", css_class="w-48"):
                            SelectOption(value="all", label="All Regions")
                            SelectOption(value="north", label="North")
                            SelectOption(value="south", label="South")
                            SelectOption(value="east", label="East")
                            SelectOption(value="west", label="West")

        # Row 2: Metrics — all driven by `m` from the let binding
        m = Rx("m")
        with DashboardItem(col=1, row=2, col_span=3):
            Metric(label="Revenue", value=m.revenue.currency())
        with DashboardItem(col=4, row=2, col_span=3):
            Metric(label="Units Sold", value=m.units.number())
        with DashboardItem(col=7, row=2, col_span=3):
            Metric(label="Avg Price", value=m.avg_price.currency())
        with DashboardItem(col=10, row=2, col_span=3):
            Metric(label="Stores", value=m.stores)

        # Row 3: Bar chart + radar chart
        chart = Rx("chart")
        cat = Rx("cat")
        t = Rx("t")
        with DashboardItem(col=1, row=3, col_span=7):
            with Card(css_class="h-full"):
                with CardHeader():
                    CardTitle("Monthly Sales")
                with CardContent():
                    BarChart(
                        data=chart,
                        series=[
                            ChartSeries(data_key="sales", label="Sales", color="#2563eb"),
                            ChartSeries(data_key="returns", label="Returns", color="#e76e50"),
                        ],
                        x_axis="month",
                        stacked=True,
                        bar_radius=0,
                        show_legend=True,
                        height=250,
                    )

        with DashboardItem(col=8, row=3, col_span=5):
            with Card(css_class="h-full"):
                with CardHeader():
                    CardTitle("Category Performance")
                with CardContent():
                    RadarChart(
                        data=cat,
                        series=[ChartSeries(data_key="score", label="Score")],
                        axis_key="category",
                        show_dots=True,
                        height=250,
                    )

        # Row 4: 12-month trend
        with DashboardItem(col=1, row=4, col_span=12):
            with Card():
                with CardHeader():
                    CardTitle("Revenue Trend (12 months)")
                with CardContent():
                    LineChart(
                        data=t,
                        series=[ChartSeries(data_key="revenue", label="Revenue", color="#2563eb")],
                        x_axis="month",
                        curve="smooth",
                        show_dots=True,
                        height=200,
                    )
```

**Patterns / gotchas:**
- Pre-segment data per filter value and put ALL variants in state up front (flattened keys `metrics_north`, `monthly_south`, ...).
- `Select(name="region")` auto-binds its value to `state.region`; picking an option sets region and re-evaluates all dependent expressions.
- `pick(prefix)` helper builds a ternary-chain string `{{ region == 'north' ? metrics_north : region == 'south' ? ... : metrics_all }}`.
- `Dashboard(let={"m": pick("metrics"), ...})` computes intermediate values once; children use `m = Rx("m")`, `m.revenue.currency()`, `m.units.number()`, and pass `data=chart` (Rx) to charts. Avoids repeating the ternary per prop.
- Formatting pipes: `{{ m.revenue | currency }}` -> "$284,750"; `| number` -> "12,450"; `m.avg_price | currency` -> "$22.87". Live expressions.
- Dashboard grid: `Dashboard(columns=12, row_height="auto", gap=4)` with `DashboardItem(col=, row=, col_span=)`.
- Charts: BarChart(stacked=True, bar_radius=0, x_axis, series=[ChartSeries(data_key,label,color)]), RadarChart(axis_key, show_dots), LineChart(curve="smooth").
- Gotcha/note: the page's own explanation notes nested dicts must be flattened into individual state keys so the ternary chain can resolve them (see code comment).

## Deploy Pipeline

**Demonstrates:** CI/CD tracker: a DataTable whose cells are components (Span, Badge, Progress) with sort and search. Static client-side data.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    Badge, Card, CardContent, CardDescription, CardHeader, CardTitle,
    DataTable, DataTableColumn, Div, Progress, Span,
)

services = [
    ("auth-service", "Production", 100, "success"),
    ("data-ingest", "Staging", 72, "default"),
    ("ml-pipeline", "Canary", 45, "warning"),
    ("web-frontend", "Rolling", 88, "default"),
    ("event-bus", "Blocked", 12, "destructive"),
    ("cache-layer", "Production", 100, "success"),
    ("search-index", "Rolling", 63, "default"),
]

rows = []
for name, stage, pct, variant in services:
    rows.append({
        "service": Span(name, css_class="font-semibold text-card-foreground"),
        "stage": Badge(stage, variant=variant),
        "progress": Progress(value=pct, max=100, variant=variant, size="lg"),
        "status": Badge(f"{pct}%", variant=variant),
    })

with Card(css_class="w-full"):
    with CardHeader():
        CardTitle("Deploy Pipeline")
        CardDescription("Current deployment status across all services")
    with CardContent():
        DataTable(
            columns=[
                DataTableColumn(key="service", header="Service", sortable=True),
                DataTableColumn(key="stage", header="Stage", align="center"),
                DataTableColumn(key="progress", header="Rollout", width="200px"),
                DataTableColumn(key="status", header="", align="right"),
            ],
            rows=rows,
            search=True,
        )
```

**Patterns / gotchas:**
- DataTable `rows` are dicts whose values may be fully constructed components (Span/Badge/Progress), not just strings; the table doubles as a layout grid.
- Compute one `variant` per row in Python (success/warning/default/destructive) and thread it into stage Badge, Progress, and status Badge so they cannot disagree.
- Column config: `width="200px"` fixed width, `align="center"|"right"`, empty `header=""`, `sortable=True` only on Service; `search=True` gives a filter box.
- Static data means no server round trip. To make it live, fetch data with a Fetch or CallTool action (runs on client, calls server) and write the response into state via `on_success` reading `$result`; the table rebuilds reactively.

## Dynamic List

**Demonstrates:** Add/remove list items with ForEach, AppendState, PopState; count via length pipe.

**Final code (verbatim):**

```python
from prefab_ui import PrefabApp
from prefab_ui.actions import AppendState, PopState, SetState
from prefab_ui.components import (
    Button, Card, CardContent, CardFooter, CardHeader, CardTitle,
    Column, Input, Muted, Row, Separator, Text,
)
from prefab_ui.components.control_flow import ForEach
from prefab_ui.rx import INDEX, ITEM, Rx

new_task = Rx("new_task")
tasks = Rx("tasks")

with PrefabApp(
    state={"tasks": ["Buy towel", "Learn Python", "Don't panic"], "new_task": ""},
    css_class="max-w-none p-0",
):
    with Card(css_class="w-full"):
        with CardHeader():
            CardTitle("Task List")
            Muted(f"{tasks.length()} items")
        with CardContent():
            with Column(gap=3):
                with Row(gap=2):
                    Input(name="new_task", placeholder="Add a task...")
                    Button(
                        "Add",
                        on_click=[
                            AppendState("tasks", new_task),
                            SetState("new_task", ""),
                        ],
                    )
                Separator()
                with ForEach(tasks):
                    with Row(gap=2, align="center", css_class="justify-between"):
                        Text(ITEM)
                        Button(
                            "Remove", variant="outline", size="sm",
                            on_click=PopState("tasks", index=INDEX),
                        )
        with CardFooter():
            Button("Clear All", variant="destructive", on_click=SetState("tasks", []))
```

**Patterns / gotchas:**
- State: `tasks` (list) and `new_task` (input buffer); `Input(name="new_task")` two-way binds.
- Add: `on_click=[AppendState("tasks", new_task), SetState("new_task", "")]` (new_task is Rx so read at click time; then clear the box).
- `with ForEach(tasks):` iterates a state key; `ITEM` and `INDEX` (from prefab_ui.rx) are the current element and position.
- Remove by index: `PopState("tasks", index=INDEX)`. Clear: `SetState("tasks", [])`.
- Count: `tasks.length()` compiles to a `length` pipe, recomputed on every state change.

## Expense Tracker

**Demonstrates:** Sortable DataTable with component cells, PieChart breakdown, Metrics, and a budget Alert. All math in plain Python; no state or reactive expressions.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    Alert, AlertDescription, AlertTitle,
    Badge, Card, CardContent, CardDescription, CardHeader, CardTitle,
    Column, DataTable, DataTableColumn, Grid, Metric, Row, Separator,
)
from prefab_ui.components.charts import ChartSeries, PieChart

expenses = [
    ("Compute", 42_000, "cloud"),
    ("Storage", 18_500, "database"),
    ("Network", 12_300, "wifi"),
    ("Monitoring", 4_200, "activity"),
    ("CI/CD", 3_800, "git-branch"),
    ("Support", 2_100, "headphones"),
]

total = sum(cost for _, cost, _ in expenses)
budget = 95_000

rows = []
for name, cost, _icon in expenses:
    pct = round(cost / total * 100)
    variant = "destructive" if pct > 40 else "default" if pct > 15 else "secondary"
    rows.append({
        "category": Badge(name, variant=variant),
        "amount": f"${cost:,}",
        "share": Badge(f"{pct}%", variant=variant),
    })

pie_data = [{"category": name, "cost": cost} for name, cost, _ in expenses]

with Column(gap=4):
    with Grid(columns=2, gap=4):
        with Card():
            with CardContent():
                Metric(label="Total Spend", value=f"${total:,}", delta="+6.2% MoM")
        with Card():
            with CardContent():
                Metric(
                    label="Budget Remaining",
                    value=f"${budget - total:,}",
                    delta=f"{round((budget - total) / budget * 100)}% left",
                )

    with Card():
        with CardHeader():
            CardTitle("Monthly Breakdown")
            CardDescription("March 2026")
        with CardContent():
            with Column(gap=6):
                PieChart(
                    data=pie_data,
                    data_key="cost",
                    name_key="category",
                    height=220,
                    inner_radius=50,
                    show_legend=True,
                    show_tooltip=True,
                )
                Separator()
                DataTable(
                    columns=[
                        DataTableColumn(key="category", header="Category", sortable=True),
                        DataTableColumn(key="amount", header="Amount", align="right", sortable=True),
                        DataTableColumn(key="share", header="Share", align="right"),
                    ],
                    rows=rows,
                    search=True,
                )

    with Alert(variant="warning", icon="triangle-alert"):
        AlertTitle("Approaching Budget Limit")
        AlertDescription(
            f"${total:,} of ${budget:,} used ({round(total / budget * 100)}%). "
            "Review compute costs for optimization opportunities."
        )
```

**Patterns / gotchas:**
- Compute totals, percentages, variants in Python before building components (`variant = "destructive" if pct > 40 else "default" if pct > 15 else "secondary"`).
- Component cells in DataTable rows (`Badge(name, variant=variant)`); the table still sorts and searches on underlying row data.
- Derive a separate chart-shaped projection (`pie_data`) from the same source list: PieChart(data_key="cost", name_key="category", inner_radius=50 for donut).
- Alert text computed from the same totals; alert is rendered unconditionally.
- Page suggests: for editable expenses, lift `expenses` into state and recompute totals/chart/table/alert via reactive expressions.

## File Upload

**Demonstrates:** DropZone writing file descriptors into state; list, remove, and clear files, all client-side. In practice forward the base64 payload to a backend tool with CallTool so bytes stay out of the LLM context window.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    STATE as state, Badge, Button, Card, CardContent, CardFooter,
    CardHeader, Column, DropZone,
    H3, Muted, Row, Small,
)
from prefab_ui.components.control_flow import Else, ForEach, If
from prefab_ui.actions import PopState, SetState


with Card(css_class="w-full max-w-2xl") as view:
    with CardHeader():
        with Row(gap=2, align="center"):
            H3("File Inbox")
            with If(state.files.length()):
                Badge(state.files.length(), variant="secondary")

    with CardContent():
        with Column(gap=4):
            DropZone(
                icon="inbox",
                label="Drop files here",
                description="Don't worry, files aren't actually uploaded",
                multiple=True,
                max_size=10_000_000,
                name="files",
            )

            with If(state.files.length()):
                with Column(gap=2):
                    with ForEach("files") as (i, item):
                        with Row(gap=3, align="center"):
                            with Column(gap=0):
                                Small(item.name)
                                Muted(f"{item.type} · {item.size} bytes")
                            Button(
                                "×",
                                variant="ghost",
                                size="sm",
                                css_class=(
                                    "ml-auto h-6 w-6 p-0"
                                    " text-muted-foreground"
                                ),
                                on_click=PopState("files", i),
                            )

    with CardFooter():
        with Row(align="center", css_class="w-full"):
            with If(state.files.length()):
                Muted(
                    f"{state.files.length()}"
                    f" {state.files.length().pluralize('file')}"
                )
            with Else():
                Muted("No files uploaded")
            with If(state.files.length()):
                Button(
                    "Clear all",
                    variant="outline",
                    size="sm",
                    css_class="ml-auto",
                    on_click=SetState("files", []),
                )
```

**Patterns / gotchas:**
- `DropZone(name="files", multiple=True, max_size=...)` writes a list of descriptors (`name`, `type`, `size` plus base64 contents) to state key `files`.
- `from prefab_ui.components import STATE as state`; `state.files.length()` compiles to a reactive expression; `If(state.files.length())` shows things only when files exist; `Else()` for empty message.
- `with ForEach("files") as (i, item):` exposes index and item; `item.name`, `item.type`, `item.size`.
- Remove one: `PopState("files", i)`; clear: `SetState("files", [])`.
- `state.files.length().pluralize('file')` for pluralization.
- Real upload: wire DropZone `on_change` (or a button `on_click`) to `CallTool(...)` with the payload from `state.files`; server processes, returns result; read `$result` in `on_success` and write it into state. Binary goes client -> server directly, never through the model context.

## Reactive Binding

**Demonstrates:** One Slider drives a Ring, four Progress bars, and a text status via Rx arithmetic, ternaries and f-strings.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    Card, CardContent, CardHeader, CardTitle,
    Column, Grid, Muted, Progress, Ring, Row, Slider, Text,
)
from prefab_ui.rx import Rx

level = Rx("level")
variant = (level > 75).then(
    "destructive", (level > 40).then("warning", "success")
)

with Card(css_class="w-full"):
    with CardHeader():
        CardTitle("Power Level")
    with CardContent():
        with Column(gap=6):
            Slider(name="level", min=0, max=100, value=50)
            with Row(gap=6, align="center"):
                Ring(
                    value=level, label=f"{level}%",
                    variant=variant, size="lg", thickness=10,
                )
                with Grid(columns=2, gap=4, css_class="flex-1"):
                    with Column(gap=1):
                        Muted("Primary")
                        Progress(value=level, max=100, variant=variant)
                    with Column(gap=1):
                        Muted("Inverse")
                        Progress(value=100 - level, max=100, variant="info")
                    with Column(gap=1):
                        Muted("Doubled")
                        Progress(value=level * 2, max=100, variant="default")
                    with Column(gap=1):
                        Muted("Halved")
                        Progress(value=level / 2, max=100, variant="success")
            Text(
                f"Level is {level}% — "
                f"{(level > 75).then('critical!', (level > 40).then('nominal', 'low'))}",
                css_class="text-sm text-muted-foreground text-center",
            )
```

**Patterns / gotchas:**
- `Slider(name="level", ...)` binds to state key; `level = Rx("level")`.
- Python operators on Rx build expressions: `100 - level`, `level * 2`, `level / 2` -> `{{ ... }}` strings evaluated live.
- Compute a shared variant once: `(level > 75).then("destructive", (level > 40).then("warning", "success"))` (nested ternary) and reuse across Ring and Progress.
- f-strings embed Rx: `f"{level}%"`, and inline `.then()` chains inside f-strings swap words.
- Single source of truth (one state key), everything else derived.

## Sales Dashboard

**Demonstrates:** Full analytics dashboard: 4 KPI metrics, AreaChart + donut PieChart, searchable paginated orders DataTable. Static data embedded; renderer handles interactivity client-side.

**Final code (verbatim):**

```python
from prefab_ui.components import (
    Card, CardContent, CardHeader, CardTitle,
    Dashboard, DashboardItem,
    DataTable, DataTableColumn,
    Muted, Row,
)
from prefab_ui.components.charts import AreaChart, ChartSeries, PieChart
from prefab_ui.components.metric import Metric

monthly = [
    {"month": "Sep", "revenue": 38200, "costs": 22100},
    {"month": "Oct", "revenue": 41500, "costs": 23400},
    {"month": "Nov", "revenue": 45800, "costs": 24800},
    {"month": "Dec", "revenue": 52100, "costs": 27200},
    {"month": "Jan", "revenue": 48900, "costs": 25600},
    {"month": "Feb", "revenue": 58250, "costs": 28900},
]

categories = [
    {"category": "Electronics", "revenue": 98600},
    {"category": "Clothing", "revenue": 67200},
    {"category": "Home", "revenue": 54300},
    {"category": "Books", "revenue": 38400},
    {"category": "Sports", "revenue": 26250},
]

orders = [
    {"id": "ORD-7842", "customer": "Acme Corp", "product": "Laptop Pro", "total": "$1,249.99", "status": "Shipped", "date": "Feb 18"},
    {"id": "ORD-7841", "customer": "Globex Inc", "product": "Wireless Mouse", "total": "$42.00", "status": "Delivered", "date": "Feb 17"},
    {"id": "ORD-7840", "customer": "Initech", "product": "Standing Desk", "total": "$599.00", "status": "Processing", "date": "Feb 17"},
    {"id": "ORD-7839", "customer": "Umbrella LLC", "product": "Monitor 27\"", "total": "$389.99", "status": "Shipped", "date": "Feb 16"},
    {"id": "ORD-7838", "customer": "Stark Industries", "product": "Keyboard MX", "total": "$179.00", "status": "Delivered", "date": "Feb 16"},
    {"id": "ORD-7837", "customer": "Wayne Enterprises", "product": "Webcam HD", "total": "$89.99", "status": "Delivered", "date": "Feb 15"},
    {"id": "ORD-7836", "customer": "Cyberdyne", "product": "USB Hub", "total": "$34.99", "status": "Shipped", "date": "Feb 15"},
    {"id": "ORD-7835", "customer": "Oscorp", "product": "Headphones Pro", "total": "$299.00", "status": "Processing", "date": "Feb 14"},
]

with Dashboard(columns=12, row_height="auto", gap=4):
    # Row 1: KPI metrics in cards
    with DashboardItem(col=1, row=1, col_span=3):
        with Card():
            with CardContent():
                Metric(label="Revenue", value="$284,750", delta="+12.5%", trend="up", trend_sentiment="positive")
    with DashboardItem(col=4, row=1, col_span=3):
        with Card():
            with CardContent():
                Metric(label="Orders", value="1,842", delta="+8.2%", trend="up", trend_sentiment="positive")
    with DashboardItem(col=7, row=1, col_span=3):
        with Card():
            with CardContent():
                Metric(label="Avg Order", value="$154.59", delta="-3.1%", trend="down", trend_sentiment="negative")
    with DashboardItem(col=10, row=1, col_span=3):
        with Card():
            with CardContent():
                Metric(label="Growth", value="12.5%", delta="+2.4pp", trend="up", trend_sentiment="positive")

    # Row 2: Revenue trend + category breakdown
    with DashboardItem(col=1, row=2, col_span=8):
        with Card(css_class="h-full"):
            with CardHeader():
                CardTitle("Revenue Over Time")
            with CardContent():
                AreaChart(
                    data=monthly,
                    series=[
                        ChartSeries(data_key="revenue", label="Revenue", color="#2563eb"),
                        ChartSeries(data_key="costs", label="Costs", color="#e76e50"),
                    ],
                    x_axis="month",
                    curve="smooth",
                    show_legend=True,
                    value_format="compact",
                    height=250,
                )

    with DashboardItem(col=9, row=2, col_span=4):
        with Card(css_class="h-full"):
            with CardHeader():
                CardTitle("Revenue by Category")
            with CardContent():
                PieChart(
                    data=categories,
                    data_key="revenue",
                    name_key="category",
                    inner_radius=60,
                    show_legend=True,
                    height=250,
                )

    # Row 3: Orders table
    with DashboardItem(col=1, row=3, col_span=12):
        with Card():
            with CardHeader():
                with Row(align="center", css_class="justify-between"):
                    CardTitle("Recent Orders")
                    Muted("Last 7 days")
            with CardContent():
                DataTable(
                    columns=[
                        DataTableColumn(key="id", header="Order ID", sortable=True),
                        DataTableColumn(key="customer", header="Customer", sortable=True),
                        DataTableColumn(key="product", header="Product"),
                        DataTableColumn(key="total", header="Total", sortable=True),
                        DataTableColumn(key="status", header="Status"),
                        DataTableColumn(key="date", header="Date", sortable=True),
                    ],
                    rows=orders,
                    search=True,
                    paginated=True,
                    page_size=5,
                )
```

**Patterns / gotchas:**
- `Dashboard(columns=12, row_height="auto", gap=4)` + `DashboardItem(col, row, col_span)`: rows of 3x3-col metrics, 8+4, then 12.
- `Metric(label, value, delta, trend="up"|"down", trend_sentiment="positive"|"negative")` gives colored arrows/delta badges (red for declining avg order).
- AreaChart with two ChartSeries, `curve="smooth"`, `show_legend=True`, `value_format="compact"`; PieChart `inner_radius=60` for donut.
- DataTable `search=True, paginated=True, page_size=5`, sortable columns on selected keys.
- Cards use `css_class="h-full"` inside DashboardItem to fill the cell.

## Server Dashboard

**Demonstrates:** Simulated live-updating server dashboard auto-refreshing every 400ms with sparklines, health badge, and progress bar, driven by one counter.

**Final code (verbatim):**

```python
from prefab_ui import PrefabApp
from prefab_ui.actions import SetInterval, SetState
from prefab_ui.components import (
    Badge, Card, CardContent, CardHeader, CardTitle,
    Column, Grid, Metric, Muted, Progress, Row, Separator, Text,
)
from prefab_ui.components.charts import Sparkline
from prefab_ui.rx import Rx

tick = Rx("tick")
cpu = tick % 20 * 4 + 15
mem = tick % 30 * 2 + 40
cpu_variant = (cpu > 80).then("destructive", (cpu > 50).then("warning", "success"))

# Live-ticking footer stats
requests = 12000 + tick % 50 * 30
latency = 120 + tick % 30

with PrefabApp(
    state={"tick": 0},
    on_mount=SetInterval(400, on_tick=SetState("tick", tick + 1)),
    css_class="max-w-md p-0",
):
    with Column(gap=4):
        with Grid(columns=2, gap=4):
            with Card(css_class="gap-0 pb-0 overflow-hidden"):
                with CardContent():
                    Metric(label="CPU Usage", value=f"{cpu}%")
                Sparkline(
                    data=[35, 42, 38, 55, 48, 62, 58, 70, 65, 45],
                    variant="info", fill=True, css_class="h-10",
                )
            with Card(css_class="gap-0 pb-0 overflow-hidden"):
                with CardContent():
                    Metric(label="Memory", value=f"{mem}%")
                Sparkline(
                    data=[60, 62, 58, 65, 63, 68, 64, 70, 66, 62],
                    variant="success", fill=True, css_class="h-10",
                )

        with Card():
            with CardHeader():
                with Row(align="center", css_class="justify-between"):
                    CardTitle("System Health")
                    Badge(cpu_variant, variant=cpu_variant)
            with CardContent():
                with Column(gap=4):
                    with Row(gap=4, align="center", css_class="justify-between"):
                        Text(f"CPU: {cpu}%")
                        Muted(f"Memory: {mem}%")
                    Progress(value=cpu, max=100, variant=cpu_variant)
                    Separator()
                    with Row(gap=6):
                        Metric(label="Uptime", value=f"99.9{tick % 10}%")
                        Metric(label="Requests/s", value=requests.number())
                        Metric(label="p99 Latency", value=f"{latency}ms")
```

**Patterns / gotchas:**
- `on_mount=SetInterval(400, on_tick=SetState("tick", tick + 1))` on PrefabApp: client-side timer, no server.
- Derive values with Rx arithmetic: `cpu = tick % 20 * 4 + 15` (modulo keeps values bounded); `requests.number()` formatting; f-strings like `f"99.9{tick % 10}%"`.
- Threshold to variant: `cpu_variant = (cpu > 80).then("destructive", (cpu > 50).then("warning", "success"))` feeds Badge label/variant and Progress variant, keeping them in lockstep.
- Sparkline data is static (`variant`, `fill=True`, `css_class="h-10"`); live feel comes only from expressions reacting to tick.
- Python script runs once; the browser owns the clock.

## The Button

**Demonstrates:** A single button escalating through four states using If/Elif/Else on a press counter and SetState.

**Final code (verbatim):**

```python
from prefab_ui import PrefabApp
from prefab_ui.actions import SetState
from prefab_ui.components import (
    Alert, AlertDescription, AlertTitle, Badge, Button, Card, CardContent,
    CardFooter, CardHeader, CardTitle, Column, Loader,
    Muted, Progress, Row, Text,
)
from prefab_ui.components.control_flow import Elif, Else, If
from prefab_ui.rx import Rx

presses = Rx("presses")

with PrefabApp(state={"presses": 0}, css_class="max-w-none p-0"):
    with Card(css_class="w-full"):
        with CardHeader():
            with Row(align="center", css_class="justify-between"):
                CardTitle("The Button")
                with If(presses > 0):
                    Badge(presses, variant="secondary")
        with CardContent():
            with Column(gap=4):
                with If(presses == 0):
                    Button(
                        "This is probably the best button to press",
                        variant="success",
                        on_click=SetState(presses, presses + 1),
                    )
                with Elif(presses == 1):
                    with Alert(variant="info", icon="info"):
                        AlertTitle("Thank you!")
                        AlertDescription(
                            "Your cooperation has been noted and will be reported."
                        )
                    Button(
                        "Please do not press this button again",
                        variant="outline",
                        on_click=SetState(presses, presses + 1),
                    )
                with Elif(presses == 2):
                    with Alert(variant="warning", icon="alert-triangle"):
                        AlertTitle("We did ask nicely")
                        AlertDescription("Management has been informed.")
                    Progress(value=66, max=100, indicator_class="bg-yellow-500")
                    Muted("Patience remaining: 34%")
                    Button(
                        "Please do not press this button again",
                        variant="destructive",
                        on_click=SetState(presses, presses + 1),
                    )
                with Elif(presses == 3):
                    with Alert(variant="destructive", icon="alert-triangle"):
                        AlertTitle("Now look what you've done")
                        AlertDescription(
                            "The improbability drive has been activated."
                        )
                    Progress(value=100, max=100, indicator_class="bg-red-500")
                    with Row(gap=2, align="center"):
                        Loader(variant="spin", size="sm")
                        Muted("Recalculating the probability of your existence...")
                    Button(
                        "OK maybe press it one more time",
                        variant="ghost",
                        on_click=SetState(presses, 0),
                    )
                with Else():
                    Text("This should not happen.")
        with CardFooter():
            with If(presses > 0):
                Muted("Share and Enjoy!")
```

**Patterns / gotchas:**
- One integer `presses` is the whole state; the screen is purely a function of it.
- `If(presses == 0)` / `Elif(presses == 1..3)` / `Else()` chain; exactly one branch renders. Else is a safety net.
- Advance: `on_click=SetState(presses, presses + 1)` (note: first arg here is the Rx object `presses`, not a string); reset: `SetState(presses, 0)`.
- Guards in header/footer: `with If(presses > 0): Badge(presses, ...)`.
- Progress `indicator_class="bg-yellow-500"`/`"bg-red-500"` for colour; Alert with `icon=`; `Loader(variant="spin", size="sm")`.

## Threshold Meter

**Demonstrates:** Slider drives a Progress bar whose colour class changes at thresholds; uses a forward-declared anonymous Rx binding.

**Final code (verbatim):**

```python
from prefab_ui.components import Column, H3, Muted, Progress, Row, Slider, Text
from prefab_ui.rx import Rx

val = Rx(lambda: slider)

with Column(gap=6, css_class="max-w-sm mx-auto"):
    H3("Health Monitor")
    Muted("Drag the slider — the bar color changes at each threshold.")

    with Column(gap=4):
        with Row(css_class="justify-between items-center"):
            Text("CPU Usage")
            Text((val / 100).percent(), bold=True)
        Progress(
            value=val,
            indicator_class=(val < 20).then(
                "bg-red-500",
                (val < 60).then(
                    "bg-primary",
                    (val < 75).then("bg-amber-500", "bg-green-500"),
                ),
            ),
        )
        slider = Slider(min=0, max=100, step=1, value=50)
```

**Patterns / gotchas:**
- Anonymous binding: Slider with no `name` auto-generates a state key; `val = Rx(lambda: slider)` forward-declares the reference (lambda resolves at render time) so components above the slider can use it.
- Nested `.then()` chain mapping thresholds to Tailwind classes passed to `indicator_class` (compiles to nested ternary like `{{ slider_1 < 20 ? 'bg-red-500' : ... }}`).
- `(val / 100).percent()` formats a fraction as percentage; `Text(..., bold=True)`.
- Each `.then(a, b)` = use a if condition holds, else fall through to b.

## Todo List

**Demonstrates:** Multiple todo lists (groups) with inline editing, add-validation, show/hide done, and dynamic groups, all client-side.

**Final code (verbatim):**

```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Button, Card, CardContent, CardFooter, CardHeader,
    Checkbox, Column, Form, Grid, Input, Muted, Row, Separator,
)
from prefab_ui.components.control_flow import ForEach, If
from prefab_ui.actions import AppendState, PopState, SetState
from prefab_ui.rx import Rx

# Each group has a name, a list of todos, an input buffer, and a visibility flag
with Grid(min_column_width="12rem", gap=6, align="start") as view:

    # Destructure to capture the group index (gi) and the group itself.
    # Each ForEach auto-captures $item and $index into scoped let bindings,
    # so nested loops don't shadow each other.
    with ForEach("groups") as (gi, group):
        with Card():
            with CardHeader():
                with Row(gap=2, align="center"):
                    Input(
                        name=f"groups.{gi}.name",
                        css_class="border-0 ring-0 shadow-none p-0 h-auto font-semibold text-lg focus-visible:ring-0 focus-visible:ring-offset-0",
                    )
                    Button("×", variant="ghost", size="sm", css_class="ml-auto", on_click=PopState("groups", gi))
            with CardContent():
                with Column(gap=4):
                    with Form(gap=0, on_submit=[
                        AppendState(f"groups.{gi}.todos", {"text": group.new_todo, "done": False}),
                        SetState(f"groups.{gi}.new_todo", ""),
                    ]):
                        with Row(gap=2):
                            Input(name=f"groups.{gi}.new_todo", placeholder="Add a todo...")
                            Button("Add", disabled=~group.new_todo)

                    with Column(gap=2):
                        with If(group.todos.length()):
                            Separator(spacing=3)
                        with ForEach(f"groups.{gi}.todos") as (ti, todo):
                            with If(~todo.done | group.show_done):
                                with Row(gap=2, align="center"):
                                    Checkbox(name=f"groups.{gi}.todos.{ti}.done")
                                    Input(
                                        name=f"groups.{gi}.todos.{ti}.text",
                                        css_class="border-0 ring-0 shadow-none p-0 h-auto focus-visible:ring-0 focus-visible:ring-offset-0",
                                    )
                                    Button("×", variant="ghost", size="sm", css_class="ml-auto", on_click=PopState(f"groups.{gi}.todos", ti))

            with CardFooter():
                with Row(gap=2, align="center", css_class="w-full justify-between"):
                    Muted(f"{group.todos.length()} items")
                    with Row(gap=1, align="center"):
                        Checkbox(name=f"groups.{gi}.show_done", css_class="h-3 w-3")
                        Muted("Show done")

    with Card(css_class="border-dashed p-3"):
        Button(
            "+",
            variant="ghost",
            size="lg",
            css_class="text-4xl text-muted-foreground w-full h-full min-h-48 rounded-md",
            on_click=AppendState("groups", {"name": "New List", "todos": [], "new_todo": "", "show_done": True}),
        )

app = PrefabApp(
    state={
        "groups": [
            {
                "name": "Work",
                "todos": [
                    {"text": "Find Magrathea", "done": False},
                    {"text": "Escape Vogons", "done": False},
                ],
                "new_todo": "",
                "show_done": True,
            },
            {
                "name": "Personal",
                "todos": [
                    {"text": "Have lunch at Milliways", "done": True},
                    {"text": "Buy towel", "done": False},
                ],
                "new_todo": "",
                "show_done": True,
            },
        ],
    },
    view=view,
)
```

**Patterns / gotchas:**
- State: array of groups each with `name`, `todos`, `new_todo` buffer, `show_done`.
- Nested loops: `with ForEach("groups") as (gi, group)` and `with ForEach(f"groups.{gi}.todos") as (ti, todo)`; each ForEach auto-captures $item/$index into scoped `let` bindings so outer `group`/`gi` survive inner shadowing.
- Dot-path auto-binding: `Input(name=f"groups.{gi}.todos.{ti}.text")`, `Checkbox(name=f"groups.{gi}.todos.{ti}.done")` read and write exact item in state.
- Inline editing: borderless Input styled `border-0 ring-0 shadow-none p-0 h-auto ...` looks like text but is editable.
- Form submit: `Form(on_submit=[AppendState(f"groups.{gi}.todos", {"text": group.new_todo, "done": False}), SetState(f"groups.{gi}.new_todo", "")])`.
- Disable button when empty: `Button("Add", disabled=~group.new_todo)`.
- Hide completed: `If(~todo.done | group.show_done)` (Rx `~` not, `|` or).
- Remove by dot-path index: `PopState(f"groups.{gi}.todos", ti)`; add group: `AppendState("groups", {...})`.
- Here the final view is passed to `PrefabApp(state=..., view=view)`; view built with `as view` contexts (Grid min_column_width).
