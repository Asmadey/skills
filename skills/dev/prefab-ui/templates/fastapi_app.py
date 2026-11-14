"""Prefab UI on top of a plain FastAPI backend (no MCP).

pip install prefab-ui fastapi uvicorn
Run: uvicorn fastapi_app:app --reload     (http://127.0.0.1:8000)

Three kinds of routes: page (HTML), data (JSON, written to state), component (UI tree as JSON, shown in a Slot).
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from prefab_ui.actions import CloseOverlay, Fetch, SetState, ShowToast
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Button, Card, CardContent, CardHeader, CardTitle, Column, Dialog, Form, H2,
    Input, Row, Slot, Text,
)
from prefab_ui.components.control_flow import ForEach
from prefab_ui.rx import RESULT, Rx

app = FastAPI()
ITEMS = [{"id": 1, "name": "Widget", "note": "A small thing"},
         {"id": 2, "name": "Gadget", "note": "A clever thing"}]


@app.get("/api/items")
def list_items(q: str = ""):
    return [i for i in ITEMS if q.lower() in i["name"].lower()] if q else ITEMS


@app.post("/api/items")
def create_item(item: dict):
    if not str(item.get("name", "")).strip():
        raise HTTPException(status_code=400, detail="Name is required")
    ITEMS.append({"id": max(i["id"] for i in ITEMS) + 1, "name": item["name"], "note": ""})
    return {"ok": True}


@app.get("/api/items/{item_id}/detail")
def item_detail(item_id: int):
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    with Card() as detail:                      # component route: return the tree as JSON
        with CardHeader():
            CardTitle(item["name"])
        with CardContent():
            Text(item["note"] or "No note")
    return detail.to_json()


@app.get("/", response_class=HTMLResponse)
def page():
    new_name = Rx("new_name")
    with Column(gap=4) as view:
        H2("Catalog")
        Input(
            name="q", placeholder="Search...",
            on_change=[
                SetState("q", "{{ $event }}"),
                Fetch.get("/api/items", params={"q": "{{ $event }}"}, on_success=SetState("items", RESULT)),
            ],
        )
        with Dialog(title="New item", description="Add an item to the catalog."):
            Button("+ Add", size="sm")
            with Form(on_submit=Fetch.post(
                "/api/items", body={"name": new_name},
                on_success=[
                    ShowToast("Created", variant="success"),
                    SetState("new_name", ""),
                    Fetch.get("/api/items", on_success=SetState("items", RESULT)),
                    CloseOverlay(),
                ],
                on_error=ShowToast("{{ $error }}", variant="error"),
            )):
                with Column(gap=3):
                    Input(name="new_name", placeholder="Name")
                    Button("Create")
        with ForEach("items") as it:
            with Row(gap=2):
                Button(it.name, variant="outline", on_click=Fetch.get(
                    f"/api/items/{it.id}/detail", on_success=SetState("detail", RESULT)))
        with Slot("detail"):
            Text("Select an item to see details")
    return HTMLResponse(PrefabApp(
        title="Catalog", view=view, css_class="p-6 max-w-2xl mx-auto",
        state={"q": "", "items": ITEMS, "detail": None, "new_name": ""},
    ).html())
