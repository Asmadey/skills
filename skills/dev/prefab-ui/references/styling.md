# Styling: Tailwind classes, CSS helpers, themes

Source: prefab.prefect.io/docs/styling/css and /styling/themes; import paths checked on prefab-ui 0.21.1.

## Without a theme

No theme is required. The base renderer ships with system fonts, automatic gaps between cards, comfortable card
padding and gradient fills on progress bars. Layout: `Row`/`Column` take `gap` (Tailwind spacing scale, `gap=4` =
`1rem`), `align="center"`, `justify=...`. The root column of `PrefabApp` has class `pf-app-root` (themes target it for
default padding); add yours with `PrefabApp(css_class="max-w-3xl mx-auto p-6")`.

## `css_class` and `id`

Every component accepts `css_class` (Tailwind utility classes) and `id` (HTML id on the outermost element, useful for
custom CSS selectors and anchors). `css_class` also accepts a **list of strings**, joined with spaces.

```python
Card(id="status-card", css_class="my-card-styles")
Column(css_class="w-auto")                       # shrink a column to its content (default is full width)
Div(css_class="bg-emerald-500 rounded-md h-10 w-24")
```

## Variant and breakpoint helpers (`prefab_ui.css`)

Each helper prefixes every class in a space-separated string. Returns a plain string.

| Helper | Prefix | | Helper | Prefix / min width |
|---|---|---|---|---|
| `Hover` | `hover:` | | `Sm` | `sm:` 640px |
| `Focus` | `focus:` | | `Md` | `md:` 768px |
| `FocusVisible` | `focus-visible:` | | `Lg` | `lg:` 1024px |
| `FocusWithin` | `focus-within:` | | `Xl` | `xl:` 1280px |
| `Active` | `active:` | | `Xxl` | `2xl:` 1536px |
| `Disabled` | `disabled:` | | `Responsive`, `Any` | for responsive layout props |

```python
from prefab_ui.css import FocusVisible, Hover, Md, Lg

Card(css_class=[
    "p-3 text-sm transition-shadow",
    Md("p-6 text-base"),
    Lg("p-8 text-lg"),
    Hover("shadow-lg"),
    FocusVisible("ring-2 ring-primary"),
])
Button("Submit", css_class=["w-full", Md("w-auto"), Lg("w-1/2")])   # -> "w-full md:w-auto lg:w-1/2"
```

Breakpoints apply from that width *and up*. Layout props that accept `Responsive` (`Grid.columns`, `Grid.gap`,
`Dashboard.gap`, `css_class` on Grid/Dashboard items): a dict whose `default` key is the base and `sm md lg xl 2xl`
override progressively, e.g. `Grid(columns={"default": 1, "md": 2, "lg": 4})` (see Grid in `references/components-*.md`).
`Grid(min_column_width="16rem")` is the other responsive option (mutually exclusive with `columns`).

## Themes

```python
from prefab_ui.app import PrefabApp
from prefab_ui.themes import Presentation          # also: Basic, Minimal, Theme, Windows2000, MySpace
app = PrefabApp(view=my_view, theme=Presentation(accent="blue"))
```

| Theme | Character |
|---|---|
| (none) | system fonts, auto card gaps, gradient fills: what every app looks like by default |
| `Basic` | default look + accent/font/mode options |
| `Presentation` | dark blue-slate chrome, Inter, gradient fills, generous card padding, tinted badges, taller table rows; for slides, demos, focused data displays. Renders dark regardless of OS preference unless `mode="light"` |
| `Minimal` | strips all renderer defaults: no card padding, no auto gaps, no gradients; you control everything |
| `Windows2000` | total conversion (bevelled gray controls, Tahoma, VGA chart palette): any dashboard becomes a Windows 2000 program |
| `MySpace` | black starfield, neon glow borders, Comic Neue, lime text; helper classes `pf-neon-pink/cyan/lime/yellow`, `pf-visitor-counter`, `pf-construction`, animated `pf-blink`/`pf-rainbow`/`pf-sparkle` (animations respect `prefers-reduced-motion`; blinking is a photosensitivity risk, avoid in real products) |
| `Theme` | full control: `css`, `light_css`, `dark_css`, `font`, `font_mono` |

Options on any theme:

```python
Basic(accent="amber")            # Tailwind name (defaults to 500 shade)
Basic(accent="amber-600")        # specific shade
Basic(accent="#3b82f6")          # hex / CSS colour string
Basic(accent=260)                # OKLCH hue 0-360
Basic(font="Geist", font_mono="Geist Mono")     # auto-imported from Google Fonts (network at render time)
Presentation(font="IBM Plex Sans")              # Presentation loads Inter by default
Basic(accent="blue", mode="dark")               # default: follow the OS light/dark preference
```

`accent` controls the primary colour, focus rings and chart colours (`chart-1..5`). With `accent=None` (default) no
colour overrides apply and components use the neutral zinc palette. Verified: `Presentation(accent="blue")` adds a
`css` block to the wire JSON; `Basic(mode="dark")` adds `"mode": "dark"`.

Custom theme:

```python
from prefab_ui.themes import Theme
Theme(font="Inter", css=".pf-table-cell { font-variant-numeric: tabular-nums; }")
Theme(
    light_css="--primary: oklch(0.60 0.24 260); --ring: oklch(0.60 0.24 260);",
    dark_css="--primary: oklch(0.70 0.18 260); --ring: oklch(0.70 0.18 260);",
)
```

CSS variables (shadcn/ui naming, so output of any shadcn theme generator can be pasted into `light_css`/`dark_css`):

| Variable | Controls |
|---|---|
| `primary` / `primary-foreground` | primary buttons, active states |
| `secondary` / `secondary-foreground` | secondary buttons |
| `accent` / `accent-foreground` | highlighted surfaces |
| `background` / `foreground` | page background, default text |
| `card` / `card-foreground` | card surfaces |
| `muted` / `muted-foreground` | subdued text and surfaces |
| `destructive` | delete / error |
| `success` / `warning` / `info` | semantic status colours |
| `border` | borders and dividers |
| `ring` | focus rings |
| `chart-1` ... `chart-5` | chart palette |
| `radius` | border radius |
| `card-padding-y` | card vertical padding (default `1rem`) |
| `layout-gap` | gap between cards in containers (default `1rem`) |

Other ways to style: `PrefabApp(css=["..."])` (inline `<style>`), `PrefabApp(stylesheets=[url])` (`<link>`, also adds
CSP origins), `PrefabApp(mode="light"|"dark")`. Component variants (`variant="success"`, `size="sm"`) are listed per
component in `references/components-*.md`. In the playground, theme styles stay with the preview.

## Accessibility

`aria_label` and `aria_labelledby` (space-separated DOM ids) exist on components; both accept reactive expressions.
`aria_labelledby` wins when both are given. They name the existing semantic element (button, input, calendar grid, chart
svg, table); they do not give a layout container a role. For Dialog/Popover/HoverCard/Tooltip they name the popup
content; Tabs names the tablist, Tab its trigger. Unnamed `Icon`s are decorative; naming one exposes it to assistive tech.
`Label("Search", id="search-label")` + `Input(aria_labelledby="search-label")`. Transparent control-flow nodes
(`ForEach`, `If`, `Slot`) create no DOM root: name what they render. Do not use blinking/animated themes for real users.
