"""FastMCP server whose tools return Prefab UI (MCP Apps).

pip install "fastmcp[apps]" "prefab-ui>=0.21,<0.22"
Run (stdio):  python mcp_server.py
Claude Code:  claude mcp add prefab-demo -- /abs/path/.venv/bin/python /abs/path/mcp_server.py
Try without a host: python test_client.py
"""
from fastmcp import FastMCP
from fastmcp.apps import AppConfig

from prefab_ui.actions import CallTool, SetState, ShowToast
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Button, Card, CardContent, CardDescription, CardHeader, CardTitle, Column,
    DataTable, DataTableColumn, Input, Metric, Row, Text,
)
from prefab_ui.components.charts import BarChart, ChartSeries
from prefab_ui.components.control_flow import ForEach
from prefab_ui.rx import ERROR, RESULT, Rx

mcp = FastMCP("Prefab Demo")

TEAM = [
    {"name": "Anna", "dept": "Dev", "salary": 5000},
    {"name": "Boris", "dept": "Dev", "salary": 4500},
    {"name": "Vera", "dept": "Design", "salary": 4000},
]
NOTES: list[str] = ["First note"]


# 1) Simplest: return a bare component -> FastMCP wraps it in a PrefabApp.
@mcp.tool(app=True)
def team_table() -> DataTable:
    """Show the team as a searchable, sortable table."""
    return DataTable(
        columns=[DataTableColumn(key="name", header="Name", sortable=True),
                 DataTableColumn(key="dept", header="Dept", sortable=True),
                 DataTableColumn(key="salary", header="Salary", sortable=True)],
        rows=TEAM, search=True,
    )


# 2) Return a PrefabApp when you need state, a title, theme, etc.
@mcp.tool(app=True)
def team_dashboard() -> PrefabApp:
    """Team dashboard: metrics and a salary chart."""
    with PrefabApp(title="Team", css_class="p-4") as app:
        with Column(gap=4):
            with Row(gap=4):
                Metric(label="People", value=str(len(TEAM)))
                Metric(label="Payroll", value=f"${sum(p['salary'] for p in TEAM):,}")
            BarChart(data=TEAM, x_axis="name", height=200,
                     series=[ChartSeries(data_key="salary", label="Salary")])
    return app


# 3) Interactive app: the UI calls a server tool with CallTool.
@mcp.tool(app=True)
def notes_app() -> PrefabApp:
    """Open the notes app."""
    text = Rx("text")
    with PrefabApp(state={"notes": list(NOTES), "text": ""}, css_class="p-4") as app:
        with Card():
            with CardHeader():
                CardTitle("Notes")
                CardDescription("The button calls the add_note tool on the server")
            with CardContent():
                with Column(gap=3):
                    with Row(gap=2):
                        Input(name="text", placeholder="Note text")
                        Button("Add", on_click=CallTool(
                            "add_note", arguments={"text": text},
                            on_success=[SetState("notes", RESULT), SetState("text", ""),
                                        ShowToast("Saved", variant="success")],
                            on_error=ShowToast(ERROR, variant="error")))
                    with Column(gap=1):
                        with ForEach("notes") as n:
                            Text(n)
    return app


# Helper called only from the UI: hide it from the model (host enforces visibility).
@mcp.tool(app=AppConfig(visibility=["app"]))
def add_note(text: str) -> list[str]:
    """Add a note and return all notes."""
    if not text.strip():
        raise ValueError("Text is required")
    NOTES.append(text.strip())
    return NOTES


if __name__ == "__main__":
    mcp.run()
