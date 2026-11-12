# Prefab UI digest, group 1

> **Read first.** Condensed from prefab.prefect.io (Apache-2.0, PrefectHQ/prefab) for prefab-ui 0.21.x. Code is copied from the docs and was NOT all re-run. Known drift in 0.21.1: bare `{{ field }}` inside `ForEach` renders empty, so use `with ForEach("rows") as r: Text(r.field)` or `{{ $item.field }}`; charts import from `prefab_ui.components.charts`. See `gotchas.md`.

Conventions seen on these pages: `css_class` (Python) maps to `cssClass` on the wire. Components that bind state take `name` (auto-generated if omitted) and expose `.rx`. Template syntax is `{{ key }}`, with pipes like `| default:x`, `| length`, `| date:long`.

---

## Accordion (+ AccordionItem)

**Purpose:** Collapsible content sections for progressive disclosure.

**Import:** `from prefab_ui.components import Accordion, AccordionItem`

Accordion params:
| prop | type | default | notes |
|---|---|---|---|
| default_open_items | `int \| str \| list[int \| str] \| None` | None | Initially expanded item(s). Int = position index, str = match by title (or by item `value`) |
| multiple | `bool` | False | Allow multiple items open at once |
| collapsible | `bool` | True | Whether the open item can be collapsed |
| css_class | `str \| None` | None | Tailwind classes |

AccordionItem params:
| prop | type | default | notes |
|---|---|---|---|
| title | `str` *required* | - | Trigger label; can be positional |
| value | `str \| None` | None | Unique value identifying the item. Defaults to the title |

Both are context managers (`with`); AccordionItem holds arbitrary children.

**Example (basic):**
```python
from prefab_ui.components import Accordion, AccordionItem, Text

with Accordion():
    with AccordionItem("What is the Answer?"):
        Text(
            "Forty-two. The Answer to the Ultimate "
            "Question of Life, the Universe, and "
            "Everything."
        )
    with AccordionItem("What is the Heart of Gold?"):
        Text(
            "A starship powered by the Infinite "
            "Improbability Drive. It can pass through "
            "every conceivable point in every "
            "conceivable universe almost simultaneously."
        )
    with AccordionItem("What is Deep Thought?"):
        Text(
            "A supercomputer designed to find the "
            "Answer to the Ultimate Question. It took "
            "7.5 million years to compute: 42."
        )
```

**Example (multiple + default open by index):**
```python
from prefab_ui.components import Accordion, AccordionItem, Text

with Accordion(
    multiple=True,
    default_open_items=[0, 1]
):
    with AccordionItem("Who is Arthur Dent?"):
        Text(
            "An ordinary human from Earth, unexpectedly "
            "swept into the cosmos when his planet is "
            "demolished to make way for a hyperspace "
            "bypass."
        )
    with AccordionItem("Who is Ford Prefect?"):
        Text(
            "A researcher for the Hitchhiker's Guide "
            "to the Galaxy, and Arthur's best friend. "
            "He's from a small planet somewhere in the "
            "vicinity of Betelgeuse."
        )
    with AccordionItem("What is the Guide?"):
        Text(
            "A digital reference with the words "
            "'Don't Panic' written in large, friendly "
            "letters on the cover."
        )
```

**Example (stable value reference):**
```python
with Accordion(default_open_items="faq"):
    with AccordionItem("FAQ", value="faq"):
        Text("Frequently asked questions...")
    with AccordionItem("Contact"):
        Text("Get in touch...")
```

**Gotchas:**
- `default_open_items=0` opens the first item; strings match the item title (or `value`). Use an explicit `value` when item order or titles might change.
- Wire format: Accordion emits `defaultValues` (list of titles) in the protocol; the Python-side `default_open_items` index is resolved to the title.
- Without `multiple=True`, only one item is open at a time; `collapsible=True` lets the open one be closed.

---

## Audio

**Purpose:** Play audio files with native HTML5 controls (`<audio>`); supports dynamic URLs via `{{ field }}` interpolation.

**Import:** `from prefab_ui.components import Audio`

| prop | type | default | notes |
|---|---|---|---|
| src | `str` *required* | - | Audio URL; first positional arg |
| controls | `bool` | True | Show playback controls |
| autoplay | `bool` | False | Auto-start. Requires `muted=True` in most browsers |
| loop | `bool` | False | Loop playback |
| muted | `bool` | False | Mute audio |
| css_class | `str \| None` | None | Tailwind classes |

**Example (basic):**
```python
from prefab_ui.components import Audio

Audio(src="https://interactive-examples.mdn.mozilla.net"
      "/media/cc0-audio/t-rex-roar.mp3")
```

**Example (looping background audio):**
```python
from prefab_ui.components import Audio

Audio(
    src="https://example.com/ambient.mp3",
    loop=True,
    controls=False,
    autoplay=True,
    muted=True,
)
```

**Gotchas:**
- Browsers block autoplaying sound until user interaction, so `autoplay` only takes effect when paired with `muted=True`.
- `loop` for continuous playback.

---

## ButtonGroup

**Purpose:** Visually connect related buttons into one unit; borders merge, only outer corners stay rounded.

**Import:** `from prefab_ui.components import Button, ButtonGroup`

| prop | type | default | notes |
|---|---|---|---|
| orientation | `str` | "horizontal" | `"horizontal"` or `"vertical"` |
| css_class | `str \| None` | None | Tailwind classes appended to built-in styles |

Context manager; children are `Button`s.

**Example (basic):**
```python
from prefab_ui.components import Button, ButtonGroup

with ButtonGroup():
    Button("Save")
    Button("Cancel", variant="outline")
```

**Example (pagination / segmented control pattern):**
```python
from prefab_ui.components import Button, ButtonGroup

with ButtonGroup():
    Button("Previous", variant="outline")
    Button("1")
    Button("2", variant="outline")
    Button("3", variant="outline")
    Button("Next", variant="outline")
```

**Example (vertical):**
```python
from prefab_ui.components import Button, ButtonGroup

with ButtonGroup(orientation="vertical"):
    Button("Top")
    Button("Middle", variant="outline")
    Button("Bottom", variant="outline")
```

**Gotchas:** Page suggests pagination controls, view toggles and segmented controls as typical uses. The "active" button is shown by leaving it on default variant while others use `variant="outline"`.

---

## Card (+ CardHeader, CardTitle, CardDescription, CardContent, CardFooter)

**Purpose:** Bordered, shadowed container for grouping related content and actions, composed from sub-components.

**Import:** `from prefab_ui.components import Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter` (examples also import `Button, P, Muted, H3, Grid`).

Params:
| component | prop | type | default | notes |
|---|---|---|---|---|
| Card | css_class | `str \| None` | None | Renders as `div` with border, shadow, rounded corners |
| CardHeader | css_class | `str \| None` | None | Renders as a grid with automatic spacing for title + description |
| CardTitle | content | `str \| None` | None | Title text; positional. Alternatively use child components |
| CardTitle | css_class | `str \| None` | None | |
| CardDescription | content | `str \| None` | None | Description text; positional. Alternatively child components |
| CardDescription | css_class | `str \| None` | None | |
| CardContent | css_class | `str \| None` | None | Provides horizontal padding (`px-4`) for the main body |
| CardFooter | css_class | `str \| None` | None | Renders as a flex row for action buttons |

**Example (basic):**
```python
from prefab_ui.components import (
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter,
    Button,
    P,
)

with Card():
    with CardHeader():
        CardTitle("Create project")
        CardDescription("Deploy your new project in one-click.")
    with CardContent():
        P("Your project will be created with default settings.")
    with CardFooter():
        Button("Cancel", variant="outline")
        Button("Deploy")
```

**Example (simple card without sub-components, css_class padding):**
```python
from prefab_ui.components import (
    Card,
    H3,
    P,
)

with Card(css_class="p-6"):
    H3("Quick Stats")
    P("42 active connections, 3 pending requests.")
```

**Example (card grid / KPI tiles):**
```python
from prefab_ui.components import (
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    Grid,
)

with Grid(columns=3, gap=4):
    for title, desc in [
        ("Revenue", "$12,450"),
        ("Users", "1,234"),
        ("Uptime", "99.9%"),
    ]:
        with Card():
            with CardHeader():
                CardDescription(title)
                CardTitle(desc)
```

**Gotchas:**
- Pattern is header -> content -> footer; every section is optional.
- Simple cards: skip sub-components and add padding via `css_class="p-6"`.
- CardTitle/CardDescription accept either a `content` string or child components.
- Card + Grid is the dashboard pattern.

---

## Checkbox

**Purpose:** Checkbox input for binary/multiple selections; each checkbox binds to its own independent state key.

**Import:** `from prefab_ui.components import Checkbox`

| prop | type | default | notes |
|---|---|---|---|
| label | `str \| None` | None | Label next to the checkbox |
| value | `bool` | False | Initially checked |
| name | `str \| None` | None | State key for checked state; auto-generated if omitted. Use `.rx` to reference |
| disabled | `bool` | False | Non-interactive |
| required | `bool` | False | Required for form submission |
| on_change | `Action \| list[Action] \| None` | None | Runs on toggle. `$event` is `true` when checked, `false` when unchecked |
| css_class | `str \| None` | None | Appended to built-in styles |

**Example (basic):**
```python
from prefab_ui.components import Checkbox

Checkbox(label="Accept terms and conditions")
```

**Example (on_change action with EVENT):**
```python
from prefab_ui.components import Checkbox, Column, Text
from prefab_ui.actions import SetState
from prefab_ui.rx import EVENT, Rx

message = Rx("message")

with Column(gap=4, css_class="w-fit mx-auto"):
    Checkbox(
        label="Accept terms",
        name="accepted",
        on_change=SetState(
            "message",
            EVENT.then("Thank you!", "Please accept to continue"),
        ),
    )
    Text(
        message.default("Check the box"),
        css_class="text-muted-foreground",
    )
```

**Example (reading the value with `.rx`):**
```python
from prefab_ui.components import Checkbox, Input, Label, Row

with Row(gap=4, align="center"):
    cb = Checkbox(label="Enable Infinite Improbability Drive", value=True)
    Label("Drive status:")
    Input(value=cb.rx.then("Engaged", "Disengaged"), read_only=True)
```

**Other snippets on the page:** `Checkbox(label="Subscribe to newsletter", value=True)`; disabled variants `Checkbox(label="Disabled option", disabled=True)`, `Checkbox(label="Disabled & checked", value=True, disabled=True)`; multiple checkboxes inside `Column(gap=3, css_class="w-fit mx-auto")`.

**Gotchas:**
- Multiple checkboxes are independent (unlike a grouped Radio, where selecting one clears the rest).
- `.rx` gives a boolean; `.then(a, b)` turns it into display strings. `EVENT.then(...)` does the same for `$event` inside `on_change`.
- Protocol `value` can be `boolean | string` (string = template expression).
- Disabled still shows its checked/unchecked state.

---

## Column

**Purpose:** Vertical flex container for stacking children top-to-bottom.

**Import:** `from prefab_ui.components import Column`

| prop | type | default | notes |
|---|---|---|---|
| gap | `int \| tuple \| Responsive \| None` | None | int -> `gap-{n}`. Tuple `(x, y)` sets per-axis gaps; `None` skips an axis. `Responsive()` for per-breakpoint gaps |
| align | `str \| None` | None | Cross-axis (horizontal in a Column): `"start"`, `"center"`, `"end"`, `"stretch"`, `"baseline"` |
| justify | `str \| None` | None | Main-axis: `"start"`, `"center"`, `"end"`, `"between"`, `"around"`, `"evenly"`, `"stretch"` |
| css_class | `str \| Responsive \| None` | None | Tailwind classes; `Responsive()` compiles breakpoint-prefixed classes |

**Example (basic):**
```python
from prefab_ui.components import (
    Column,
    Div,
)

with Column(gap=4):
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
    Div(css_class="bg-emerald-500 rounded-md h-10")
```

**Example (alignment):**
```python
from prefab_ui.components import Column, Div

with Column(gap=4, align="start", css_class="p-3 border-3 border-dashed"):
    Div(css_class="bg-emerald-500 rounded-md h-10 w-full")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-3/4")
    Div(css_class="bg-emerald-500 rounded-md h-10 w-1/2")
```

**Gotchas:**
- In a Column, `align` controls horizontal alignment (visible only when children have different widths). Wire format: `gap=4` becomes `gap-4` in cssClass, `align="start"` becomes `items-start`.
- Gap examples shown: 4, 8, 12.

---

## Container

**Purpose:** Responsive centered container with built-in padding and a default max-width.

**Import:** `from prefab_ui.components import Container`

| prop | type | default | notes |
|---|---|---|---|
| css_class | `str \| Responsive \| None` | None | Use `max-w-*` to constrain width beyond the default responsive breakpoints |

**Example (basic):**
```python
from prefab_ui.components import (
    Container,
    H1,
    P,
)

with Container():
    H1("The Hitchhiker's Guide to the Galaxy")
    P(
        "A wholly remarkable book, the standard"
        " repository for all the knowledge and"
        " wisdom in the Galaxy."
    )
```

**Example (narrowing):**
```python
from prefab_ui.components import Container, P

with Container(css_class="max-w-2xl"):
    P(
        "The ships hung in the sky in much the"
        " same way that bricks don't."
    )
```

**Gotchas:** Padding scales with viewport. Override width with a `max-w-*` class (narrow for forms and long-form prose).

---

## DatePicker

**Purpose:** Popover button that opens a calendar for single-date selection; button shows the selected date or placeholder.

**Import:** `from prefab_ui.components import DatePicker`

| prop | type | default | notes |
|---|---|---|---|
| placeholder | `str` | "Pick a date" | Button text when no date is selected |
| name | `str \| None` | None | State key for the selected date (stored as an ISO string) |
| on_change | `Action \| list[Action] \| None` | None | Triggered when the date changes |
| css_class | `str \| None` | None | Tailwind classes |

(Protocol also lists `value?: string`; the Python API table does not list `value`.)

**Example (basic):**
```python
from prefab_ui.components import DatePicker

DatePicker(placeholder="Select deadline", css_class="w-fit mx-auto")
```

**Example (reading value with `.rx` and date formatting):**
```python
from prefab_ui.components import Column, DatePicker, Label, Row, Text

with Row(gap=6, align="center"):
    picker = DatePicker(placeholder="When does the whale arrive?")
    with Column(gap=2, justify="center"):
        Label("Selected date")
        Text(picker.rx.then(picker.rx.date("long"), "None yet"), italic=True)
```

**Gotchas:**
- Value is an ISO date string once picked (e.g. `"2026-04-02"`), but starts as `undefined` when nothing is selected. Use `.rx.then(...)` to handle both states.
- `.rx.date("long")` pipe formats `"2026-04-02"` into `"April 2, 2026"`.
- Value syncs to state automatically; in forms use `.rx` to reference it elsewhere.
- Compiled expression for reference: `{{ datepicker_2 ? (datepicker_2 | date:long) : 'None yet' }}`.

---

## Div & Span

**Purpose:** Unstyled block (Div) and inline (Span) containers; escape hatches when Row/Column/Grid don't fit. Both support `css_class` (Tailwind) and `style` (arbitrary inline CSS).

**Import:** `from prefab_ui.components import Div, Span` (examples also use `P`, `Row`)

Div params:
| prop | type | default | notes |
|---|---|---|---|
| css_class | `str \| None` | None | Tailwind classes; Div has no built-in styling |
| style | `dict[str, str] \| None` | None | Inline CSS for properties Tailwind can't express |

Span params:
| prop | type | default | notes |
|---|---|---|---|
| content | `str` *required* | - | Text content; positional |
| css_class | `str \| None` | None | Span has no built-in styling |
| style | `dict[str, str] \| None` | None | Inline CSS |

Protocol-only extras for Span (from the protocol block): `bold`, `italic`, `underline`, `strikethrough`, `uppercase`, `lowercase`, `code` (default false), `align`.

**Example (Div custom layout):**
```python
from prefab_ui.components import (
    Div,
    P,
)

with Div(css_class="flex items-center gap-3 rounded-lg border p-4"):
    Div(css_class="bg-emerald-500 rounded-md h-8 w-8")
    P("Custom layout with Div")
```

**Example (inline `style` for CSS Tailwind can't express):**
```python
from prefab_ui.components import (
    Div,
    P,
)

with Div(style={
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "border-radius": "12px",
    "padding": "24px",
}):
    P("Styled with inline CSS", css_class="text-white font-medium")
```

**Example (Span):**
```python
from prefab_ui.components import (
    P,
    Row,
    Span,
)

with Row(gap=2, align="baseline"):
    P("Status:")
    Span("Online", css_class="text-sm text-success font-medium")
```

**Gotchas:** Use `style` for vendor prefixes, `clamp()`, `mask-image`, etc. `style` keys use CSS property names (e.g. `"border-radius"`).

---

## Embed

**Purpose:** Embed external content (videos, maps, PDFs) via `url`, or custom HTML/JS (Three.js, Canvas, shaders) via `html`, in an iframe.

**Import:** `from prefab_ui.components import Embed`

| prop | type | default | notes |
|---|---|---|---|
| url | `str \| None` | None | iframe `src`; first positional arg. Mutually exclusive with `html` |
| html | `str \| None` | None | iframe `srcdoc`. Mutually exclusive with `url` |
| width | `str \| None` | None | CSS width with units (`"100%"`, `"640px"`) |
| height | `str \| None` | None | CSS height with units |
| sandbox | `str \| None` | None | iframe sandbox attr; space-separated, e.g. `"allow-scripts allow-same-origin"` |
| allow | `str \| None` | None | iframe allow attr (Permissions Policy), e.g. `"fullscreen; autoplay"` |
| css_class | `str \| None` | None | Tailwind classes |

Classmethod: `Embed.from_iframe(iframe_html_string, **overrides)`; parses `src`, `width`, `height`, `allow`, `sandbox` from a pasted `<iframe>` tag.

**Example (URL, YouTube):**
```python
from prefab_ui.components import Embed

Embed(
    url="https://www.youtube.com/embed/iVdZdLL0CJ4",
    width="100%",
    height="400px",
)
```

**Example (HTML mode, interactive canvas):**
```python
from prefab_ui.components import Embed

Embed(
    html="""\
<style>
  html, body { margin: 0; height: 100%; overflow: hidden;
               background: #1a1a2e; }
  canvas { display: block; width: 100%; height: 100%;
           cursor: crosshair; }
</style>
<canvas id="c"></canvas>
<script>
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
  const particles = [];

  canvas.addEventListener('mousemove', (e) => {
    for (let i = 0; i < 3; i++) {
      particles.push({
        x: e.offsetX, y: e.offsetY,
        vx: (Math.random() - 0.5) * 4,
        vy: (Math.random() - 0.5) * 4,
        life: 1,
        hue: (Date.now() / 10) % 360,
      });
    }
  });

  function draw() {
    ctx.fillStyle = 'rgba(26, 26, 46, 0.15)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx; p.y += p.vy; p.life -= 0.015;
      if (p.life <= 0) { particles.splice(i, 1); continue; }
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.life * 4, 0, Math.PI * 2);
      ctx.fillStyle =
        `hsla(${p.hue}, 80%, 60%, ${p.life})`;
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  draw();
</script>""",
    width="100%",
    height="250px",
)
```

**Example (paste an embed code):**
```python
from prefab_ui.components import Embed

Embed.from_iframe(
    '<iframe src="https://open.spotify.com/embed/track/2CgBqLufSdwMt0FMIu1CVn"'
    ' width="100%" height="352" allow="autoplay; encrypted-media;'
    ' fullscreen; picture-in-picture"></iframe>'
)
```

**Example (sandbox):**
```python
from prefab_ui.components import Embed

# Scripts can run, but no access to parent origin
Embed(url="https://example.com", sandbox="allow-scripts")

# Scripts + forms + same-origin access
Embed(
    url="https://example.com",
    sandbox="allow-scripts allow-same-origin allow-forms",
)
```

**Example (allow):**
```python
from prefab_ui.components import Embed

Embed(
    url="https://www.youtube.com/embed/dQw4w9WgXcQ",
    allow="fullscreen; autoplay",
)
```

**Other examples:** Google Maps (`url=` a long `https://www.google.com/maps/embed?pb=...` with `width="100%", height="400px"`), Spotify (`https://open.spotify.com/embed/track/2CgBqLufSdwMt0FMIu1CVn?utm_source=generator`, `height="152px"`).

**Gotchas:**
- `url` and `html` are mutually exclusive.
- By default NO sandbox is applied (iframe has full capabilities). Set `sandbox` to restrict. `sandbox` restricts capabilities; `allow` grants browser API access; they are independent.
- Common sandbox tokens: `allow-scripts`, `allow-same-origin`, `allow-forms`, `allow-popups`, `allow-modals`.
- `allow` is mostly needed for video embeds (fullscreen) or device APIs (camera, microphone, geolocation).
- `from_iframe()`: bare numeric dimensions (`height="352"`) are converted to CSS (`"352px"`); keyword arguments override the parsed attributes.
- HTML mode runs in an isolated iframe, so `<script>`, Canvas, WebGL, client-side code work. The `html` string should set its own `html, body { margin:0; height:100% }` to fill the frame.
- Width/height need units.

---

## Form (+ Form.from_model)

**Purpose:** Group labeled inputs with a submit action; `Form.from_model()` generates a complete form (labels, typed inputs, validation, submit button) from a Pydantic model.

**Import:** `from prefab_ui.components import Form`; actions: `from prefab_ui.actions.mcp import CallTool`, `from prefab_ui.actions import ShowToast`.

Form params:
| prop | type | default | notes |
|---|---|---|---|
| gap | `int` | 4 | Spacing between children (Tailwind `gap-N`) |
| on_submit | `Action \| list[Action] \| None` | None | Action(s) on submit |
| css_class | `str \| None` | None | Tailwind classes |

`Form.from_model()` params:
| prop | type | default | notes |
|---|---|---|---|
| model | `type[BaseModel]` *required* | - | Pydantic model class |
| fields_only | `bool` | False | Returns field components without Form wrapper or submit button; fields auto-parent to the active context manager. For custom layouts where you provide your own Form, button and CallTool arguments |
| submit_label | `str` | "Submit" | Submit button text; ignored when `fields_only=True` |
| on_submit | `Action \| list[Action] \| None` | None | A `CallTool` with no arguments is auto-filled from model fields under a `data` key |
| defaults | `dict[str, Any] \| None` | None | Runtime values keyed by field name; overrides class-level `Field(default=...)` for this render only. Partial dicts fine. Unknown keys raise `ValueError` |
| css_class | `str \| None` | None | Classes on the form container |

**Example (manual form with named inputs; `{{ name }}` reflects `Input(name="name")`):**
```python
from prefab_ui.components import (
    Button, Card, CardContent, CardDescription, CardFooter,
    CardHeader, CardTitle, Column, Form, Grid, Input, Label,
)
from prefab_ui.actions.mcp import CallTool

submit = CallTool("create_user", arguments={"name": "{{ name }}", "email": "{{ email }}"})

with Grid(columns=2, gap=6):
    with Form(on_submit=submit):
        with Column(gap=2):
            Label("Name")
            Input(name="name", placeholder="Your name")
        with Column(gap=2):
            Label("Email")
            Input(name="email", input_type="email", placeholder="you@example.com")
        Button("Submit")

    with Card():
        with Form(on_submit=submit):
            with CardHeader():
                CardTitle("Create Account")
                CardDescription("Enter your information to get started.")
            with CardContent():
                with Column(gap=4):
                    with Column(gap=2):
                        Label("Name")
                        Input(name="name", placeholder="Your name")
                    with Column(gap=2):
                        Label("Email")
                        Input(name="email", input_type="email", placeholder="you@example.com")
            with CardFooter(css_class="justify-end"):
                Button("Submit")
```

**Example (turnkey `from_model`; note CallTool has no `arguments`):**
```python
from pydantic import BaseModel, Field
from prefab_ui.components import Form
from prefab_ui.actions.mcp import CallTool

class ContactInfo(BaseModel):
    name: str = Field(title="Full Name", min_length=1)
    email: str
    message: str = Field(
        description="Your message",
        json_schema_extra={"ui": {"type": "textarea", "rows": 4}},
    )

Form.from_model(ContactInfo, on_submit=CallTool("submit_contact"))
```
Generated: `arguments` = `{"data": {"name": "{{ name }}", "email": "{{ email }}", "message": "{{ message }}"}}` plus default `onError` toast `ShowToast("{{ $error }}", variant="error")`.

**Example (`fields_only=True` custom layout):**
```python
from pydantic import BaseModel, Field
from prefab_ui.components import (
    Button, Card, CardContent, CardFooter, CardTitle,
    Column, Form,
)
from prefab_ui.actions import ShowToast
from prefab_ui.actions.mcp import CallTool

class ContactInfo(BaseModel):
    name: str = Field(title="Full Name", min_length=1)
    email: str
    message: str = Field(
        description="Your message",
        json_schema_extra={"ui": {"type": "textarea", "rows": 4}},
    )

with Card(css_class="w-full max-w-lg"):
    with Form(on_submit=CallTool(
        "submit_contact",
        arguments={"name": "{{ name }}", "email": "{{ email }}", "message": "{{ message }}"},
        on_success=ShowToast("Message sent!", variant="success"),
        on_error=ShowToast("{{ $error }}", variant="error"),
    )):

        with CardContent():
            CardTitle("Contact Us", css_class="mb-2")
            with Column(gap=4):
                Form.from_model(ContactInfo, fields_only=True)
        with CardFooter(css_class="justify-end gap-2"):
            Button("Cancel", variant="outline", button_type="button")
            Button("Send Message")
```

**Example (type mapping):**
```python
from pydantic import BaseModel, Field, SecretStr
from prefab_ui.components import Form

class UserProfile(BaseModel):
    username: str
    email: str
    age: int = Field(ge=0, le=150)
    password: SecretStr
    active: bool = True

Form.from_model(UserProfile)
```

**Example (field metadata):**
```python
from pydantic import BaseModel, Field
from prefab_ui.components import Form

class Profile(BaseModel):
    name: str = Field(
        title="Your Name",
        description="How should we address you?",
        min_length=2,
        max_length=50,
    )
    bio: str = Field(
        default="",
        description="Tell us about yourself",
        json_schema_extra={"ui": {"type": "textarea", "rows": 3}},
    )

Form.from_model(Profile)
```

**Example (runtime defaults):**
```python
from typing import Literal
from pydantic import BaseModel
from prefab_ui.components import Form
from prefab_ui.actions.mcp import CallTool

class BugReport(BaseModel):
    title: str
    severity: Literal["low", "medium", "high"] = "low"
    reproducible: bool = False

Form.from_model(
    BugReport,
    defaults={
        "title": "Login button unresponsive on Safari",
        "severity": "high",
        "reproducible": True,
    },
    on_submit=CallTool("file_bug"),
)
```

**Example (error handling override):**
```python
from pydantic import BaseModel, Field
from prefab_ui.components import Form
from prefab_ui.actions import ShowToast
from prefab_ui.actions.mcp import CallTool

class Contact(BaseModel):
    name: str = Field(min_length=1)
    email: str

Form.from_model(
    Contact,
    on_submit=CallTool(
        "create_contact",
        on_success=ShowToast("Contact saved!", variant="success"),
        on_error=ShowToast("Could not save: {{ $error }}", variant="error"),
    ),
)
```

**Type mapping table (Python type -> input):**
| Python type | Input component |
|---|---|
| `str` | Text input (auto-detects `email`, `password`, `tel`, `url` from field name) |
| `int`, `float` | Number input |
| `bool` | Checkbox |
| `Literal["a", "b", "c"]` | Select dropdown |
| `SecretStr` | Password input |
| `datetime.date` | Date picker |
| `datetime.time` | Time picker |
| `datetime.datetime` | Datetime picker |

**Field metadata mapping:**
| Field metadata | Form effect |
|---|---|
| `Field(title="...")` | Label text (fallback: humanized field name) |
| `Field(description="...")` | Placeholder text |
| `Field(min_length=..., max_length=...)` | HTML input constraints |
| `Field(ge=..., le=...)` | Number input min/max |
| `Field(json_schema_extra={"ui": {"type": "textarea", "rows": 4}})` | Textarea override |
| `Field(exclude=True)` | Skip field entirely |
| Optional type or default value | Label shows "optional" indicator |

**Gotchas:**
- Named inputs sync to client state automatically; `{{ name }}` always reflects `Input(name="name")`.
- Turnkey `from_model()` with a `CallTool` that has no `arguments` auto-wraps fields as `{{ field_name }}` under a `data` key and adds a default error toast. If `on_error` is given, the default is not added.
- With `fields_only=True` you must: create the `Form` yourself, give `CallTool` explicit `arguments` (not auto-generated), add your own submit button, and wrap fields in `Column(gap=4)` for spacing.
- A button that should not submit needs `button_type="button"` (e.g. Cancel).
- `$error` captures the error message of a failed tool call.
- `defaults`: unknown keys raise `ValueError`; date/time values accept Python `date`/`datetime`/`time` instances or ISO strings.
- Unsupported types skipped by `from_model()`: `list`, `dict`, `set`, `tuple`, nested `BaseModel`; build those parts manually and handle arguments yourself.
- In the `defaults` example's generated output, the `Literal` field becomes a Select with the matching option `selected: true` and the `bool` a Checkbox with `value: true`.
- Protocol `Form` has `gap?: 4`, `onSubmit`.

---

## HoverCard

**Purpose:** Rich content panel on hover. First child = trigger; all remaining children = panel content.

**Import:** `from prefab_ui.components import HoverCard`

| prop | type | default | notes |
|---|---|---|---|
| side | `str \| None` | None | Preferred side: `"top"`, `"right"`, `"bottom"`, `"left"` |
| open_delay | `int \| None` | None | ms before card appears; defaults to Radix default (700ms). `0` = instant |
| close_delay | `int \| None` | None | ms before dismissal after cursor leaves |
| css_class | `str \| None` | None | Tailwind classes |

**Example (basic):**
```python
from prefab_ui.components import Button, Column, HoverCard, Muted, Row, Text

with HoverCard():
    Button("@heart-of-gold", variant="link")
    with Column(gap=2):
        Text("heart-of-gold")
        Muted("Infinite Improbability Drive vessel. Currently in orbit around Magrathea.")
        with Row(gap=4):
            Muted("Status: In Orbit")
            Muted("Deployed 2h ago")
```

**Example (instant hover):**
```python
from prefab_ui.components import Badge, Column, HoverCard, Muted, Text

with HoverCard(open_delay=0, close_delay=200):
    Badge("Healthy")
    with Column(gap=2):
        Text("weather-api")
        Muted("Uptime: 99.97%")
```

**Example (side placement):**
```python
from prefab_ui.components import Badge, HoverCard, Text

with HoverCard(side="right"):
    Badge("Details")
    Text("Panel appears to the right of the trigger.")
```

**Gotchas:**
- For plain-text hover labels use Tooltip (simpler). For interactive content that must stay open (forms, menus) use Popover (click-based, stays open until dismissed).
- Renderer auto-adjusts if the card would overflow the viewport.
- Only the first child is the trigger; all remaining children become panel content (the examples wrap them in a `Column`).

---

## Input

**Purpose:** Single-line text input fields for user data entry.

**Import:** `from prefab_ui.components import Input`

| prop | type | default | notes |
|---|---|---|---|
| input_type | `str` | "text" | `"text"`, `"email"`, `"password"`, `"number"`, `"tel"`, `"url"`, `"search"`, `"date"`, `"time"`, `"datetime-local"`, `"file"` |
| placeholder | `str \| None` | None | Shown when empty |
| value | `str \| None` | None | Initial value |
| name | `str \| None` | None | State key for current value; auto-generated if omitted. Set to bind to a known key, or use `.rx` |
| disabled | `bool` | False | Non-interactive |
| read_only | `bool` | False | Value visible and selectable but not editable |
| required | `bool` | False | Required for form submission |
| css_class | `str \| None` | None | Appended to built-in styles |

Protocol-only extras (wire): `minLength`, `maxLength`, `min`, `max`, `step`, `pattern`, `onChange` (`Action | Action[]`). The Python API table does not list these; Form.from_model generates `minLength`/`maxLength`/`min`/`max`.

**Example (basic):**
```python
from prefab_ui.components import Input

Input(placeholder="Enter your email...")
```

**Example (reading the value with `.rx` in an f-string):**
```python
from prefab_ui.components import Column, Input, Text

with Column(gap=4):
    inp = Input(placeholder="What is your name, traveler?")
    Text(f"Hello, {inp.rx.default('stranger')}!")
```

**Other snippets:**
```python
# types
Input(input_type="email", placeholder="Email")
Input(input_type="password", placeholder="Password")
Input(input_type="number", placeholder="Age")
Input(input_type="tel", placeholder="Phone")

# label pairing
with Column(gap=2):
    Label("Email address")
    Input(input_type="email", placeholder="you@example.com", required=True)

# date/time (native browser pickers)
Input(input_type="date", name="date")
Input(input_type="time", name="time")
Input(input_type="datetime-local", name="datetime")

# disabled / read-only
Input(placeholder="Disabled input", disabled=True)
Input(value="example_value_123", read_only=True)
```

**Gotchas:**
- `read_only` keeps normal appearance (not greyed), text is selectable/copyable; `disabled` greys out.
- Different `input_type` values give appropriate mobile keyboards/validation.
- `.rx` updates on each keystroke; `.rx.default('x')` supplies a fallback when empty.
- `value=` with `read_only=True` accepts a reactive expression (e.g. `cb.rx.then("Engaged", "Disengaged")`).
- Pair with `Label` in a `Column(gap=2)` for accessible forms.

---

## LineChart (+ ChartSeries)

**Purpose:** Connected data points as lines, for trends. Each `ChartSeries` becomes a line. (Page references a shared "Charts" page for the data/series/formatting model.)

**Import:** `from prefab_ui.components.charts import LineChart, ChartSeries`

LineChart params:
| prop | type | default | notes |
|---|---|---|---|
| data | `list[dict] \| str` *required* | - | List of dicts, or `{{ field }}` interpolation reference |
| series | `list[ChartSeries] \| RxStr` *required* | - | Series definitions, or an `Rx` / sole template resolving to a list of series dicts |
| x_axis | `str \| None` | None | Data key for x-axis labels |
| x_axis_label | `RxStr \| None` | None | Category-axis title |
| y_axis_label | `RxStr \| None` | None | Value-axis title; hidden when `show_y_axis=False` |
| height | `int` | 300 | Pixels |
| curve | `Literal["linear", "smooth", "step"]` | "linear" | Interpolation |
| show_dots | `bool` | False | Dot at each point |
| show_legend | `bool` | False | Legend below chart |
| show_tooltip | `bool` | True | Tooltips on hover |
| show_grid | `bool` | True | Horizontal grid lines |
| show_y_axis | `bool` | True | Y-axis with tick labels; False for compact axis-free view |
| value_format | `str` | "auto" | Format ticks/tooltips with expression pipe: `currency`, `currency:EUR`, `percent:1`, `compact:0` |
| css_class | `str \| None` | None | Tailwind classes |

ChartSeries params:
| prop | type | default | notes |
|---|---|---|---|
| data_key | `str` *required* | - | Field to plot; must match a key in the data dicts |
| label | `str \| None` | None | Legend/tooltip label; defaults to `data_key` |
| color | `str \| None` | None | CSS color override; default cycles theme palette `--chart-1` .. `--chart-5` |

(Protocol also lists `animate?: true`.)

**Example (basic):**
```python
from prefab_ui.components.charts import LineChart, ChartSeries

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
    {"month": "Apr", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "Jun", "desktop": 214, "mobile": 140},
]

LineChart(
    data=data,
    series=[
        ChartSeries(data_key="desktop", label="Desktop"),
        ChartSeries(data_key="mobile", label="Mobile"),
    ],
    x_axis="month",
    show_legend=True,
)
```

**Example (reactive series bound to state):**
```python
from prefab_ui.app import PrefabApp
from prefab_ui.components.charts import LineChart
from prefab_ui.rx import Rx

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
]

app = PrefabApp(
    state={
        "chart_series": [
            {
                "dataKey": "desktop",
                "label": "Desktop",
                "color": "var(--chart-1)",
                "visible": True,
            },
            {
                "dataKey": "mobile",
                "label": "Mobile",
                "color": "var(--chart-2)",
                "visible": False,
            },
        ]
    },
    view=LineChart(
        data=data,
        series=Rx("chart_series").selectattr("visible"),
        x_axis="month",
    ),
)
```

**Example (value formatting):**
```python
from prefab_ui.components.charts import ChartSeries, LineChart

data = [
    {"month": "Jan", "conversion": 0.031},
    {"month": "Feb", "conversion": 0.036},
    {"month": "Mar", "conversion": 0.041},
    {"month": "Apr", "conversion": 0.039},
]

LineChart(
    data=data,
    series=[ChartSeries(data_key="conversion", label="Conversion")],
    x_axis="month",
    value_format="percent:1",
    show_legend=True,
)
```

**Example (axis labels):**
```python
from prefab_ui.components.charts import LineChart, ChartSeries

LineChart(
    data=[{"month": "Jan", "users": 10}, {"month": "Feb", "users": 20}],
    series=[ChartSeries(data_key="users")],
    x_axis="month",
    x_axis_label="Month",
    y_axis_label="Users",
)
```

**Variant snippets (use the `data` above):** `show_grid=False` (minimal), `curve="smooth"`, `curve="step"` (discrete jumps), `show_dots=True`.

**Gotchas:**
- Reactive series state dictionaries must use WIRE names (`dataKey`, not `data_key`) and the expression must resolve to a list of dicts. `"{{ chart_series | selectattr:'visible' }}"` as a sole template is equivalent to `Rx("chart_series").selectattr("visible")`.
- Automatic palette colors follow the order of the resolved series list; set `color` on each series to keep stable colors when filtering/reordering.
- `show_y_axis=False` hides the y-axis title too.
- `show_legend` default is False in the Python API table (the protocol block lists `showLegend?: true`; the page's examples pass it explicitly).
- Percent formatting expects fractions (0.031 -> 3.1%).

---

## Mermaid

**Purpose:** Render diagrams from Mermaid text definitions (flowchart, sequence, state, ER, etc.). The library loads lazily on first use (zero cost if unused). Useful for generative UI where LLMs emit diagram definitions directly.

**Import:** `from prefab_ui.components import Mermaid`

| prop | type | default | notes |
|---|---|---|---|
| chart | `str` *required* | - | Mermaid diagram definition; supports all Mermaid diagram types; positional |
| css_class | `str \| None` | None | Tailwind classes |

**Example (flowchart):**
```python
from prefab_ui.components import Mermaid

Mermaid("""
graph TD
    A[New Request] --> B{Authenticated?}
    B -->|Yes| C{Authorized?}
    B -->|No| D[401 Unauthorized]
    C -->|Yes| E[Process Request]
    C -->|No| F[403 Forbidden]
    E --> G{Success?}
    G -->|Yes| H[200 OK]
    G -->|No| I[500 Error]

    style A fill:#818cf8,color:#fff
    style H fill:#34d399,color:#fff
    style D fill:#f472b6,color:#fff
    style F fill:#f472b6,color:#fff
    style I fill:#fb923c,color:#fff
""")
```

**Example (state diagram):**
```python
from prefab_ui.components import Mermaid

Mermaid("""
stateDiagram-v2
    [*] --> Pending
    Pending --> Running: start()
    Running --> Completed: finish()
    Running --> Failed: error()
    Running --> Cancelled: cancel()
    Failed --> Pending: retry()
    Cancelled --> [*]
    Completed --> [*]

    state Running {
        [*] --> Initializing
        Initializing --> Processing
        Processing --> Finalizing
        Finalizing --> [*]
    }
""")
```

**Example (sequence diagram):**
```python
from prefab_ui.components import Mermaid

Mermaid("""
sequenceDiagram
    actor User
    participant App
    participant Auth
    participant API
    participant DB

    User->>App: Click "Sign In"
    App->>Auth: Redirect to OAuth
    Auth-->>User: Show login form
    User->>Auth: Enter credentials
    Auth->>Auth: Validate
    Auth-->>App: Authorization code
    App->>Auth: Exchange for token
    Auth-->>App: Access token
    App->>API: GET /user (token)
    API->>DB: Query user
    DB-->>API: User data
    API-->>App: User profile
    App-->>User: Welcome!
""")
```

**Example (ER diagram):**
```python
from prefab_ui.components import Mermaid

Mermaid("""
erDiagram
    TEAM ||--o{ MEMBER : has
    MEMBER ||--o{ TASK : assigned
    TEAM ||--o{ PROJECT : owns
    PROJECT ||--o{ TASK : contains
    TASK ||--o{ COMMENT : has
    MEMBER ||--o{ COMMENT : writes

    TEAM {
        string name
        string department
    }
    MEMBER {
        string name
        string role
        string email
    }
    PROJECT {
        string name
        date deadline
        string status
    }
""")
```

**Gotchas:** Mermaid syntax notes from the page: flowchart `[...]` steps, `{...}` decisions, `-->|label|` names a path, `style` lines tint nodes; sequence `->>` call and `-->>` response, declare each `actor`/`participant` once; state `[*]` start/end, nested `state X { }` sub-machine; ER `||--o{` = one to zero-or-many.

---

## PieChart

**Purpose:** Show parts of a whole as slices; supports donut (`inner_radius`) and combining small categories into an `Other` slice.

**Import:** `from prefab_ui.components.charts import PieChart`

| prop | type | default | notes |
|---|---|---|---|
| data | `list[dict] \| str` *required* | - | List of dicts or `{{ field }}` reference |
| data_key | `str` *required* | - | Field with numeric values (slice sizes) |
| name_key | `str` *required* | - | Field with slice labels |
| aggregate_below | `float \| None` | None | Combine slices below this fraction of the original total into `Other`; accepts 0 through 1; slices exactly at the cutoff stay separate. Mutually exclusive with `aggregate_except` |
| aggregate_except | `list[str] \| Rx \| None` | None | Keep these `name_key` values as individual slices; combine the rest into `Other`. Literal list or reactive binding. Mutually exclusive with `aggregate_below` |
| height | `int` | 300 | Pixels |
| inner_radius | `int` | 0 | Pixels; >0 makes a donut |
| show_label | `bool` | False | Label on each slice |
| padding_angle | `int` | 0 | Degrees between slices |
| show_legend | `bool` | True | Legend below chart |
| show_tooltip | `bool` | True | Tooltips on hover |
| value_format | `str` | "auto" | Tooltip format pipe: `currency`, `currency:EUR`, `percent:1`, `compact:0` |
| css_class | `str \| None` | None | Tailwind classes |

(Protocol also lists `animate?: true`.)

**Example (basic):**
```python
from prefab_ui.components.charts import PieChart

data = [
    {"browser": "Chrome", "visitors": 275},
    {"browser": "Safari", "visitors": 200},
    {"browser": "Firefox", "visitors": 187},
    {"browser": "Edge", "visitors": 173},
    {"browser": "Other", "visitors": 90},
]

PieChart(
    data=data,
    data_key="visitors",
    name_key="browser",
    show_legend=True,
)
```

**Example (reactive aggregate_except bound to state):**
```python
from prefab_ui import PrefabApp
from prefab_ui.actions import SetState
from prefab_ui.components import Button, Column, Row
from prefab_ui.components.charts import PieChart
from prefab_ui.rx import STATE

with PrefabApp(
    state={
        "sales": [
            {"country": "US", "revenue": 100},
            {"country": "MX", "revenue": 20},
            {"country": "IN", "revenue": 10},
        ],
        "selected_countries": ["US"],
    }
):
    with Column():
        with Row():
            Button(
                "Show MX",
                on_click=SetState("selected_countries", ["US", "MX"]),
            )
            Button("Group MX", on_click=SetState("selected_countries", ["US"]))
        PieChart(
            data=STATE.sales,
            name_key="country",
            data_key="revenue",
            aggregate_except=STATE.selected_countries,
            show_label=True,
        )
```

**Example (automatic cutoff):**
```python
from prefab_ui.components.charts import PieChart

PieChart(
    data=[
        {"country": "US", "revenue": 70},
        {"country": "MX", "revenue": 20},
        {"country": "IN", "revenue": 10},
    ],
    name_key="country",
    data_key="revenue",
    aggregate_below=0.2,
    show_label=True,
)
```

**Example (tooltip formatting):**
```python
from prefab_ui.components.charts import PieChart

data = [
    {"category": "Compute", "share": 0.42},
    {"category": "Storage", "share": 0.24},
    {"category": "Network", "share": 0.18},
    {"category": "Support", "share": 0.16},
]

PieChart(
    data=data,
    data_key="share",
    name_key="category",
    value_format="percent:1",
    show_legend=True,
)
```

**Other snippets (use `data` above):** donut `inner_radius=60`; labels `show_label=True`; spaced slices `inner_radius=60, padding_angle=5`.

**Gotchas:**
- Choose ONE aggregation option per chart (`aggregate_below` and `aggregate_except` are mutually exclusive).
- Aggregation preserves the total. With `aggregate_below=0.2` slices below 20% of the total join `Other`; exactly 20% stays separate.
- Empty `aggregate_except` list combines all rows. `Other` is omitted when no rows are combined.
- Aggregation accepts finite, non-negative numeric values and DISTINCT `data_key` and `name_key` fields.
- An existing category named `Other` joins the combined bucket when one is needed.
- With a zero total, automatic cutoff leaves rows unchanged.
- Percent formatting expects fractional values (0.42 -> 42%).
- `show_legend` defaults to True on PieChart (unlike Line/Radar where default is False).
- In the reactive example the compiled chart has `animate: false` on the wire (page-generated, not a documented Python prop).
- `with PrefabApp(state={...}):` context-manager form is used, with `STATE.<key>` references for data binding.

---

## RadarChart (+ ChartSeries)

**Purpose:** Multivariate comparison on radial axes (spider-web); each `ChartSeries` is a filled polygon.

**Import:** `from prefab_ui.components.charts import RadarChart, ChartSeries`

| prop | type | default | notes |
|---|---|---|---|
| data | `list[dict] \| str` *required* | - | List of dicts or `{{ field }}` reference |
| series | `list[ChartSeries]` *required* | - | Each becomes a filled polygon |
| axis_key | `str \| None` | None | Data key for angular axis labels |
| height | `int` | 300 | Pixels |
| filled | `bool` | True | Fill inside each polygon |
| show_dots | `bool` | False | Dot per data point |
| show_legend | `bool` | False | Legend below chart |
| show_tooltip | `bool` | True | Tooltips on hover |
| show_grid | `bool` | True | Polar grid lines |
| css_class | `str \| None` | None | Tailwind classes |

ChartSeries: `data_key` (`str`, required; must match a key in data dicts), `label` (`str | None`, defaults to `data_key`), `color` (`str | None`, default cycles `--chart-1` through `--chart-5`). (Protocol also lists `animate?: true`.)

**Example (basic):**
```python
from prefab_ui.components.charts import RadarChart, ChartSeries

data = [
    {"subject": "Math", "alice": 120, "bob": 98},
    {"subject": "English", "alice": 98, "bob": 130},
    {"subject": "Science", "alice": 86, "bob": 110},
    {"subject": "History", "alice": 99, "bob": 95},
    {"subject": "Art", "alice": 85, "bob": 90},
]

RadarChart(
    data=data,
    series=[
        ChartSeries(data_key="alice", label="Alice"),
        ChartSeries(data_key="bob", label="Bob"),
    ],
    axis_key="subject",
    show_legend=True,
)
```

**Example (lines only):**
```python
RadarChart(
    data=data,
    series=[
        ChartSeries(data_key="alice", label="Alice"),
        ChartSeries(data_key="bob", label="Bob"),
    ],
    axis_key="subject",
    filled=False,
    show_legend=True,
)
```

**Gotchas:** `show_grid=False` hides the polar grid (compare silhouettes). `filled=False` is easier to read with multiple series. Unlike LineChart, `series` here is documented as `list[ChartSeries]` only (no Rx/reactive series, no `value_format`, no axis labels on this page).

---

## Ring

**Purpose:** Circular progress indicator (arc fills clockwise from 12 o'clock) with centered label; same `value`/`min`/`max`/`variant` API as Progress but more compact.

**Import:** `from prefab_ui.components import Ring`

| prop | type | default | notes |
|---|---|---|---|
| value | `float \| str` | 0 | Current value; can be a template expression |
| min | `float` | 0 | Min; renderer normalizes `(value - min) / (max - min)` to 0-100% |
| max | `float` | 100 | Max |
| label | `str \| None` | None | Center text; supports template expressions; ignored when children are present |
| children | `list[Component]` | [] | Arbitrary components in the center, replacing the label (use `with Ring(...)`) |
| variant | `str` | "default" | `"default"`, `"success"`, `"warning"`, `"destructive"`, `"info"`, `"muted"` |
| size | `str` | "default" | `"sm"` (64px), `"default"` (96px), `"lg"` (128px) |
| thickness | `float` | 6 | Stroke width in px |
| target | `float \| str \| None` | None | Target marker position; renders a tick on the ring |
| indicator_class | `str \| None` | None | Tailwind classes on the filled arc; wrapper is a `group`, so `group-hover:` works |
| target_class | `str \| None` | None | Tailwind classes for the target tick |
| gradient | `bool \| None` | None | `None` inherits theme default, `True` forces gradient, `False` forces solid stroke |
| css_class | `str \| None` | None | Tailwind classes for the outer container |

**Example (basic):**
```python
from prefab_ui.components import Ring

Ring(value=72, label="72%")
```

**Example (custom center content):**
```python
from prefab_ui.components import Column, Ring, Row, Text

with Row(css_class="gap-6"):
    with Ring(value=75, variant="success", size="lg", thickness=8):
        Text("75%", css_class="text-3xl font-bold")
    with Ring(value=3, max=5, variant="info", size="lg", thickness=8):
        with Column(css_class="text-center"):
            Text("3/5", css_class="text-2xl font-bold")
            Text("steps", css_class="text-xs text-muted-foreground")
```

**Other examples:**
```python
# variants
with Row(css_class="gap-4 flex-wrap"):
    Ring(value=60, label="60%")
    Ring(value=100, variant="success", label="100%")
    Ring(value=72, variant="warning", label="72%")
    Ring(value=90, variant="destructive", label="90%")
    Ring(value=45, variant="info", label="45%")
    Ring(value=30, variant="muted", label="30%")

# indicator_class
with Row(css_class="gap-6"):
    Ring(
        value=72, label="72%", variant="info",
        indicator_class=(
            "group-hover:drop-shadow-[0_0_20px_rgba(59,130,246,0.8)]"
        ),
    )
    Ring(
        value=90, label="90%",
        indicator_class=(
            "stroke-emerald-500"
            " group-hover:drop-shadow-[0_0_20px_rgba(16,185,129,0.8)]"
        ),
    )

# target marker
with Row(css_class="gap-6"):
    Ring(value=55, target=75, label="55%")
    Ring(value=90, target=75, variant="success", label="90%")
    Ring(
        value=60, target=80, variant="info",
        label="60%", target_class="stroke-red-500",
    )

# custom range
with Row(css_class="gap-6"):
    Ring(value=72, min=60, max=100, variant="warning", label="72°F")
    Ring(value=3, max=5, variant="info", label="3/5")

# sizes
Ring(value=60, size="sm", label="sm")
# thickness
Ring(value=75, thickness=12, label="12")
```

**Gotchas:**
- The arc is an SVG stroke: use `stroke-*` classes (NOT `bg-*`) in `indicator_class`/`target_class` to override colors.
- When children are present they replace `label`.
- Use `min`/`max` for non-0-100 ranges (the value is normalized automatically).
- Ring wrapper is a Tailwind `group` so `group-hover:` effects (e.g. drop-shadow glow) work on `indicator_class`.
- `value`, `label` and `target` accept template expressions for reactive binding.

---

## Select (+ SelectOption, SelectGroup, SelectLabel, SelectSeparator)

**Purpose:** Dropdown to pick one option; the selected option's `value` string is stored in client state (readable via `.rx`).

**Import:** `from prefab_ui.components import Select, SelectOption, SelectGroup, SelectLabel, SelectSeparator`

Select params:
| prop | type | default | notes |
|---|---|---|---|
| placeholder | `str \| None` | None | Shown when nothing selected |
| name | `str \| None` | None | State key; auto-generated if omitted |
| size | `str` | "default" | `"default"`, `"sm"` |
| side | `str \| None` | None | Dropdown side: `"top"`, `"right"`, `"bottom"`, `"left"` |
| align | `str \| None` | None | `"start"`, `"center"`, `"end"` |
| disabled | `bool` | False | Non-interactive |
| required | `bool` | False | Required for form submission |
| invalid | `bool` | False | Error styling (red border) |
| on_change | `Action \| list[Action] \| None` | None | `$event` is the `value` string of the selected option |
| css_class | `str \| None` | None | Tailwind classes |

SelectOption params:
| prop | type | default | notes |
|---|---|---|---|
| value | `str` *required* | - | Value stored in state |
| label | `str` *required* | - | Display text |
| selected | `bool` | False | Initially selected |
| disabled | `bool` | False | Non-interactive (dimmed) |
| css_class | `str \| None` | None | |

SelectGroup: `css_class`. SelectLabel: `label` (`str`, required) + `css_class`. SelectSeparator: `css_class`. (Protocol Select also lists `value?: string`.)

**Example (basic):**
```python
from prefab_ui.components import Select, SelectOption

with Select(placeholder="Choose size...", css_class="w-fit"):
    SelectOption(value="sm", label="Small")
    SelectOption(value="md", label="Medium")
    SelectOption(value="lg", label="Large")
```

**Example (reading value with `.rx`):**
```python
from prefab_ui.components import Column, Select, SelectOption, Text

with Column(gap=4, css_class="w-fit mx-auto"):
    with Select(placeholder="Choose a planet...") as sel:
        SelectOption(value="magrathea", label="Magrathea")
        SelectOption(value="betelgeuse", label="Betelgeuse V")
        SelectOption(value="vogsphere", label="Vogsphere")
        SelectOption(value="earth", label="Earth (Mostly Harmless)")
    Text(f"You chose: {sel.rx}")
```

**Example (on_change action):**
```python
from prefab_ui.components import Column, Select, SelectOption, Text
from prefab_ui.actions import SetState

with Column(gap=4, css_class="w-fit mx-auto"):
    with Select(
        placeholder="Pick a color...",
        on_change=SetState("picked", "You chose: {{ $event }}"),
    ):
        SelectOption(value="red", label="Red")
        SelectOption(value="green", label="Green")
        SelectOption(value="blue", label="Blue")
    Text(
        "{{ picked | default:'Make a selection' }}",
        css_class="text-muted-foreground",
    )
```

**Example (option groups):**
```python
from prefab_ui.components import (
    Select,
    SelectGroup,
    SelectLabel,
    SelectOption,
    SelectSeparator,
)

with Select(placeholder="Choose a food...", css_class="w-fit"):
    with SelectGroup():
        SelectLabel("Fruits")
        SelectOption(value="apple", label="Apple")
        SelectOption(value="banana", label="Banana")
        SelectOption(value="cherry", label="Cherry")
    SelectSeparator()
    with SelectGroup():
        SelectLabel("Vegetables")
        SelectOption(value="carrot", label="Carrot")
        SelectOption(value="broccoli", label="Broccoli")
        SelectOption(value="spinach", label="Spinach")
```

**Other snippets:**
```python
# preselected
SelectOption(value="uk", label="United Kingdom", selected=True)
# small size
with Select(placeholder="Small size", size="sm"): ...
# label pairing
with Column(gap=2, css_class="w-fit mx-auto"):
    Label("Preferred language")
    with Select(placeholder="Choose language"): ...
# disabled select / options / invalid
with Select(placeholder="Travel class...", disabled=True, css_class="w-fit mx-auto"): ...
SelectOption(value="bistromath", label="Bistromath", disabled=True)
with Select(placeholder="Choose a planet...", invalid=True): ...
```

**Gotchas:**
- Select is a container: add `SelectOption` children inside a `with` block. Every option needs both `value` and `label`.
- `.rx` holds the option `value` (e.g. `"magrathea"`), NOT the display label.
- `on_change` is for transforming the value before storing; for a simple "show current selection" prefer `.rx`.
- Mark `selected=True` on an option to preselect.
- `invalid=True` is just error styling; pair with a `Label` in a form layout.
- Groups: `SelectGroup` + `SelectLabel` for sections, `SelectSeparator` between groups.

---

## Slot

**Purpose:** Placeholder that renders a component tree stored in a state key; fallback children render when the key is empty.

**Import:** `from prefab_ui.components import Slot`

| prop | type | default | notes |
|---|---|---|---|
| name | `str` *required* | - | State key containing the component tree (a JSON object with a `type` field); positional |
| children | `list[Component]` | [] | Fallback content when the state key is empty or missing |
| css_class | `str \| None` | None | Tailwind classes |

**Example (basic):**
```python
from prefab_ui.components import Column, Heading, Slot


with Column(gap=4):
    Heading("Starship Registry", level=3)
    Slot("info")
```

**Example (fallback content, ternary from state):**
```python
from prefab_ui.components import Column, Heading, Slot, Switch, Text
from prefab_ui.actions import SetState


with Column(gap=4):
    Heading("Item Detail", level=3)
    Switch(
        label="Show details",
        name="selected_item",
        on_change=SetState(
            "selected_item",
            "{{ $event ? detail_card : null }}",
        ),
    )
    with Slot("selected_item"):
        Text(
            "Toggle the switch to load details",
            css_class="text-muted-foreground",
        )
```

**Gotchas:**
- Slot renders the key's value when it is a component tree (a JSON object with a `type` field); when the key is empty/missing it shows the fallback children (the example sets it to `null` to return to the fallback).
- Typical pattern: a `CallTool` or `Fetch` action with `SetState("key", RESULT)` in `on_success` writes a component tree into state; the Slot picks it up automatically.
- The layout defines where; state decides what. `detail_card` in the example must exist in state as a component tree (not shown on the page).
- Note the Switch in the example has `name="selected_item"` and starts at `false` (its own boolean state), then `on_change` overwrites that same key with the tree or `null`.

---

## Switch

**Purpose:** Toggle switch for on/off state (alternative to Checkbox).

**Import:** `from prefab_ui.components import Switch`

| prop | type | default | notes |
|---|---|---|---|
| label | `str \| None` | None | Label next to the switch |
| value | `bool` | False | Whether on |
| size | `str` | "default" | `"default"`, `"sm"` |
| name | `str \| None` | None | State key for checked state; auto-generated if omitted; use `.rx` |
| disabled | `bool` | False | Non-interactive |
| required | `bool` | False | Required for form submission |
| on_change | `Action \| list[Action] \| None` | None | `$event` is `true` when on, `false` when off |
| css_class | `str \| None` | None | Appended to built-in styles |

**Example (basic):**
```python
from prefab_ui.components import Switch

Switch(label="Enable notifications")
```

**Example (on_change with EVENT.then):**
```python
from prefab_ui.components import Column, Switch, Text
from prefab_ui.actions import SetState
from prefab_ui.rx import EVENT, Rx

status = Rx("status")

with Column(gap=4, css_class="w-fit mx-auto"):
    Switch(
        label="Enable notifications",
        name="notifications",
        on_change=SetState(
            "status",
            EVENT.then("Notifications enabled", "Notifications disabled"),
        ),
    )
    Text(
        status.default("Toggle the switch"),
        css_class="text-muted-foreground",
    )
```

**Example (reading the value with `.rx`):**
```python
from prefab_ui.components import Input, Label, Row, Switch

with Row(gap=4, align="center"):
    sw = Switch(label="Auto-save to the Guide", value=True)
    Label("Auto-save:")
    Input(value=sw.rx.then("On", "Off"), read_only=True)
```

**Other snippets:** `Switch(label="Dark mode", value=True)`; `Switch(label="Small size", size="sm", value=True)`; disabled `Switch(label="Disabled on", value=True, disabled=True)`.

**Gotchas:** Disabled still displays on/off, signalling a locked setting (plan tier, permission, another toggle). Protocol `value` can be `boolean | string`. Wire form of `EVENT.then(a, b)` is `{{ $event ? 'a' : 'b' }}`.

---

## Textarea

**Purpose:** Multi-line text input for comments, descriptions, longer content.

**Import:** `from prefab_ui.components import Textarea`

| prop | type | default | notes |
|---|---|---|---|
| placeholder | `str \| None` | None | Shown when empty |
| value | `str \| None` | None | Initial value (seeds state) |
| name | `str \| None` | None | State key; auto-generated if omitted; use `.rx` |
| rows | `int \| None` | None | Visible text rows |
| disabled | `bool` | False | Non-interactive |
| required | `bool` | False | Required for form submission |
| css_class | `str \| None` | None | Appended to built-in styles |

Protocol-only extras: `minLength`, `maxLength`, `onChange` (`Action | Action[]`) (not in the Python parameter table; Form.from_model emits `rows`).

**Example (basic):**
```python
from prefab_ui.components import Textarea

Textarea(placeholder="Enter your message...")
```

**Example (live character count with `.rx.length()`):**
```python
from prefab_ui.components import Column, Text, Textarea

with Column(gap=4):
    ta = Textarea(placeholder="Describe your journey through the galaxy...", rows=4)
    Text(f"Character count: {ta.rx.length()}")
```

**Other snippets:**
```python
# label + rows
with Column(gap=2):
    Label("Feedback")
    Textarea(
        placeholder="Tell us what you think...",
        rows=5,
    )

# initial value
Textarea(
    value="This is some initial content that can be edited.",
    rows=4,
)

# disabled
Textarea(placeholder="This textarea is disabled", disabled=True)
```

**Gotchas:** No built-in caption; pair with a `Label` in a `Column`. `disabled` makes it read-only, muted, and out of the tab order. In `Form.from_model`, use `json_schema_extra={"ui": {"type": "textarea", "rows": N}}` to get a Textarea.

---

## Video

**Purpose:** Play video files with native HTML5 controls (`<video>`); supports dynamic URLs via `{{ field }}` interpolation.

**Import:** `from prefab_ui.components import Video`

| prop | type | default | notes |
|---|---|---|---|
| src | `str` *required* | - | Video URL; first positional arg |
| poster | `str \| None` | None | Poster image URL shown before playback |
| controls | `bool` | True | Playback controls |
| autoplay | `bool` | False | Auto-start; requires `muted=True` in most browsers |
| loop | `bool` | False | Loop |
| muted | `bool` | False | Mute |
| width | `str \| None` | None | CSS width with units |
| height | `str \| None` | None | CSS height with units |
| css_class | `str \| None` | None | Tailwind classes |

**Example (basic):**
```python
from prefab_ui.components import Video

Video(
    src="https://mdn.github.io/shared-assets/videos/flower.mp4",
    width="100%",
)
```

**Example (autoplay, loop, no controls):**
```python
from prefab_ui.components import Video

Video(
    src="https://example.com/background.mp4",
    autoplay=True,
    muted=True,
    loop=True,
    controls=False,
)
```

**Example (poster):**
```python
from prefab_ui.components import Video

Video(
    src="https://example.com/presentation.mp4",
    poster="https://example.com/thumbnail.jpg",
    width="640px",
)
```

**Gotchas:** Browsers require `muted=True` for autoplay to work without user interaction. Width/height need CSS units.
