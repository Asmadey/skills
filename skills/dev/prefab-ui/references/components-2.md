## Alert

> **Read first.** Condensed from prefab.prefect.io (Apache-2.0, PrefectHQ/prefab) for prefab-ui 0.21.x. Code is copied from the docs and was NOT all re-run. Known drift in 0.21.1: bare `{{ field }}` inside `ForEach` renders empty, so use `with ForEach("rows") as r: Text(r.field)` or `{{ $item.field }}`; charts import from `prefab_ui.components.charts`. See `gotchas.md`.

Purpose: prominent message box (title + description) with semantic color variants.

Import: `from prefab_ui.components import Alert, AlertTitle, AlertDescription`

| Component | Prop | Type / default / allowed |
|---|---|---|
| Alert (container) | variant | `str`, default `"default"`; `"default"`, `"destructive"`, `"success"`, `"warning"`, `"info"` |
| Alert | icon | `str \| None`, default None; Lucide icon name, kebab-case (e.g. `"circle-alert"`, `"circle-check"`) |
| Alert | css_class | `str \| None`, default None; extra Tailwind classes |
| AlertTitle | content | `str`, required, positional OK |
| AlertTitle | css_class | `str \| None` |
| AlertDescription | content | `str`, required, positional OK |
| AlertDescription | css_class | `str \| None` |

Minimal example:
```python
from prefab_ui.components import (
    Alert,
    AlertTitle,
    AlertDescription,
)

with Alert():
    AlertTitle("Heads up!")
    AlertDescription("You can add components to your app using the CLI.")
```

Variants + icons example:
```python
from prefab_ui.components import (
    Alert,
    AlertDescription,
    AlertTitle,
    Column,
)

with Column(gap=4):
    with Alert(icon="circle-alert"):
        AlertTitle("Heads up!")
        AlertDescription(
            "You can add components to your app "
            "using the CLI."
        )

    with Alert(variant="destructive", icon="circle-x"):
        AlertTitle("Error")
        AlertDescription(
            "Your session has expired. Please log "
            "in again."
        )

    with Alert(variant="success", icon="circle-check"):
        AlertTitle("Success")
        AlertDescription(
            "Your changes have been saved "
            "successfully."
        )
```

Without title (description only):
```python
from prefab_ui.components import (
    Alert,
    AlertDescription,
)

with Alert():
    AlertDescription("Your changes have been saved.")
```

Notes:
- Title is optional; description-only is valid.
- Icon auto-aligns with title and description.
- Works inside Card/CardContent or at page top; wrap several Alerts in `Column(gap=4)`.
- Protocol: Alert accepts `id`, `onMount`, `children`, `let`, `variant` (any string allowed in protocol), `icon`, `cssClass`.

---

## Badge

Purpose: small pill-shaped inline label for status, counts, categories.

Import: `from prefab_ui.components import Badge`

| Prop | Type / default / allowed |
|---|---|
| label | `str \| None`, default None; positional OK. When using children, omit label and compose content directly |
| variant | `str`, default `"default"`; `"default"`, `"secondary"`, `"destructive"`, `"outline"`, `"ghost"`, `"success"`, `"warning"`, `"info"` |
| css_class | `str \| None`, default None; Tailwind classes appended to built-in styles |

Minimal example:
```python
from prefab_ui.components import Badge

Badge("Mostly Harmless")
```

Container/children example (icons, loaders):
```python
from prefab_ui.components import Badge, Icon, Loader, Row, Text

with Row(gap=4, css_class="items-center"):
    with Badge(variant="success"):
        Icon("check", size="sm")
        Text("Verified")
    with Badge():
        Loader(size="sm")
        Text("Syncing")
    with Badge(variant="secondary"):
        Loader(variant="dots", size="sm")
        Text("Processing")
```

Variants grid:
```python
from prefab_ui.components import Badge, Grid

with Grid(gap=8, columns=4, css_class="place-items-center"):
    Badge("Default")
    Badge("Secondary", variant="secondary")
    Badge("Destructive", variant="destructive")
    Badge("Outline", variant="outline")
    Badge("Ghost", variant="ghost")
    Badge("Success", variant="success")
    Badge("Warning", variant="warning")
    Badge("Info", variant="info")
```

Notes:
- Badge is a container component (`children`, `let` in protocol); use `with Badge(...)` for richer content.
- Typical use: next to CardTitle inside `Row(gap=2, css_class="items-center")`:
```python
with Row(gap=2, css_class="items-center"):
    CardTitle("Heart of Gold")
    Badge("Online", variant="success")
```

---

## Button

Purpose: interactive button that triggers actions; variants signal intent, sizes control dimensions.

Import: `from prefab_ui.components import Button`

| Prop | Type / default / allowed |
|---|---|
| label | `str`, required; positional or `label=` keyword |
| icon | `str \| None`, None; Lucide kebab-case name (e.g. `"arrow-right"`, `"trash-2"`); renders before label |
| variant | `str`, `"default"`; `"default"`, `"destructive"`, `"outline"`, `"secondary"`, `"ghost"`, `"link"`, `"success"`, `"warning"`, `"info"` |
| size | `str`, `"default"`; `"default"`, `"xs"`, `"sm"`, `"lg"`, `"icon"`, `"icon-xs"`, `"icon-sm"`, `"icon-lg"` |
| button_type | `str \| None`, None; `"submit"` (default in forms), `"button"` (no form submit), `"reset"` (clears form). Protocol key `buttonType` |
| disabled | `bool \| str`, False; accepts template expression like `"{{ not $item.name }}"` |
| on_click | `Action \| list[Action] \| None`, None; list sequences actions; server actions like `CallTool` take own `on_success`/`on_error` for follow-ups. Protocol key `onClick` |
| css_class | `str \| None`, None; Tailwind classes appended to built-ins |

Minimal example:
```python
from prefab_ui.components import Button

Button("Save Changes")
```

Form / button_type example:
```python
from prefab_ui.components import Button, Form
from prefab_ui.actions.mcp import CallTool

with Form(on_submit=CallTool("save")):
    # ... inputs ...
    Button("Cancel", variant="outline", button_type="button")
    Button("Save")  # defaults to submit
```

Icons and icon-only sizes:
```python
from prefab_ui.components import Button, Row

with Row(gap=3, css_class="items-center"):
    Button("Download", icon="download")
    Button("Settings", icon="settings", variant="outline")
    Button("Delete", icon="trash-2", variant="destructive")
```
```python
from prefab_ui.components import Button, Row

with Row(gap=3, css_class="items-center"):
    Button("", icon="plus", size="icon-xs")
    Button("", icon="plus", size="icon-sm")
    Button("", icon="plus", size="icon")
    Button("", icon="plus", size="icon-lg")
```

Disabled + custom styling:
```python
from prefab_ui.components import Button

Button("Unavailable", disabled=True)
```
```python
from prefab_ui.components import (
    Button,
    Column,
)

with Column(gap=3, css_class="items-start w-full"):
    Button("Full Width Emerald", css_class="w-full bg-emerald-500")
    Button("Pill Shape Rose", css_class="rounded-full bg-rose-500")
```

Notes:
- Inside a `Form`, buttons default to `type="submit"`; use `button_type="button"` for cancel/close.
- Use `xs`/`sm` in dense surfaces (toolbars, table rows); `lg` for primary CTA.
- Icon-only buttons: pass `""` label with `icon=` and an `icon-*` size.
- `css_class` conflicts: if your classes target the same CSS property as a built-in (e.g. `rounded-full` vs `rounded-md`), the built-in class is automatically removed so your override wins. Applies to every component.
- `disabled` can be a template string for conditional disabling.

---

## Carousel

Purpose: scrollable container where each direct child is a slide; same component does slideshow (arrows/dots/swipe), auto-advancing reel, and continuous marquee.

Import: `from prefab_ui.components import Carousel` (children e.g. `Div`, `Badge`)

| Prop | Type / default / allowed |
|---|---|
| visible | `float \| None`, 1; whole number = that many full slides; decimal (1.3) = peek (1 full + 30% of next); `None` = natural slide width (default for marquee when omitted) |
| gap | `int`, 16; pixels between slides (ignored in fade mode) |
| height | `int \| None`, None; fixed px height; vertical carousels auto-detect from first slide when omitted |
| direction | `str`, `"left"`; `"left"` (horizontal), `"right"` (horizontal reversed), `"down"` (vertical), `"up"` (vertical reversed). For auto-advance/marquee controls motion direction; manual nav works either way |
| loop | `bool`, True; seamless infinite looping; when False stops at ends and arrows disappear where nothing left to scroll |
| auto_advance | `int`, 0; ms between advances, 0 = off; pauses on hover by default |
| continuous | `bool`, False; marquee mode, constant velocity; children auto-duplicated for seamless loop |
| speed | `int`, 2; continuous speed 1 (gentle) to 10 (fast) |
| effect | `str`, `"slide"`; `"slide"` or `"fade"` |
| dim_inactive | `bool`, False; reduce opacity of non-active slides (best with peek/multiple visible) |
| show_controls | `bool`, True; prev/next arrows |
| controls_position | `str`, `"outside"`; `"overlay"` (on slides), `"outside"` (flanking viewport), `"gutter"` (where dots render) |
| show_dots | `bool`, False; pagination dots |
| pause_on_hover | `bool`, True; pause auto-advance/continuous on hover |
| align | `str`, `"start"`; `"start"`, `"center"`, `"end"`; only visible with peek or multiple slides |
| slides_to_scroll | `int`, 1; slides per nav step |
| drag | `bool`, True; drag/swipe navigation |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Carousel, Div

with Carousel(show_dots=True, css_class="w-full"):
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-emerald-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-violet-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-amber-500 rounded-lg", style={"height": "160px"})
```

Marquee example:
```python
from prefab_ui.components import Carousel, Column, Badge

with Column(gap=4, css_class="w-full"):
    with Carousel(continuous=True, speed=1, show_controls=False, css_class="w-full"):
        Badge("Python", css_class="mx-2")
        Badge("React", css_class="mx-2")
        Badge("TypeScript", css_class="mx-2")
        Badge("Tailwind", css_class="mx-2")
        Badge("Embla", variant="success", css_class="mx-2")
        Badge("Prefab", variant="success", css_class="mx-2")
```

Peek + dim, fade, auto-advance, vertical:
```python
from prefab_ui.components import Carousel, Div

with Carousel(visible=1.3, dim_inactive=True, show_dots=True, align="center", css_class="w-full"):
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-emerald-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-violet-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-amber-500 rounded-lg", style={"height": "160px"})
```
```python
from prefab_ui.components import Carousel, Div

with Carousel(effect="fade", show_dots=True, auto_advance=2000, show_controls=False, css_class="w-full"):
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-emerald-500 rounded-lg", style={"height": "160px"})
    Div(css_class="bg-violet-500 rounded-lg", style={"height": "160px"})
```
```python
from prefab_ui.components import Carousel, Div

with Carousel(visible=3, gap=16, show_dots=True, css_class="w-full"):
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "120px"})
    Div(css_class="bg-emerald-500 rounded-lg", style={"height": "120px"})
    Div(css_class="bg-violet-500 rounded-lg", style={"height": "120px"})
    Div(css_class="bg-amber-500 rounded-lg", style={"height": "120px"})
    Div(css_class="bg-purple-500 rounded-lg", style={"height": "120px"})
    Div(css_class="bg-red-500 rounded-lg", style={"height": "120px"})
```
```python
from prefab_ui.components import Carousel, Column, Div, H3

with Column(gap=6, css_class="w-full"):
    H3("Vertical with controls")
    with Carousel(direction="down", show_dots=True, controls_position="gutter", loop=True, css_class="w-full"):
        Div(css_class="bg-blue-500 rounded-lg", style={"height": "160px"})
        Div(css_class="bg-emerald-500 rounded-lg", style={"height": "160px"})
        Div(css_class="bg-violet-500 rounded-lg", style={"height": "160px"})

    H3("Vertical reel (auto advance)")
    with Carousel(direction="down", auto_advance=2000, show_controls=False, loop=True, css_class="w-full"):
        Div(css_class="bg-blue-500 rounded-lg", style={"height": "160px"})
        Div(css_class="bg-emerald-500 rounded-lg", style={"height": "160px"})
        Div(css_class="bg-violet-500 rounded-lg", style={"height": "160px"})
```
Sized marquee:
```python
from prefab_ui.components import Carousel, Div

with Carousel(continuous=True, speed=3, show_controls=False, visible=4, gap=12, css_class="w-full"):
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "80px"})
    Div(css_class="bg-emerald-500 rounded-lg", style={"height": "80px"})
    Div(css_class="bg-violet-500 rounded-lg", style={"height": "80px"})
    Div(css_class="bg-amber-500 rounded-lg", style={"height": "80px"})
    Div(css_class="bg-purple-500 rounded-lg", style={"height": "80px"})
    Div(css_class="bg-blue-500 rounded-lg", style={"height": "80px"})
```

Notes:
- Each direct child = one slide.
- `align` has no visible effect with `visible=1` (slide fills viewport).
- Fade mode ignores `gap`.
- Marquee: without `visible`, items use natural width; `visible=4` sizes each at 25% of viewport. Marquee uses constant velocity (unlike auto_advance which pauses between slides). Hover pauses unless `pause_on_hover=False`.
- Vertical carousel measures first slide's height for viewport; honors `gap`. `controls_position="gutter"` puts arrows and dots in the same side gutter.
- Protocol keys are camelCase (`autoAdvance`, `dimInactive`, `showControls`, `controlsPosition`, `showDots`, `pauseOnHover`, `slidesToScroll`). Mentions Embla in example badges.

---

## ChoiceCard

Purpose: bordered clickable card (a Field) that wraps a toggle control; clicking anywhere on card toggles the control; highlights border/tint when on.

Import: `from prefab_ui.components import ChoiceCard, FieldContent, FieldTitle, FieldDescription` (plus Switch/Checkbox)

| Component | Prop | Type / default |
|---|---|---|
| ChoiceCard | (inherits all Field props, see Field) | |
| ChoiceCard | invalid | `bool \| str`, False; error state, cascades red text to all children |
| ChoiceCard | disabled | `bool \| str`, False; dims card, non-interactive |
| ChoiceCard | css_class | `str \| None` |
| FieldTitle | content | `str`, required |
| FieldDescription | content | `str`, required |
| FieldContent | (container) | groups FieldTitle and FieldDescription on the left side |

Minimal example:
```python
from prefab_ui.components import (
    ChoiceCard, Column, FieldContent, FieldDescription, FieldTitle, Switch,
)

with Column(gap=4):
    with ChoiceCard():
        with FieldContent():
            FieldTitle("Marketing emails")
            FieldDescription(
                "Receive emails about new products and features."
            )
        Switch()

    with ChoiceCard():
        with FieldContent():
            FieldTitle("Security emails")
            FieldDescription(
                "Receive emails about your account activity."
            )
        Switch(value=True)
```

Checkbox / disabled variants:
```python
from prefab_ui.components import (
    Checkbox, ChoiceCard, Column, FieldContent, FieldDescription, FieldTitle,
)

with Column(gap=4):
    with ChoiceCard():
        with FieldContent():
            FieldTitle("Accept terms")
            FieldDescription(
                "You agree to our Terms of Service and Privacy Policy."
            )
        Checkbox()

    with ChoiceCard():
        with FieldContent():
            FieldTitle("Subscribe to newsletter")
            FieldDescription("Get weekly updates on new features.")
        Checkbox(value=True)
```
```python
from prefab_ui.components import (
    ChoiceCard, Column, FieldContent, FieldDescription, FieldTitle, Switch,
)

with Column(gap=4):
    with ChoiceCard():
        with FieldContent():
            FieldTitle("Enabled option")
            FieldDescription("You can toggle this.")
        Switch(value=True)

    with ChoiceCard(disabled=True):
        with FieldContent():
            FieldTitle("Disabled option")
            FieldDescription("This cannot be changed.")
        Switch(disabled=True)
```

Notes:
- Works with any toggle control (Switch, Checkbox).
- With `ChoiceCard(disabled=True)` the example also sets `Switch(disabled=True)` on the inner control.

---

## Combobox

Purpose: searchable dropdown select; container of `ComboboxOption` children, filters as user types.

Import: `from prefab_ui.components import Combobox, ComboboxOption, ComboboxGroup, ComboboxLabel, ComboboxSeparator`

Combobox props:
| Prop | Type / default |
|---|---|
| placeholder | `str \| None`, None; shown when no value selected |
| search_placeholder | `str \| None`, None; placeholder in the search input inside dropdown |
| name | `str \| None`, None; state key for the selected value |
| disabled | `bool`, False |
| invalid | `bool`, False; red border on trigger |
| side | `'top' \| 'right' \| 'bottom' \| 'left' \| None`, None; where dropdown appears |
| align | `'start' \| 'center' \| 'end' \| None`, None; alignment relative to trigger |
| on_change | `Action \| list[Action] \| None`, None; `$event` is the selected option's `value` string |
| css_class | `str \| None` |

(Protocol also lists `value?: string`.)

ComboboxOption: `label` (`str`, required, positional OK), `value` (`str`, required; stored in state; "Defaults to a kebab-case version of the label"), `disabled` (`bool`, False; stays in list but unselectable).
ComboboxGroup: container; children should be `ComboboxLabel` and `ComboboxOption`.
ComboboxLabel: `label` (`str`, required, positional OK); non-selectable group header.
ComboboxSeparator: no parameters; visual divider between flat options.

Minimal example:
```python
from prefab_ui.components import Combobox, ComboboxOption

with Combobox(placeholder="Search planets...", css_class="w-fit mx-auto"):
    ComboboxOption("Magrathea", value="magrathea")
    ComboboxOption("Betelgeuse V", value="betelgeuse")
    ComboboxOption("Vogsphere", value="vogsphere")
    ComboboxOption("Krikkit", value="krikkit")
    ComboboxOption("Earth", value="earth")
```

Reactive read via `.rx`:
```python
from prefab_ui.components import Column, Combobox, ComboboxOption, Text

with Column(gap=3, css_class="w-fit mx-auto"):
    with Combobox(placeholder="Search planets...") as combo:
        ComboboxOption("Magrathea", value="magrathea")
        ComboboxOption("Betelgeuse V", value="betelgeuse")
        ComboboxOption("Vogsphere", value="vogsphere")
        ComboboxOption("Krikkit", value="krikkit")
    Text(f"Selected: {combo.rx}")
```

Action via on_change:
```python
from prefab_ui.components import Column, Combobox, ComboboxOption, Text
from prefab_ui.actions import SetState

with Column(gap=4, css_class="w-fit mx-auto"):
    with Combobox(
        placeholder="Choose a ship...",
        on_change=SetState(
            "ship_status",
            "Boarding: {{ $event }}",
        ),
    ):
        ComboboxOption("Heart of Gold", value="heart-of-gold")
        ComboboxOption("Bistromath", value="bistromath")
        ComboboxOption("Starship Titanic", value="starship-titanic")
    Text(
        "{{ ship_status | default:'No ship selected' }}",
        css_class="text-muted-foreground",
    )
```

Groups, separator, disabled option, invalid:
```python
from prefab_ui.components import (
    Combobox,
    ComboboxGroup,
    ComboboxLabel,
    ComboboxOption,
)

with Combobox(
    placeholder="Choose a destination...",
    css_class="w-fit mx-auto",
):
    with ComboboxGroup():
        ComboboxLabel("Inner Planets")
        ComboboxOption("Magrathea", value="magrathea")
        ComboboxOption("Vogsphere", value="vogsphere")
        ComboboxOption("Earth", value="earth")
    with ComboboxGroup():
        ComboboxLabel("Outer Reaches")
        ComboboxOption("Betelgeuse V", value="betelgeuse")
        ComboboxOption("Krikkit", value="krikkit")
        ComboboxOption("Lamuella", value="lamuella")
```
```python
from prefab_ui.components import Combobox, ComboboxOption, ComboboxSeparator

with Combobox(placeholder="Pick one...", css_class="w-fit mx-auto"):
    ComboboxOption("Earth", value="earth")
    ComboboxOption("Mars", value="mars")
    ComboboxSeparator()
    ComboboxOption("Jupiter", value="jupiter")
    ComboboxOption("Saturn", value="saturn")
```
```python
from prefab_ui.components import Combobox, ComboboxOption

with Combobox(placeholder="Select a planet...", css_class="w-fit mx-auto"):
    ComboboxOption("Magrathea", value="magrathea")
    ComboboxOption("Earth", value="earth", disabled=True)
    ComboboxOption("Betelgeuse", value="betelgeuse")
    ComboboxOption("Vogsphere", value="vogsphere")
```
```python
from prefab_ui.components import Column, Combobox, ComboboxOption, Label, Text

with Column(gap=2, css_class="w-fit mx-auto"):
    Label("Home planet")
    with Combobox(placeholder="Select a planet...", invalid=True):
        ComboboxOption("Magrathea", value="magrathea")
        ComboboxOption("Betelgeuse V", value="betelgeuse")
        ComboboxOption("Vogsphere", value="vogsphere")
    Text(
        "Please select your home planet",
        css_class="text-sm text-destructive",
    )
```
Side/align, search placeholder:
```python
from prefab_ui.components import Combobox, ComboboxOption

with Combobox(
    placeholder="Choose a ship...",
    side="top",
    align="end",
    css_class="w-fit mx-auto",
):
    ComboboxOption("Heart of Gold", value="heart-of-gold")
    ComboboxOption("Bistromath", value="bistromath")
    ComboboxOption("Starship Titanic", value="starship-titanic")
```
```python
from prefab_ui.components import Combobox, ComboboxOption

with Combobox(
    placeholder="Choose a ship...",
    search_placeholder="Filter by name...",
    css_class="w-fit mx-auto",
):
    ComboboxOption("Heart of Gold", value="heart-of-gold")
    ComboboxOption("Bistromath", value="bistromath")
    ComboboxOption("Starship Titanic", value="starship-titanic")
    ComboboxOption("Vogon Constructor Fleet", value="vogon-fleet")
```

Notes:
- Use `with Combobox(...) as combo:` then `combo.rx` (reactive ref to selected `value` string) in f-strings/other components. For simple "show current selection" `.rx` is better than `on_change`; use `on_change`+`$event` when transforming the value before storing.
- Disabled combobox: trigger grayed, dropdown won't open. Disabled options still appear but can't be chosen.
- `invalid=True` only styles the trigger; add `Label` and error `Text` yourself for a full form field.
- Groups are auto-separated by dividers; `ComboboxSeparator` is lightweight alternative for flat options.
- `ComboboxOption` value is stored in state.

---

## Define / Use

Purpose: define a reusable component template once (`Define`) and reference it by name (`Use`) with scoped data; template body lives outside the tree and is passed through `UIResponse(defs=[...])`.

Imports: `from prefab_ui.define import Define`, `from prefab_ui.use import Use`, `from prefab_ui.response import UIResponse`

| Component | Prop | Type |
|---|---|---|
| Define | name | `str`, required, positional OK; template name referenced by Use |
| Use | name | `str`, required, positional OK; must match a Define name |
| Use | \*\*kwargs | `Any`; scoped interpolation values. Any kwarg that is not `css_class` becomes a scoped state override for the template |
| Use | css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.define import Define
from prefab_ui.use import Use
from prefab_ui.response import UIResponse
from prefab_ui.components import Card, CardHeader, CardTitle, CardDescription, Column

with Define("user-card") as user_card:
    with Card():
        with CardHeader():
            CardTitle("{{ name }}")
            CardDescription("{{ role }}")

with Column(gap=3) as view:
    Use("user-card", name="Alice", role="Engineer")
    Use("user-card", name="Bob", role="Designer")
    Use("user-card", name="Carol", role="PM")

UIResponse(view=view, defs=[user_card])
```

With ForEach:
```python
from prefab_ui.define import Define
from prefab_ui.use import Use
from prefab_ui.response import UIResponse
from prefab_ui.components import (
    Card, CardHeader, CardTitle, CardDescription,
    Column, ForEach, Heading,
)

with Define("project-card") as project_card:
    with Card():
        with CardHeader():
            CardTitle("{{ name }}")
            CardDescription("{{ description }}")

with Column(gap=4) as view:
    Heading("Featured")
    Use("project-card", name="Prefab", description="The generative UI framework")

    Heading("All Projects")
    with ForEach("projects"):
        Use("project-card")

UIResponse(
    view=view,
    defs=[project_card],
    data={"projects": [
        {"name": "Alpha", "description": "First project"},
        {"name": "Beta", "description": "Second project"},
    ]},
)
```

Other snippets from page:
```python
with Define("status-row") as status_row:
    with Row(gap=2, css_class="items-center"):
        CardTitle("{{ label }}")
        Badge("{{ status }}", variant="{{ variant }}")
```
```python
UIResponse(view=layout, defs=[status_row])
```
```python
# Bare reference (data comes from surrounding scope)
Use("status-row")

# With scoped data
Use("status-row", label="Build", status="passing", variant="default")
```

Notes:
- `Define` uses context manager like a container but does NOT attach to a parent; it lives outside the tree and must be passed via `UIResponse(..., defs=[...])`.
- Multiple children in a Define are auto-wrapped in a Column.
- Template placeholders use `{{ name }}` interpolation; Use kwargs are scoped to that instance.
- Inside `ForEach`, each item's fields automatically become the interpolation context, so bare `Use("project-card")` works.
- Protocol: Define serializes to `{"defs": {"user-card": {...}}}`; bare Use -> `{"$ref": "user-card"}`; with overrides -> `{"$ref": "user-card", "let": {"name": "Alice", "role": "Engineer"}}`.

---

## Dashboard (Dashboard / DashboardItem)

Purpose: grid layout with explicit item placement at exact 1-indexed grid coordinates (col, row, spans); like pinning widgets to a canvas.

Import: `from prefab_ui.components import Dashboard, DashboardItem`

When to use: `Grid` auto-flows children and wraps rows (wrap children in `GridItem` to span; use for most layouts incl. dashboard-style with different-size items). `Dashboard` is for pinned coordinates (e.g. drag-and-drop layout builder).

Dashboard props:
| Prop | Type / default |
|---|---|
| columns | `int`, 12 |
| row_height | `int \| str`, 120; int = pixels; string = any CSS value (e.g. `"auto"`, `"minmax(100px, auto)"`) |
| rows | `int \| None`, None; fixed number of rows -> uses `grid-template-rows` instead of `grid-auto-rows`; omit for auto-expanding rows |
| gap | `int \| tuple \| Responsive \| None`, None; int maps to `gap-{n}`; tuple `(x, y)` sets per-axis gaps |
| css_class | `str \| Responsive \| None`, None |

DashboardItem props:
| Prop | Type / default |
|---|---|
| col | `int`, 1; starting column (1-indexed) |
| row | `int`, 1; starting row (1-indexed) |
| col_span | `int`, 1 |
| row_span | `int`, 1 |
| z_index | `int \| None`, None; CSS z-index for overlapping items |
| css_class | `str \| Responsive \| None`, None |

Minimal example:
```python
from prefab_ui.components import Dashboard, DashboardItem, Div, Text

with Dashboard(columns=4, row_height=80, gap=4):
    # A: starts at column 1, row 1, spans 2 columns
    with DashboardItem(col=1, row=1, col_span=2):
        with Div(css_class="bg-blue-500 rounded-md h-full flex items-center justify-center"):
            Text("A", css_class="text-white font-semibold")
    # B: starts at column 3, row 1, spans 2 columns
    with DashboardItem(col=3, row=1, col_span=2):
        with Div(css_class="bg-emerald-500 rounded-md h-full flex items-center justify-center"):
            Text("B", css_class="text-white font-semibold")
    # C: single cell at column 1, row 2
    with DashboardItem(col=1, row=2):
        with Div(css_class="bg-amber-500 rounded-md h-full flex items-center justify-center"):
            Text("C", css_class="text-white font-semibold")
    # D: starts at column 2, row 2, spans the remaining 3 columns
    with DashboardItem(col=2, row=2, col_span=3):
        with Div(css_class="bg-purple-500 rounded-md h-full flex items-center justify-center"):
            Text("D", css_class="text-white font-semibold")
```

Realistic 12-column layout (chart + stat cards + full-width table):
```python
from prefab_ui.components import (
    Card, CardContent, CardHeader, CardTitle,
    Dashboard, DashboardItem,
    Div, H2, Muted,
)

with Dashboard(columns=12, row_height=100, gap=4):
    # Chart: columns 1-8, rows 1-3 (spans all three stat card rows)
    with DashboardItem(col=1, row=1, col_span=8, row_span=3):
        with Card(css_class="h-full"):
            with CardHeader():
                CardTitle("Revenue Over Time")
            with CardContent():
                Div(css_class="h-full bg-gradient-to-r from-blue-100 to-blue-50 rounded-md")

    # Stat cards: column 9-12, one per row
    with DashboardItem(col=9, row=1, col_span=4):
        with Card(css_class="h-full"):
            with CardHeader(css_class="pb-2"):
                Muted("Total Revenue")
            with CardContent():
                H2("$45,231")

    with DashboardItem(col=9, row=2, col_span=4):
        with Card(css_class="h-full"):
            with CardHeader(css_class="pb-2"):
                Muted("Active Users")
            with CardContent():
                H2("2,350")

    with DashboardItem(col=9, row=3, col_span=4):
        with Card(css_class="h-full"):
            with CardHeader(css_class="pb-2"):
                Muted("Conversion Rate")
            with CardContent():
                H2("3.2%")

    # Full-width table: all 12 columns, rows 4-5
    with DashboardItem(col=1, row=4, col_span=12, row_span=2):
        with Card(css_class="h-full"):
            with CardHeader():
                CardTitle("Recent Transactions")
            with CardContent():
                Div(css_class="h-full bg-gradient-to-r from-gray-100 to-gray-50 rounded-md")
```

Content-sized rows and layering:
```python
from prefab_ui.components import (
    Card, CardContent,
    Dashboard, DashboardItem,
    Div, P, Text,
)

with Dashboard(columns=3, row_height="auto", gap=3):
    # Row 1 — the card's paragraph makes this row tall
    with DashboardItem(col=1, row=1, col_span=2):
        with Card(css_class="h-full"):
            with CardContent():
                P("This card has a paragraph of content, so the first row "
                  "expands to fit. The green cell to the right stretches "
                  "to match, even though its own content is short.")
    with DashboardItem(col=3, row=1):
        with Div(css_class="bg-emerald-500 rounded-md h-full flex items-center justify-center"):
            Text("Stretches", css_class="text-white font-semibold")

    # Row 2 — short content, so this row is smaller
    with DashboardItem(col=1, row=2, col_span=3):
        with Div(css_class="bg-purple-500 rounded-md h-full p-3 flex items-center"):
            Text("Row 2 has less content, so it's shorter.", css_class="text-white")
```
```python
from prefab_ui.components import (
    Card, CardContent,
    Dashboard, DashboardItem,
    Div, Text,
)

with Dashboard(columns=6, row_height=80, gap=2):
    # This panel covers columns 1-4
    with DashboardItem(col=1, row=1, col_span=4, row_span=2):
        with Div(css_class="bg-blue-500 rounded-md h-full flex items-center justify-center"):
            Text("Background panel", css_class="text-white font-semibold")
    # This card covers columns 3-6, overlapping columns 3-4
    with DashboardItem(col=3, row=1, col_span=4, row_span=2, z_index=1):
        with Card(css_class="h-full border-2 border-amber-500"):
            with CardContent(css_class="flex items-center justify-center h-full"):
                Text("Overlay (z_index=1)", css_class="font-semibold")
```

Notes:
- Coordinates are 1-indexed (CSS Grid convention).
- To make children fill their cells use `css_class="h-full"` on the content inside each DashboardItem.
- Row height is uniform; `row_span=2` = twice `row_height` plus one gap.
- `row_height="auto"` sizes each row to tallest item; `"minmax(80px, auto)"` sets a min height while allowing growth.
- Overlapping items stack; later items render on top by default; `z_index` (higher on top) overrides.
- Protocol keys: `rowHeight`, `colSpan`, `rowSpan`, `zIndex`, `cssClass`.

---

## Dot

Purpose: small colored indicator dot for status, categories, legends (lighter than Badge).

Import: `from prefab_ui.components import Dot`

| Prop | Type / default / allowed |
|---|---|
| variant | `str`, `"default"`; `"default"`, `"secondary"`, `"success"`, `"warning"`, `"destructive"`, `"info"`, `"muted"` (protocol also allows arbitrary string) |
| size | `str`, `"default"`; `"sm"`, `"default"`, `"lg"` |
| shape | `str`, `"circle"`; `"circle"`, `"square"`, `"rounded"` |
| css_class | `str \| None`, None; use a `bg-*` class to override the variant color |

Minimal example:
```python
from prefab_ui.components import Dot

Dot(variant="success")
```

Most common pattern (Dot + Text in Row):
```python
from prefab_ui.components import Card, CardContent, Column, Dot, Row, Text

with Card():
    with CardContent():
        with Column(gap=3):
            with Row(gap=2, css_class="items-center"):
                Dot(variant="success")
                Text("Heart of Gold — Operational")
            with Row(gap=2, css_class="items-center"):
                Dot(variant="warning")
                Text("Bistromath — Maintenance")
            with Row(gap=2, css_class="items-center"):
                Dot(variant="destructive")
                Text("Starship Titanic — Crashed")
            with Row(gap=2, css_class="items-center"):
                Dot(variant="muted")
                Text("Krikkit One — Decommissioned")
```

Custom colors (chart legends):
```python
from prefab_ui.components import Dot, Row, Text

with Row(gap=6, css_class="items-center"):
    with Row(gap=2, css_class="items-center"):
        Dot(css_class="bg-[var(--chart-1)]")
        Text("Sector ZZ9")
    with Row(gap=2, css_class="items-center"):
        Dot(css_class="bg-[var(--chart-2)]")
        Text("Sector ZZ Alpha")
    with Row(gap=2, css_class="items-center"):
        Dot(css_class="bg-[var(--chart-3)]")
        Text("Western Spiral Arm")
```

Shape and size:
```python
from prefab_ui.components import Dot, Row, Text

with Row(gap=6, css_class="items-center"):
    with Row(gap=2, css_class="items-center"):
        Dot(variant="info")
        Text("Circle")
    with Row(gap=2, css_class="items-center"):
        Dot(variant="info", shape="square")
        Text("Square")
    with Row(gap=2, css_class="items-center"):
        Dot(variant="info", shape="rounded")
        Text("Rounded")
```
```python
from prefab_ui.components import Dot, Row, Text

with Row(gap=6, css_class="items-center"):
    with Row(gap=2, css_class="items-center"):
        Dot(variant="success", size="sm")
        Text("Small")
    with Row(gap=2, css_class="items-center"):
        Dot(variant="success")
        Text("Default")
    with Row(gap=2, css_class="items-center"):
        Dot(variant="success", size="lg")
        Text("Large")
```

Notes:
- Semantic variants share the palette used by Badge and other status-aware components.
- Not a container (no children); Dot has no label, always pair with `Text` in a `Row(gap=2, css_class="items-center")`. Works in table cells, card content, legends.
- Chart palette CSS variables `var(--chart-1)`, `--chart-2`, `--chart-3` usable via `css_class="bg-[var(--chart-N)]"`.

---

## Field

Purpose: composable form-field wrapper (label + control + error) whose main job is validation styling; `invalid` turns all text inside red.

Import: `from prefab_ui.components import Field, FieldError, Label, Input, Checkbox, Rx` (Rx imported from components in the page example)

| Component | Prop | Type / default |
|---|---|---|
| Field | invalid | `bool \| str`, False; accepts reactive expression like `Rx("!email")` |
| Field | disabled | `bool \| str`, False; dimmed and non-interactive; accepts reactive expressions |
| Field | css_class | `str \| None` |
| FieldError | content | `str`, required; always destructive (red) styling |

(Related: FieldContent, FieldTitle, FieldDescription — see ChoiceCard. ChoiceCard is a Field subclass.)

Minimal example:
```python
from prefab_ui.components import Column, Field, Input, Label

with Column(gap=4):
    with Field():
        Label("Username")
        Input(name="username", placeholder="Choose a username")

    with Field():
        Label("Email")
        Input(name="email", placeholder="you@example.com")
```

Reactive validation example:
```python
from prefab_ui.components import Checkbox, Field, FieldError, Label, Rx

with Field(invalid=Rx("!agree")):
    Label("Terms and conditions")
    Checkbox(name="agree", label="I accept the terms of service")
    FieldError("You must accept the terms to continue.")
```

Notes:
- Field is a vertical container.
- `data-invalid` attribute on Field cascades via CSS to all text descendants (label, description, error) automatically.
- `FieldError` is hidden by default and only appears when its parent Field is invalid; no conditional wrapper needed.
- `ChoiceCard` is a Field subclass rendering bordered clickable card (settings-page toggles).

---

## Grid

Purpose: CSS grid container; equal columns (1-12), custom widths via list, auto-fill via min width, or responsive breakpoints. Children fill cells left-to-right and wrap.

Import: `from prefab_ui.components import Grid, GridItem`

Grid props:
| Prop | Type / default |
|---|---|
| columns | `int \| list \| dict \| Responsive`, 3; count (1-12) or list of widths; positional OK. In list: ints = fractional units (`1` -> `1fr`), strings pass through (`"auto"`, `"200px"`). dict/`Responsive()` for breakpoints. Mutually exclusive with `min_column_width` |
| min_column_width | `str \| None`, None; e.g. `"16rem"`; auto-fill as many columns as fit. Mutually exclusive with `columns` |
| gap | `int \| tuple \| Responsive \| None`, None; int -> `gap-{n}`; tuple `(x, y)` per-axis, `None` skips an axis; `Responsive()` for breakpoints |
| align | `str \| None`, None; `"start"`, `"center"`, `"end"`, `"stretch"`, `"baseline"` |
| justify | `str \| None`, None; `"start"`, `"center"`, `"end"`, `"between"`, `"around"`, `"evenly"`, `"stretch"` |
| css_class | `str \| Responsive \| None`, None |

GridItem props: `col_span` (`int`, 1), `row_span` (`int`, 1), `css_class` (`str | Responsive | None`).
Protocol also lists `columnTemplate?: string`.

Minimal example:
```python
from prefab_ui.components import (
    Div,
    Grid,
)

with Grid(columns=3, gap=4):
    for _ in range(6):
        Div(css_class="bg-emerald-500 rounded-md h-10")
```

Custom widths / spanning:
```python
from prefab_ui.components import Column, Grid, H3, P

with Grid(columns=[1, 3], gap=6, css_class="p-3 border-3 border-dashed"):
    with Column(css_class="p-3 border-3 border-dashed"):
        H3("Sidebar")
        P("Navigation or filters.")
    with Column(css_class="p-3 border-3 border-dashed"):
        H3("Main Content")
        P("The sidebar gets 1/4 of the space; main content gets 3/4.")
```
```python
from prefab_ui.components import Column, Grid, H3, P, Separator

with Grid(columns=[1, "auto", 1], gap=6, css_class="p-3 border-3 border-dashed"):
    with Column(css_class="p-3 border-3 border-dashed"):
        H3("Panel A")
        P("Left side content.")
    Separator(orientation="vertical")
    with Column(css_class="p-3 border-3 border-dashed"):
        H3("Panel B")
        P("Right side content.")
```
```python
from prefab_ui.components import Div, Grid, GridItem

with Grid(columns=4, gap=4):
    with GridItem(col_span=2):
        Div(css_class="bg-blue-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
    with GridItem(col_span=3):
        Div(css_class="bg-purple-500 rounded-md h-10")
```
```python
from prefab_ui.components import Div, Grid, GridItem, Text

with Grid(columns=3, gap=4):
    with GridItem(row_span=2):
        Div(css_class="bg-blue-500 rounded-md h-full min-h-24 flex items-center justify-center",
            children=[Text("Tall", css_class="text-white font-semibold")])
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-amber-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-amber-500 rounded-md h-10")
```
Auto-fill and responsive:
```python
from prefab_ui.components import Div, Grid

with Grid(min_column_width="10rem", gap=4):
    for _ in range(6):
        Div(css_class="bg-emerald-500 rounded-md h-10")
```
```python
Grid(columns={"default": 1, "md": 2, "lg": 3})
```

Notes:
- Children without a `GridItem` wrapper take a single cell. Grid still auto-flows, so items reflow responsively.
- Responsive dict: `default` key is the base; Tailwind breakpoints `sm`, `md`, `lg`, `xl`, `2xl` override progressively. See docs "Responsive Layout Props" (styling/css) for responsive `gap`, `css_class`, and the `Responsive` helper.
- TIP: for explicit row/column placement (pinned coordinates) use `Dashboard`; GridItem controls size, DashboardItem controls size and position.
- `"auto"` column sizes to content (good for Separator between fluid areas).
- Protocol: `Div` can be given `children=[...]` kwarg as in the Tall example.

---

## Icon

Purpose: render any lucide icon by kebab-case name (resolved at render time).

Import: `from prefab_ui.components import Icon`

| Prop | Type / default |
|---|---|
| name | `str`, required; Lucide kebab-case (e.g. `"arrow-right"`, `"circle-alert"`); positional OK; browse lucide.dev/icons |
| size | `str`, `"default"`; `"sm"`, `"default"`, `"lg"` |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Icon

Icon("rocket")
```

In context:
```python
from prefab_ui.components import (
    Column,
    Icon,
    Row,
    Text,
)

with Column(gap=3):
    with Row(gap=2, css_class="items-center"):
        Icon("check", size="sm")
        Text("Task completed")
    with Row(gap=2, css_class="items-center"):
        Icon("clock", size="sm")
        Text("Waiting for approval")
    with Row(gap=2, css_class="items-center"):
        Icon("circle-x", size="sm")
        Text("Build failed")
```

Notes: Icons work inline with text; sizes demo: `Icon("heart", size="sm")`, `Icon("heart", size="default")`, `Icon("heart", size="lg")`. Other components (Button, Alert) take `icon="name"` string props instead.

---

## Kbd

Purpose: inline keyboard-key indicator for shortcuts/hotkeys; one Kbd can show a single key or a full combination.

Import: `from prefab_ui.components import Kbd`

| Prop | Type / default |
|---|---|
| label | `str`, default `""`; key label (e.g. `"⌘"`, `"K"`, `"→"`, `"Shift"`); positional |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Kbd, Row

with Row(gap=2, align="center"):
    Kbd("K")
    Kbd("⌘ + K")
    Kbd("Ctrl + Shift + P")
```

Shortcut list:
```python
from prefab_ui.components import Column, Kbd, Row, Text

with Column(gap=3):
    with Row(gap=4, css_class="justify-between items-center"):
        Text("Save")
        Kbd("⌘ + S")
    with Row(gap=4, css_class="justify-between items-center"):
        Text("Search")
        Kbd("⌘ + K")
    with Row(gap=4, css_class="justify-between items-center"):
        Text("Undo")
        Kbd("⌘ + Z")
```

Notes:
- Label can contain the full combination (e.g. `"⌘ + K"`).
- Common key glyphs shown on page: ⌘ ⇧ ⌥ ⌃ ↵ ⌫ ⇥ Esc ← → ↑ ↓.
- Note `Row(gap=2, align="center")` used here (Row has `align` prop).
- Protocol marks `label` as required (Python default is "").

---

## Loader

Purpose: animated activity indicator for loading/processing states.

Import: `from prefab_ui.components import Loader`

| Prop | Type / default / allowed |
|---|---|
| variant | `str`, `"spin"`; `"spin"`, `"dots"` (bouncing, typing/processing), `"pulse"` (subtle background/heartbeat), `"bars"` (equalizer-style), `"ios"` (segmented chasing circle) |
| size | `str`, `"default"`; `"sm"`, `"default"`, `"lg"` (all variants) |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Loader

Loader()
```

With text:
```python
from prefab_ui.components import Row, Loader, Text

with Row(gap=2, css_class="items-center"):
    Loader(size="sm")
    Text("Fetching results...")
```
```python
from prefab_ui.components import Row, Loader, Text

with Row(gap=2, css_class="items-center"):
    Text("Agent is thinking")
    Loader(variant="dots", size="sm")
```
Inside Badge (Badge accepts children):
```python
from prefab_ui.components import Row, Badge, Loader, Text

with Row(gap=4, css_class="items-center"):
    with Badge():
        Loader(size="sm")
        Text("Syncing")
    with Badge(variant="secondary"):
        Loader(variant="dots", size="sm")
        Text("Processing")
    with Badge(variant="outline"):
        Loader(variant="pulse", size="sm")
        Text("Connected")
```

Notes: no children; default variant is `spin` (the plain `Loader()`); pair with `Text` in a `Row(gap=2, css_class="items-center")`.

---

## Metric

Purpose: KPI headline number with label, optional description and auto-colored trend delta.

Import: `from prefab_ui.components import Metric`

| Prop | Type / default |
|---|---|
| label | `str`, required; metric name above value |
| value | `str \| int \| float`, required; strings displayed as-is (pre-format currency/commas/units) |
| description | `str \| None`, None; context below value (time range, source, percentile) |
| delta | `str \| int \| float \| None`, None; e.g. `"+23.4%"`, `"-15"`, `"+$2.3M"`; arrow icon and sentiment color auto-inferred from sign |
| trend | `str \| None`, None; `"up"`, `"down"`, `"neutral"`; inferred from delta sign when omitted |
| trend_sentiment | `str \| None`, None; `"positive"` (green), `"negative"` (red), `"neutral"` (muted); inferred from trend (up=positive, down=negative) when omitted. Override for inverted metrics |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Metric

Metric(
    label="Response Time",
    value="142ms",
    description="p95 over the last 24 hours",
)
```

Reactive value from state with pipes-style formatting:
```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import STATE as state, Metric

with PrefabApp(state={"revenue": 42_000_000}) as app:
    Metric(label="Revenue", value=f"${(state.revenue / 1_000_000).round()}M")
```

Inverted sentiment (up is bad):
```python
from prefab_ui.components import Card, CardContent, Metric, Row

with Row(gap=6):
    with Card():
        with CardContent(css_class="p-6"):
            Metric(label="Revenue", value="$1.2M", delta="+12%")
    with Card():
        with CardContent(css_class="p-6"):
            Metric(
                label="Response Time",
                value="284ms",
                delta="+18ms",
                trend="up",
                trend_sentiment="negative",
            )
```

KPI row with Grid:
```python
from prefab_ui.components import Card, CardContent, Grid, Metric

with Grid(min_column_width="14rem", gap=4):
    with Card():
        with CardContent(css_class="p-6"):
            Metric(
                label="Revenue",
                value="$42M",
                description="Year to date",
                delta="+12%",
            )

    with Card():
        with CardContent(css_class="p-6"):
            Metric(
                label="Conversion",
                value="3.2%",
                description="Last 30 days",
                delta="+0.4%",
            )

    with Card():
        with CardContent(css_class="p-6"):
            Metric(
                label="Avg. Order",
                value="$128",
                description="Per transaction",
                delta="-$3",
                trend="down",
                trend_sentiment="negative",
            )
```

With Sparklines (sparkline flush at card bottom):
```python
from prefab_ui.components import Card, CardContent, Grid
from prefab_ui.components.charts import Sparkline
from prefab_ui.components import Metric

with Grid(min_column_width="14rem", gap=4):
    with Card(css_class="pb-0 gap-0"):
        with CardContent():
            Metric(label="Revenue", value="$1.52M", delta="+12%")
        Sparkline(
            data=[120, 132, 101, 134, 90, 230, 210, 182, 191, 234, 290, 330],
            variant="success", fill=True, css_class="h-16",
        )
    with Card(css_class="pb-0 gap-0"):
        with CardContent():
            Metric(
                label="Response Time", value="284ms",
                delta="+18ms", trend="up", trend_sentiment="negative",
            )
        Sparkline(
            data=[180, 200, 220, 205, 240, 260, 250, 275, 290, 284],
            variant="destructive", fill=True, css_class="h-16",
        )
    with Card(css_class="pb-0 gap-0"):
        with CardContent():
            Metric(label="Active Users", value="26,104", delta="+4.3%")
        Sparkline(
            data=[22, 23, 21, 24, 23, 25, 24, 26, 25, 26],
            variant="info", fill=True, css_class="h-16",
        )
```

Metrics row + chart (dashboard layout), also shows decreasing cost = positive:
```python
from prefab_ui.components import Card, CardContent, CardHeader, CardTitle, Column, Grid, Metric
from prefab_ui.components.charts import BarChart, ChartSeries

data = [
    {"month": "Jan", "revenue": 186000},
    {"month": "Feb", "revenue": 305000},
    {"month": "Mar", "revenue": 237000},
    {"month": "Apr", "revenue": 273000},
    {"month": "May", "revenue": 209000},
    {"month": "Jun", "revenue": 314000},
]

with Column(gap=4):
    with Grid(min_column_width="14rem", gap=4):
        with Card():
            with CardContent(css_class="p-6"):
                Metric(
                    label="Revenue",
                    value="$1.52M",
                    description="Q2 2025 total",
                    delta="+12%",
                )
        with Card():
            with CardContent(css_class="p-6"):
                Metric(
                    label="Active Users",
                    value="26,104",
                    description="Monthly active",
                    delta="+4.3%",
                )
        with Card():
            with CardContent(css_class="p-6"):
                Metric(
                    label="Infra Costs",
                    value="$48K",
                    description="vs. last month",
                    delta="-15%",
                    trend="down",
                    trend_sentiment="positive",
                )
    with Card():
        with CardHeader():
            CardTitle("Monthly Revenue")
        with CardContent():
            BarChart(
                data=data,
                series=[ChartSeries(data_key="revenue", label="Revenue")],
                x_axis="month",
                height=280,
            )
```

Notes:
- Auto-inference assumes "up is good"; for response time/error rate/cost, set `trend_sentiment` explicitly (arrow still follows direction, color reflects good/bad).
- Typical wrapper: `Card` > `CardContent(css_class="p-6")` > `Metric`; use `Grid(min_column_width="14rem", gap=4)` so cards reflow.
- Sparkline: place as sibling of CardContent inside the Card; use `css_class="pb-0 gap-0"` on the Card so the sparkline bleeds flush to the bottom edge. Sparkline import here is `from prefab_ui.components.charts import Sparkline`.
- Value from state can use reactive expressions + pipes for display-time formatting (see docs concepts/expressions); `STATE as state` import used.

---

## Popover

Purpose: floating content panel opened by clicking a trigger; stays open until click outside (use for forms, settings, menus, lightweight confirmations). Unlike Tooltip/HoverCard (hover).

Import: `from prefab_ui.components import Popover`

Structure: FIRST child = trigger; ALL remaining children = panel content.

| Prop | Type / default |
|---|---|
| title | `str \| None`, None; optional header title of panel |
| description | `str \| None`, None; optional text below title |
| side | `str \| None`, None; preferred side: `"top"`, `"right"`, `"bottom"`, `"left"` |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import (
    Button,
    Column,
    Input,
    Label,
    Popover,
)

with Popover(title="Babel Fish Settings", description="Configure your universal translator."):
    Button("Open popover", variant="outline")
    with Column(gap=3):
        Label("Source Language")
        Input(placeholder="Vogon")
        Label("Target Language")
        Input(placeholder="Galactic Standard")
```

Inline confirmation with actions:
```python
from prefab_ui.components import Button, Column, Popover, Text
from prefab_ui.actions import CloseOverlay
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import Rx

item_id = Rx("item_id")

with Popover():
    Button("Archive", variant="outline")
    with Column(gap=2):
        Text("Archive this item?")
        Button(
            "Confirm",
            on_click=[
                CallTool("archive_item", arguments={"id": item_id}),
                CloseOverlay(),
            ],
        )
```

Without header / side:
```python
from prefab_ui.components import (
    Button,
    Column,
    Label,
    Popover,
    Slider,
)

with Popover():
    Button("Settings", variant="outline")
    with Column(gap=3):
        Label("Improbability Factor")
        Slider(min=0, max=100, value=42, name="improbability")
```
```python
from prefab_ui.components import Button, Popover, Text

with Popover(title="Guide Entry", side="right"):
    Button("Click for info", variant="outline")
    Text("A towel is about the most massively useful thing an interstellar hitchhiker can have.")
```

Notes:
- Skip `title`/`description` to render content directly in the panel.
- `side` is a preference; renderer auto-adjusts if it would overflow viewport. Long panels scroll within available space (up to 18rem) while the title stays visible.
- Use `CloseOverlay()` (from `prefab_ui.actions`) in an `on_click` list to dismiss the popover after an action. Popover is the lighter alternative to a full modal for confirmations.

---

## RadialChart

Purpose: shows each categorical data item as a concentric ring with length proportional to value (like PieChart: `data_key` for values, `name_key` for labels).

Import: `from prefab_ui.components.charts import RadialChart`

| Prop | Type / default |
|---|---|
| data | `list[dict] \| str`, required; list of dicts or a `{{ field }}` interpolation reference |
| data_key | `str`, required; numeric field plotted as ring length |
| name_key | `str`, required; label field for each ring |
| height | `int`, 300; pixels |
| inner_radius | `int`, 30; pixels; increase to push rings outward ("tight rings") |
| start_angle | `int`, 180; degrees |
| end_angle | `int`, 0; degrees |
| show_legend | `bool`, False; legend below chart |
| show_tooltip | `bool`, True |
| value_format | `str`, `"auto"`; tooltip value formatting via expression pipe such as `currency`, `currency:EUR`, `percent:1`, `compact:0` |
| css_class | `str \| None`, None |

(Protocol additionally lists `animate?: true`; not documented in the Python table.)

Minimal example:
```python
from prefab_ui.components.charts import RadialChart

data = [
    {"browser": "Chrome", "visitors": 275},
    {"browser": "Safari", "visitors": 200},
    {"browser": "Firefox", "visitors": 187},
    {"browser": "Edge", "visitors": 173},
    {"browser": "Other", "visitors": 90},
]

RadialChart(
    data=data,
    data_key="visitors",
    name_key="browser",
    show_legend=True,
)
```

Tooltip formatting (distinct feature):
```python
from prefab_ui.components.charts import RadialChart

data = [
    {"service": "Compute", "cost": 186_000},
    {"service": "Storage", "cost": 92_000},
    {"service": "Network", "cost": 48_000},
    {"service": "Support", "cost": 24_000},
]

RadialChart(
    data=data,
    data_key="cost",
    name_key="service",
    value_format="compact:0",
    show_legend=True,
)
```

Semicircle and tight rings:
```python
RadialChart(
    data=data,
    data_key="visitors",
    name_key="browser",
    start_angle=90,
    end_angle=-270,
    show_legend=True,
)
```
```python
RadialChart(
    data=[
        {"browser": "Chrome", "visitors": 275},
        {"browser": "Safari", "visitors": 200},
        {"browser": "Firefox", "visitors": 187},
        {"browser": "Edge", "visitors": 173},
        {"browser": "Other", "visitors": 90},
    ],
    inner_radius=80,
    data_key="visitors",
    name_key="browser",
    show_legend=True,
)
```

Notes:
- `start_angle=90, end_angle=-270` produces a semicircle opening to the right (partial arc).
- `value_format` uses the same pipe strings as Prefab expressions and data table columns.

---

## Row

Purpose: horizontal flex container (children side by side).

Import: `from prefab_ui.components import Row`

| Prop | Type / default |
|---|---|
| gap | `int \| tuple \| Responsive \| None`, None; int -> `gap-{n}`; tuple `(x, y)` per-axis, `None` skips an axis; `Responsive()` for breakpoint gaps |
| align | `str \| None`, None; cross-axis (vertical): `"start"`, `"center"`, `"end"`, `"stretch"`, `"baseline"` |
| justify | `str \| None`, None; main-axis (horizontal): `"start"`, `"center"`, `"end"`, `"between"`, `"around"`, `"evenly"`, `"stretch"` |
| css_class | `str \| Responsive \| None`, None; a `Responsive()` compiles breakpoint-prefixed classes |

Minimal example:
```python
from prefab_ui.components import (
    Div,
    Row,
)

with Row(gap=4):
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
```

Alignment / justification (distinct features):
```python
from prefab_ui.components import Row, Span

with Row(gap=4, align="baseline", css_class="p-3 border-3 border-dashed"):
    Span(
        "Small",
        css_class="bg-emerald-500 rounded-md "
        "px-3 py-1 text-white text-sm",
    )
    Span(
        "Large",
        css_class="bg-emerald-500 rounded-md "
        "px-3 py-2 text-white text-2xl",
    )
    Span(
        "Medium",
        css_class="bg-emerald-500 rounded-md "
        "px-3 py-1 text-white text-base",
    )
```
```python
from prefab_ui.components import Div, Row

with Row(gap=1, justify="between", css_class="w-full p-3 border-3 border-dashed"):
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
```
```python
from prefab_ui.components import Div, Row

with Row(gap=4, align="end", css_class="p-3 border-3 border-dashed"):
    Div(css_class="bg-emerald-500 rounded-md h-8 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-16 w-20")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-20")
```

Notes:
- `align` is vertical alignment of children; difference visible when children have different heights. `baseline` aligns along text baseline (unlike `center` which centers boxes) so text of different sizes reads naturally.
- `justify` distributes along horizontal axis; give the Row `w-full` (via css_class) to see distribution (all justify examples use `css_class="w-full p-3 border-3 border-dashed"`).
- Gap protocol shows `gap-N` class in cssClass; the common idiom elsewhere is `Row(gap=2, css_class="items-center")`.
- Page demos gap=4/8/12, align start/center/end/baseline, justify start/center/end/between/around/evenly.

---

## Separator

Purpose: visual divider between content sections.

Import: `from prefab_ui.components import Separator`

| Prop | Type / default |
|---|---|
| orientation | `str`, `"horizontal"`; `"horizontal"`, `"vertical"` |
| spacing | `int \| None`, None; Tailwind spacing scale; adds vertical margin (`my-N`) for horizontal separators and horizontal margin (`mx-N`) for vertical |
| css_class | `str \| None`, None; useful for height/width |

Minimal example:
```python
from prefab_ui.components import (
    Column,
    P,
    Separator,
)

with Column():
    P("Content above the separator")
    Separator(spacing=4)
    P("Content below the separator")
```

Vertical orientation:
```python
from prefab_ui.components import (
    Row,
    Separator,
    Span,
)

with Row(gap=4, css_class="items-center"):
    Span("Left")
    Separator(orientation="vertical", css_class="h-4")
    Span("Middle")
    Separator(orientation="vertical", css_class="h-4")
    Span("Right")
```

In card content:
```python
from prefab_ui.components import (
    Card,
    CardContent,
    P,
    Separator,
)

with Card():
    with CardContent():
        P("First section")
        Separator(spacing=4)
        P("Second section")
        Separator(spacing=4)
        P("Third section")
```

Notes:
- GOTCHA: a vertical separator has no intrinsic height and stays invisible until you give it one (e.g. `css_class="h-4"`) and it sits in a `Row` (use `items-center`).
- Also used in Grid with `columns=[1, "auto", 1]` as `Separator(orientation="vertical")` between two Columns.

---

## Sparkline

Purpose: compact inline trend chart (no axes, labels, or tooltips); flat list of numbers, Y axis auto-scales.

Import: `from prefab_ui.components.charts import Sparkline`

| Prop | Type / default |
|---|---|
| data | `list[int \| float] \| str`, required; flat numeric list or `{{ field }}` interpolation reference |
| height | `int`, 24; pixels |
| variant | `str`, `"default"`; `"default"`, `"success"`, `"warning"`, `"destructive"`, `"info"`, `"muted"` (same six as Progress, Slider, Ring) |
| indicator_class | `str \| None`, None; Tailwind classes for line/fill; use `stroke-*` classes for color overrides (line is an SVG stroke) |
| fill | `bool`, False; gradient area fill under line (inherits variant color, fades to transparent) |
| curve | `Literal["linear", "step"]`, `"linear"`; interpolation between points |
| stroke_width | `float`, 1.5; pixels |
| mode | `Literal["line", "bar"]`, `"line"`; `"line"` polyline, `"bar"` vertical bars |
| css_class | `str \| None`, None; outer container; use `w-*` for width |

Minimal example:
```python
from prefab_ui.components.charts import Sparkline

Sparkline(data=[10, 15, 8, 22, 18, 25, 20, 16, 24, 12], css_class="w-48")
```

In a Table (distinct feature; components inside cells):
```python
from prefab_ui.components import (
    Table, TableHeader, TableBody, TableRow,
    TableHead, TableCell, Text,
)
from prefab_ui.components.charts import Sparkline

with Table():
    with TableHeader():
        with TableRow():
            TableHead("Metric")
            TableHead("Trend")
            TableHead("Current")
    with TableBody():
        with TableRow():
            TableCell("Revenue")
            with TableCell():
                Sparkline(
                    data=[45, 52, 49, 60, 55, 72, 68, 75],
                    variant="success", fill=True, curve="smooth",
                    css_class="w-24",
                )
            TableCell("$75K")
        with TableRow():
            TableCell("Churn")
            with TableCell():
                Sparkline(
                    data=[12, 15, 18, 14, 20, 22, 19, 25],
                    variant="destructive", curve="smooth",
                    css_class="w-24",
                )
            TableCell("2.5%")
        with TableRow():
            TableCell("Users")
            with TableCell():
                Sparkline(
                    data=[200, 220, 215, 240, 260, 255, 270, 290],
                    variant="info", fill=True, curve="smooth",
                    css_class="w-24",
                )
            TableCell("290")
```

Size/stroke, fill, step, custom colors:
```python
from prefab_ui.components import Row, Text, Column
from prefab_ui.components.charts import Sparkline

data = [10, 15, 8, 22, 18, 25, 20, 16, 24, 12]

with Column(gap=3, css_class="w-fit mx-auto"):
    with Row(css_class="items-center gap-3"):
        Sparkline(data=data, height=16, stroke_width=1, css_class="w-16")
        Text("compact")
    with Row(css_class="items-center gap-3"):
        Sparkline(data=data, height=24, css_class="w-24")
        Text("default")
    with Row(css_class="items-center gap-3"):
        Sparkline(data=data, height=40, stroke_width=2.5, css_class="w-32")
        Text("large")
```
```python
from prefab_ui.components import Row
from prefab_ui.components.charts import Sparkline

data = [10, 15, 8, 22, 18, 25, 20, 16, 24, 12]

with Row(css_class="gap-6"):
    Sparkline(data=data, indicator_class="stroke-blue-500", css_class="w-24")
    Sparkline(data=data, indicator_class="stroke-emerald-500", css_class="w-24")
    Sparkline(data=data, indicator_class="stroke-orange-500", css_class="w-24")
```
```python
Sparkline(data=data, curve="step", css_class="w-24")
```
```python
Sparkline(data=data, fill=True, variant="success", css_class="w-24")
```

Notes:
- INCONSISTENCY on the page: the Python API table says `curve` is `Literal["linear", "step"]`, and the protocol reference says `"linear | smooth | step"`; the In-a-Table example uses `curve="smooth"`.
- Use `Table` (not `DataTable`) when putting sparklines in table cells, since sparklines are components, not plain values.
- Set width with `css_class="w-*"` and height with `height=`.
- Metric cards: put a Sparkline as sibling of CardContent inside `Card(css_class="pb-0 gap-0")` (see Metric).
- Protocol key names: `indicatorClass`, `strokeWidth`.

---

## Table

Purpose: structured data display with HTML table semantics, composed from sub-components (no data prop; built with nested `with` blocks). For data-driven tables, the page references `DataTable` as a separate component.

Import: `from prefab_ui.components import Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption`

Structure: `Table` > `TableHeader` (> `TableRow` > `TableHead`...) and `TableBody` (> `TableRow` > `TableCell`...); optional `TableCaption`.

| Component | Prop | Type / default |
|---|---|---|
| Table | css_class | `str \| None`, None |
| TableHead / TableCell | content | `str \| None`; positional OK; or use child components for rich content |
| TableHead / TableCell | css_class | `str \| None`, None (e.g. `"text-right"` for right-aligned columns) |
| TableCaption | content | `str`, required, positional OK |

(TableHeader, TableBody, TableRow are plain containers; no props documented.)

Minimal example:
```python
from prefab_ui.components import (
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
    TableCaption,
)

with Table():
    TableCaption("Recent invoices")
    with TableHeader():
        with TableRow():
            TableHead("Invoice")
            TableHead("Status")
            TableHead("Method")
            TableHead("Amount", css_class="text-right")
    with TableBody():
        with TableRow():
            TableCell("INV-001", css_class="font-medium")
            TableCell("Paid")
            TableCell("Credit Card")
            TableCell("$250.00", css_class="text-right")
        with TableRow():
            TableCell("INV-002", css_class="font-medium")
            TableCell("Pending")
            TableCell("PayPal")
            TableCell("$150.00", css_class="text-right")
        with TableRow():
            TableCell("INV-003", css_class="font-medium")
            TableCell("Paid")
            TableCell("Bank Transfer")
            TableCell("$350.00", css_class="text-right")
```

Rich cell content:
```python
from prefab_ui.components import (
    Badge,
    Table,
    TableBody,
    TableHead,
    TableHeader,
    TableRow,
    TableCell,
)

with Table():
    with TableHeader():
        with TableRow():
            TableHead("Name")
            TableHead("Status")
            TableHead("Role")
    with TableBody():
        with TableRow():
            TableCell("Alice Johnson")
            with TableCell():
                Badge("Active", variant="success")
            TableCell("Admin")
        with TableRow():
            TableCell("Bob Smith")
            with TableCell():
                Badge("Inactive", variant="secondary")
            TableCell("Viewer")
```

Notes:
- Table cells are containers: `with TableCell():` can hold any component (Badge, Button, Sparkline).
- Use `css_class="text-right"` on both TableHead and TableCell for numeric columns.
- Protocol: TableHead and TableCell share the `TableCell` schema (`content?`, `children?`).

---

## Tooltip

Purpose: hover text on any wrapped component. Wrap a single element. For richer hover content use HoverCard; for interactive click-to-open content use Popover.

Import: `from prefab_ui.components import Tooltip`

| Prop | Type / default |
|---|---|
| content | `str`, required; positional OK |
| side | `str \| None`, None; `"top"`, `"right"`, `"bottom"`, `"left"` |
| delay | `int \| None`, None; ms before showing; defaults to 700ms; `0` = instant |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components import Button, Row, Tooltip

with Row(gap=4):
    with Tooltip("Save your current work"):
        Button("Save")
    with Tooltip("Discard unsaved changes", side="bottom"):
        Button("Reset", variant="outline")
```

Instant tooltips:
```python
from prefab_ui.components import Badge, Row, Tooltip

with Row(gap=4):
    with Tooltip("Deployed 2h ago", delay=0):
        Badge("In Orbit")
    with Tooltip("64% — ETA 12 min", delay=0):
        Badge("Deploying", variant="secondary")
    with Tooltip("Position 3 of 8", delay=0):
        Badge("Queued", variant="outline")
```

Notes: the text is the positional `content` arg of Tooltip; the child inside the `with` block is the trigger. Default delay 700ms; use `delay=0` for dashboards/status displays where users scan quickly.

---

## WaterfallChart

Purpose: floating bars where each starts where the previous ended; shows how sequential gains/losses roll up to a total (profit bridge, cash flow). Auto colors for increase/decrease/total; dashed bridge lines connect bars.

Import: `from prefab_ui.components.charts import WaterfallChart`

| Prop | Type / default |
|---|---|
| data | `list[dict] \| str`, required; list of dicts or `{{ field }}` interpolation reference |
| data_key | `str`, required; value field; positive increases running total, negative decreases |
| name_key | `str`, required; bar label field |
| total_key | `str \| None`, None; bool field marking a row as total; total bars draw from zero and reset the running total for subsequent rows |
| height | `int`, 300 |
| increase_color | `str \| None`, None; CSS color; defaults to theme success color |
| decrease_color | `str \| None`, None; defaults to theme destructive color |
| total_color | `str \| None`, None; defaults to theme info color |
| bar_radius | `int`, 4; px |
| show_connectors | `bool`, True; dashed bridge lines |
| show_legend | `bool`, True; legend of increase/decrease/total categories present in data |
| show_tooltip | `bool`, True |
| animate | `bool`, True; animate data changes. Reactive data defaults to `False`; set `animate=True` explicitly to opt in |
| show_grid | `bool`, True; horizontal grid lines |
| show_y_axis | `bool`, True |
| value_format | `str`, `"auto"`; formats value-axis ticks and tooltip values via pipe e.g. `currency`, `currency:EUR`, `percent:1`, `compact:0` |
| css_class | `str \| None`, None |

Minimal example:
```python
from prefab_ui.components.charts import WaterfallChart

data = [
    {"label": "Revenue", "value": 42000},
    {"label": "COGS", "value": -18000},
    {"label": "Marketing", "value": -6500},
    {"label": "R&D", "value": -8200},
    {"label": "Other Income", "value": 3100},
]

WaterfallChart(
    data=data,
    data_key="value",
    name_key="label",
)
```

Totals + value formatting:
```python
from prefab_ui.components.charts import WaterfallChart

data = [
    {"label": "Starting Cash", "value": 50000, "total": True},
    {"label": "Sales", "value": 32000},
    {"label": "Payroll", "value": -21000},
    {"label": "Marketing", "value": -6500},
    {"label": "Ending Cash", "value": 54500, "total": True},
]

WaterfallChart(
    data=data,
    data_key="value",
    name_key="label",
    total_key="total",
    value_format="currency:0",
)
```

Custom colors / hide connectors:
```python
WaterfallChart(
    data=data,
    data_key="value",
    name_key="label",
    total_key="total",
    increase_color="#0ea5e9",
    decrease_color="#f97316",
    total_color="#64748b",
)
```
```python
WaterfallChart(
    data=data,
    data_key="value",
    name_key="label",
    total_key="total",
    show_connectors=False,
)
```

Notes:
- Like PieChart and RadialChart, does NOT use `ChartSeries` (single series): `data_key` + `name_key` instead.
- A total row's own value is drawn from zero (not added); e.g. "Ending Cash" 54500 is a total, not a delta.
- Colors accept any CSS color or theme variable.
- Full set of format pipe strings is documented on the Charts page ("Formatting values").
- Protocol keys: `dataKey`, `nameKey`, `totalKey`, `increaseColor`, `decreaseColor`, `totalColor`, `barRadius`, `showConnectors`, `showLegend`, `showTooltip`, `showGrid`, `showYAxis`, `valueFormat`.
