"""FastMCPApp: UI + backend tools + app-provided tools the AGENT can call on the open view.

Host support for app-provided tools is limited: the UI renders everywhere, but the agent may not see the tools.
Pattern from the Prefab docs (mcp/overview). Run: python mcp_app_with_backend.py
"""
from uuid import uuid4

from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions import SetState, ShowToast
from prefab_ui.app import AppTool, PrefabApp
from prefab_ui.components import Button, Text
from prefab_ui.rx import ERROR, RESULT, STATE

counters = FastMCPApp("Counters")
counts: dict[str, int] = {}


@counters.tool()
def increment(counter_id: str, amount: int = 1) -> dict[str, int]:
    """Add to this counter and return its new count."""
    counts[counter_id] += amount
    return {"count": counts[counter_id]}


@counters.ui()
def open_counter() -> PrefabApp:
    """Open a new counter."""
    counter_id = uuid4().hex
    counts[counter_id] = 0
    increment_tool = AppTool(
        increment, name="increment", description="Increment this counter",
        input_schema={
            "type": "object",
            "properties": {"counter_id": {"type": "string"}, "amount": {"type": "integer", "default": 1}},
            "required": ["counter_id"], "additionalProperties": False,
        },
        bind={"counter_id": STATE.counter_id},        # app supplies the id; the agent only gives `amount`
        on_success=SetState("count", RESULT.count),
        on_error=ShowToast(ERROR, variant="error"),
        result={"count": STATE.count},
    )
    with PrefabApp(
        state={"counter_id": counter_id, "count": 0},
        app_tools=[AppTool("get_count", result={"count": STATE.count}), increment_tool],
    ) as app:
        Text(STATE.count)
        Button("Increment", on_click=increment_tool.invoke(amount=1))
    return app


mcp = FastMCP("Counter Server", providers=[counters])

if __name__ == "__main__":
    mcp.run()
