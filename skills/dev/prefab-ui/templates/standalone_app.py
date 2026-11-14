"""Standalone Prefab app: no backend, all state lives in the browser.

Run:     prefab serve standalone_app.py --reload      (http://127.0.0.1:5175)
Export:  prefab export standalone_app.py [--bundled]  (static HTML file)
"""
from prefab_ui.app import PrefabApp
from prefab_ui.actions import AppendState, PopState, SetState, ShowToast
from prefab_ui.components import (
    Badge, Button, Card, CardContent, CardDescription, CardHeader, CardTitle,
    Column, DataTable, DataTableColumn, Grid, H1, Input, Metric, Muted, Row, Tab,
    Tabs, Text,
)
from prefab_ui.components.charts import BarChart, ChartSeries
from prefab_ui.components.control_flow import ForEach
from prefab_ui.rx import Rx

TEAM = [
    {"name": "Anna", "dept": "Dev", "salary": 5000},
    {"name": "Boris", "dept": "Dev", "salary": 4500},
    {"name": "Vera", "dept": "Design", "salary": 4000},
]
who = Rx("who")
todos = Rx("todos")
new_todo = Rx("new_todo")

with PrefabApp(
    title="My dashboard",
    state={"who": "world", "todos": ["First task"], "new_todo": "", "tab": "overview"},
    css_class="p-6 max-w-5xl mx-auto",
) as app:
    with Column(gap=4):
        H1(f"Hello, {who}!")
        Input(name="who", placeholder="Your name")
        with Tabs(name="tab", value="overview"):
            with Tab("Overview", value="overview"):
                with Column(gap=4):
                    with Grid(columns=3, gap=3):
                        Metric(label="People", value=str(len(TEAM)))
                        Metric(label="Payroll", value=f"${sum(p['salary'] for p in TEAM):,}")
                        Metric(label="Status", value="OK", trend="up", trend_sentiment="positive")
                    with Card():
                        with CardHeader():
                            CardTitle("Salaries")
                        with CardContent():
                            BarChart(data=TEAM, x_axis="name", height=220,
                                     series=[ChartSeries(data_key="salary", label="Salary")])
            with Tab("Table", value="table"):
                DataTable(
                    columns=[DataTableColumn(key="name", header="Name", sortable=True),
                             DataTableColumn(key="dept", header="Dept", sortable=True),
                             DataTableColumn(key="salary", header="Salary", sortable=True)],
                    rows=TEAM, search=True, paginated=True, page_size=10,
                )
            with Tab("Todos", value="todos"):
                with Card():
                    with CardHeader():
                        CardTitle("Todos")
                        CardDescription("AppendState / PopState, no server")
                    with CardContent():
                        with Column(gap=3):
                            with Row(gap=2):
                                Input(name="new_todo", placeholder="New task")
                                Button("Add", on_click=[
                                    AppendState("todos", new_todo),
                                    SetState("new_todo", ""),
                                    ShowToast("Added", variant="success"),
                                ])
                            with Column(gap=1):
                                with ForEach("todos") as (i, t):      # (index, item) unpacking
                                    with Row(gap=2):
                                        Text(t)
                                        Button("x", variant="ghost", size="sm", on_click=PopState("todos", i))
                            Muted(f"{todos.length()} total")
