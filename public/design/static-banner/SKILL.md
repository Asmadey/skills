---
name: Static Banner Creator
description: Use when the user wants to create static ad banners, ad creatives, or promotional images for social media ads. Uses Higgsfield API to generate images.
category: framework
source: local
version: 1.0.0
last_updated: 2026-03-24
---

# Static Banner Creator

Generate production-ready image prompts for static advertising banners across 4 proven templates.

## Core Principle

Guide the user through selecting a template, gathering creative inputs via interactive Q&A, and producing polished image-generation prompts ready for AI tools (Nanobanana, Midjourney, Seedream, Flux, Krea, Reve, Higgsfield, ElevenLabs).

## Universal Rule: Break Banner Blindness

**EVERY banner MUST include at least one scroll-stopping mechanism.** Users are in "scrolling coma" — feed autopilot where ads are invisible. The banner must jolt them out of it.

Apply one or more of these techniques to EVERY prompt you generate:

### 1. High Visual Contrast
- Clashing color pairs (neon on black, warm on cold, saturated on desaturated)
- Light subject on dark background or vice versa — avoid mid-tone-on-mid-tone
- Hard graphic edges, bold outlines, or color blocking that breaks the feed's visual rhythm

### 2. Pattern Disruption Element
- Something that "shouldn't be there": an object out of context, surreal scale, impossible physics
- Visual glitch, intentional imperfection, or raw texture that breaks the polished feed aesthetic
- Meme-native formats, handwritten scribbles over clean photos, sticky notes, arrows, circles drawn by hand

### 3. Extreme Emotion or Expression
- Exaggerated facial expression (shock, joy, disgust, disbelief) — faces with strong emotion stop scrolling
- Dynamic body language: mid-action, tension, urgency
- Eye contact with the viewer — direct gaze creates involuntary pause

### 4. Visual Tension or Incompleteness
- Cropped elements that make the brain want to "complete" the image
- Before/after juxtaposition, split frames, or visual contradiction
- Text that starts a thought but doesn't finish it (curiosity gap)

### 5. Unusual Color or Lighting
- Neon glow, duotone, infrared, inverted colors — anything that doesn't look like a stock photo
- Harsh flash (party/paparazzi aesthetic), dramatic rim lighting, colored gels
- Monochrome with a single accent color punch

### How to Apply
When generating any prompt (regardless of template), always inject at least one scroll-stopping technique into the visual description. If the user's brief is neutral or safe, proactively suggest a boldness upgrade. Ask: *"Should we add a pattern-disruption element to break banner blindness?"*

In the final prompt, include an explicit line like:
`Scroll-stop mechanism: [describe the specific technique used]`

## When to Use

- User wants to create a static ad banner or ad creative
- User needs image prompts for advertising visuals
- User wants to generate promotional images for Meta, Google, Pinterest, TikTok, Instagram
- User asks for ad creative ideas or banner concepts

## Workflow

### STEP 1 — Template Selection

Present these 4 templates and help the user choose:

**Template 1: Character + Text**
A character/person photo with a text message overlay. Simple, universal, works across many niches.
- Character can be: someone the user identifies with, an aspirational figure, an expert, a charismatic/unusual personality, or even non-human
- Style can be photorealistic or stylized
- Best for: trust-building, targeting specific audiences, personality-driven ads

**Template 2: Pinterest Infographic Collage**
Multi-tile visual with structured information — looks like a guide, checklist, or collection.
- Popular in Health & Fitness but adaptable to any category
- Works because it looks like a saveable resource, not an ad
- Users click expecting to zoom in on details
- Best for: educational content, how-to guides, tips collections, challenges

**Template 3: Text on Surface**
Text placed on an interesting texture or object — the message is the hero.
- Surfaces: interfaces (Apple Notes, tweet, iMessage), everyday objects (sticker, receipt, polaroid), urban (billboard, sidewalk), nature (sand, sky, ice), body (tattoo), unusual (foggy mirror, snow tracks, lipstick)
- Best for: strong hooks, emotional messages, pattern disruption in feed

**Template 4: Diagnostic/Calculator Preview**
Visual preview of a diagnostic tool or mini-calculator leading to a quiz.
- Looks like a useful structured tool, not an ad
- Creates perception of expertise and order
- Best for: niches with quick assessments — health, fitness, psychology, relationships, finance, learning

### STEP 2 — Generation Method

For each template, offer the user a choice:

**Option A: Full banner in one prompt** — Generate image + text together in AI image generator
**Option B: Character/background separately** — Generate visual element, then add text in Figma or other editor (more control for iterations)

### STEP 3 — Interactive Q&A

Run the appropriate mega-prompt based on the selected template. Ask questions ONE AT A TIME. After each answer, provide relevant examples and suggestions.

---

## Template 1: Character + Text — Mega-Prompts

### Option A: Full Banner (Character + Text together)

Run this interactive flow:

```
You are the AI Ad Creative Builder.
Your job:
1. Ask me 8 short questions, one at a time.
2. Question 1 is optional: offer to upload a reference image for layout inspiration.
3. After receiving all answers, generate ONE complete image-generation prompt for an ad creative (for Midjourney / Seedream / Flux / etc.).
4. Do NOT show internal logic. Only the quiz then the final ready prompt.

The final output MUST include:
- a strong HOOK headline
- a clear SUBHEADLINE explaining the offer
- a short PRODUCT EXPLANATION (2-3 lines)
- 2-4 BENEFIT BULLETS tied to persona and promise
- CTA (from the user)
- hero description + background + lighting + composition
- layout structure (guided by the optional reference if provided)
- full text overlay in the selected language
- typography notes
- disclaimer ONLY if user selected "yes"

Questions in order:
1. Would you like to provide a reference image for layout inspiration? (yes/no)
2. What product or offer is being advertised? (1-2 sentences)
3. Who is the target persona? (age + gender + main need or pain)
4. What is the key promise or result?
5. Which visual style? (realistic fitness / clean fashion / dark dramatic / illustrated / editorial)
6. Format + CTA? (example: 9x16 + "Start saving today")
7. Do you want a disclaimer? (yes/no)
8. Which language should the final ad text be written in?

After collecting all answers: Generate ONE clean, ready-to-paste image prompt.
```

### Option B: Character Only (add text in editor)

Run this interactive flow:

```
You are the AI Character Builder.
Your task:
1. Ask me 8 short questions, one at a time.
2. Question 1 is optional: offer to upload a reference image.
3. After collecting answers, generate ONE complete prompt for creating a character image.
4. Do NOT show internal logic. Only the quiz then the final ready prompt.

The final output MUST include:
- character appearance (gender, age, facial traits, body type)
- ethnic background + vibe
- outfit style
- mood / personality
- chosen IMAGE STYLE
- lighting type
- camera type (smartphone / DSLR / film)
- background/environment
- framing (headshot / half-body / full-body)
- extended negative space for text (part of scene, NO cropping)
- optional reference matching
- no ad copy

Questions:
1. Would you like to upload a reference image? (yes/no)
2. Who is the character? (gender + age + short physical description)
3. What ethnic background or facial vibe?
4. What outfit style? (casual, athletic, business, vintage, streetwear, techwear)
5. What mood or personality? (confident, shy, mysterious, friendly, serious)
6. What IMAGE STYLE? (studio realism / natural daylight / UGC smartphone / low-lit / flash-lit / cinematic / editorial / vintage film)
7. What composition? (headshot / half-body / full-body)
8. Where should the empty TEXT SPACE be? (left / right / top / bottom / none)

After receiving all answers: Generate ONE clean, ready-to-paste image prompt.
```

---

## Template 2: Pinterest Infographic Collage — Mega-Prompt

### Phase 1: Concept Generation

Run this interactive flow:

```
You are an expert creative strategist specializing in Pinterest-style infographic collages.

STEP 1 - Basic Context
Ask: product_description + target_segment (one at a time)

STEP 2 - Creative Direction
Ask: What to show in tiles? Focus areas? How to grab attention?

STEP 3 - Visual Settings
Ask or apply defaults:
- layout: number of tiles (default: 5)
- composition_type: symmetric | asymmetric | collage
- banner_format: 1x1 | 9x16 (default: 9x16)
- style: photographic | flat icons | minimalist | cinematic | cartoon realism | collage
- color_vibe: pastel | vibrant | dark | natural | brand palette
- emotion_focus: calm | energetic | inspiring | cozy | confident
- tone: playful | expert | minimalist | aesthetic | bold
- brand_words: 3-6 key adjectives

STEP 4 - Copy & UX
- headline_style: statement | question | how-to | challenge
- CTA: propose 2-3 options
- icon_style: emoji | line icons | filled icons
- typography_vibe: friendly sans | geometric sans | soft serif
- language: RU / EN / bilingual

STEP 5 - Constraints
Do / Don't rules (defaults: realistic proportions, positive tone, no exaggerated bodies, no medical promises)

STEP 6 - Confirm all inputs

STEP 7 - Generate 6 concepts:
1. Challenge / Routine
2. Tricks / Facts Collection
3. Test / Personality Grid
4. Matrix / Decision Map
5. Myths vs Facts
6. Wildcard (seasonal, emotional, contrarian)

Each concept includes: Main Headline, Tiles with Title + Details + Icon + Image prompt, CTA, Visual notes.
```

### Phase 2: Banner Generation

After user picks a concept:

```
Using the following concept, create a mobile-first vertical Pinterest infographic (1080x1920).
Divide the layout into distinct sections matching each category.
Place the main headline at the top and subheadings with bullet points in their own blocks.
Style rules: each block must look zoom-worthy; max 7-9 words per line; use curiosity or self-recognition triggers; avoid jargon; use icons only if they clarify.
Apply the specified visual notes for layout, colour palette and image cues.
Concept: [INSERT CHOSEN CONCEPT]
```

---

## Template 3: Text on Surface — Mega-Prompt

Run this interactive flow:

```
You are the Ad Creative Text-On-Surface Prompt Builder.

STEP 1 - PRODUCT
What product or service? (describe benefit clearly in 5 seconds)

STEP 2 - TARGET AUDIENCE
Who? (age, pain points, motivations)
Internal cues: Pain / Dream / Identity

STEP 3 - MESSAGE TEXT (HOOK)
What message should appear? If unsure, propose 5 variations using:
- Curiosity Gap: "Are you smarter than you think?"
- Pain->Dream: "2 minutes to feel smart again."
- Value Framing: "Your smartest habit starts today."
- Identity Trigger: "For people who want to grow daily."
- Challenge Hook: "Prove your mind in 15 questions."

STEP 4 - SURFACE + SETTING (choose 3)
Clean & Trust-Building: mirror note, Apple Notes, notebook page
Lifestyle: phone screen, sticky note on fridge, kitchen table note
Bold: foggy glass, sand writing, asphalt stencil, lipstick on mirror

STEP 5 - VISUAL STYLE + MOOD
Options: clean UGC, editorial minimalism, warm cozy daylight, high-contrast bold, film-like nostalgic

STEP 6 - TEXT STYLE & WRITING MATERIAL
Font: clean sans-serif / handwritten / bold marker / stencil / elegant script
Material: pen / pencil / marker / lipstick / chalk / digital
Texture: rough / clean / smudged / sandy / wet condensation

STEP 7 - ASPECT RATIO
1:1 (IG feed) / 4:5 (IG posts) / 9:16 (Reels/TikTok) / 16:9 (YouTube)

FINAL OUTPUT: 3 prompts, one per selected surface:
"{SURFACE + SETTING}, with the text '{TEXT}' written in {TEXT_STYLE} using {MATERIAL}, crafted to influence {TARGET_AUDIENCE} through marketing triggers (curiosity, clarity, emotional pull), illustrating the core promise of {PRODUCT}. {VISUAL_STYLE + MOOD}. Perfect readability, strong contrast, realistic textures, natural shadows, clean composition, accurate lighting, no watermarks, no logos, no AI labels, {ASPECT_RATIO}."
```

---

## Template 4: Diagnostic/Calculator Preview — Mega-Prompt

Run this interactive flow:

```
You are the Diagnostic Ad Creative Builder.
Create a visual preview of a diagnostic tool or mini-calculator that looks like a useful instrument leading to a quiz.

STEP 1 - NICHE/TOPIC
What niche? (health, fitness, psychology, relationships, finance, learning, etc.)

STEP 2 - MAIN PROBLEM OR PROMISE
What problem does the diagnostic solve? What will the user learn about themselves?

STEP 3 - PARAMETERS (3-7 items)
What parameters/metrics does the diagnostic evaluate?
After each answer, generate 5 NEW context-adapted example options.

STEP 4 - CTA
What action should the user take? (e.g., "Take the quiz", "Get your score", "Find out now")

STEP 5 - VISUAL STYLE
Clean medical / dark tech / warm wellness / minimalist / data-dashboard / editorial

STEP 6 - DESIGN CONSTRAINTS
Do / Don't rules for the visual

STEP 7 - ASPECT RATIO
1:1 / 4:5 / 9:16 / 16:9

FINAL OUTPUT: ONE polished image-generation prompt describing layout, headline, parameters, aesthetic, restrictions, ratio, and CTA — creating the impression of a diagnostic instrument leading to a quiz.
```

---

## Recommended AI Image Generators

### Higgsfield Platform API Models (automated generation)

When generating via Higgsfield API, use these model endpoints:

| Model ID | Best For | Resolution | Text Quality |
|----------|----------|------------|-------------|
| **`nano-banana-pro`** | **DEFAULT for all banners with text** — best text rendering, 4K capable | `1k` / `2k` / `4k` | Excellent |
| `nano-banana` | Fast generation, good text | `1k` / `2k` / `4k` | Good |
| `flux-2` | Alternative for complex compositions | `1k` / `2k` / `4k` | Good |
| `reve` | Native-looking digital artifacts, UGC feel | `1k` / `2k` / `4k` | Medium |
| `higgsfield-ai/soul/standard` | Portraits without text, character generation | `1080p` | Poor |
| `flux-kontext` | Image editing / style transfer | — | — |

**Note:** Always use `nano-banana-pro` for banners that contain text. Soul Standard produces garbled, unreadable text — never use it for text-heavy creatives.

**API parameters by model:**
- `nano-banana-pro` / `nano-banana` / `flux-2` / `reve`: `resolution` accepts `1k`, `2k`, `4k`
- `higgsfield-ai/soul/standard`: `resolution` accepts `1080p`
- All models: `aspect_ratio` accepts `9:16`, `16:9`, `4:3`, `3:4`, `1:1`, `2:3`, `3:2`
- Note: `4:5` is NOT supported — use `3:4` as the closest alternative for Meta feed ads

### Other Generators (manual via UI)

| Tool | Best For |
|------|----------|
| **Nanobanana (UI)** | Best prompt adherence + text rendering |
| **Reve** | Native-looking digital artifacts |
| **Seedream 4** | Camera angles + dynamic perspective, up to 4-5K |
| **Midjourney** | Largest image dataset, most personalization options |
| **Krea** | Fast + beautiful, ~8 free generations/day |
| **ElevenLabs** | Image + video generation |

## Batch Generation Mode

When the user asks for a "pack" or "batch" of banners, use the automated pipeline.

### How Claude should handle batch requests

When the user says "make 10 banners" or "create a banner pack":

1. **Ask the user** for: product, target audience, CTA text, brand text, number of banners
2. **Generate concepts** — come up with N scroll-stop concepts using the Proven Archetypes table below
3. **Present concepts** to the user for approval
4. **Write a generation script** — create a `.mjs` file based on `scripts/generate-banners.mjs` template:
   - Import `generateImage` from `./scripts/hf-api.mjs`
   - Define `BANNERS` array with `id` + `prompt` for each concept
   - Define `FORMATS` array: `3:4` (feed) + `9:16` (stories)
   - Set output directory
5. **Run the script** via Bash: `node scripts/generate-my-pack.mjs`
6. **Report results** — show which banners succeeded/failed, open output folder

### Prerequisites for batch mode

The user needs these files in their project:
- `scripts/hf-api.mjs` — Higgsfield API client (included in this kit)
- `.env` — with `HF_KEY_ID` and `HF_KEY_SECRET` from https://platform.higgsfield.ai

### How it works

1. Create a generation script (see `scripts/generate-banners.mjs` as template)
2. Define banners array with `id` + `prompt` for each concept
3. Define formats array (e.g. `3:4` for feed + `9:16` for stories)
4. Script calls Higgsfield API via `scripts/hf-api.mjs`
5. Output goes to `output/{pack-name}/`

### Proven Scroll-Stop Concepts (validated, all performed well)

These concept archetypes work and can be remixed for any product:

| Archetype | Example | Why it works |
|-----------|---------|-------------|
| **Neon object in void** | Glowing passport on black | Extreme light-dark contrast |
| **Stamp/mark on face** | Red "APPROVED" stamped on portrait | Confrontational + eye contact |
| **Object on fire** | Burning employment contract | Primal attention trigger |
| **LED/display board** | Airport departure board | Familiar format, bold yellow-on-black |
| **Chalk/handwritten on black** | Provocative text on blackboard | Maximum contrast + raw texture |
| **Flash celebration** | Harsh flash + confetti + screaming joy | Extreme emotion + UGC energy |
| **Split face duotone** | Cold blue vs warm gold halves | Visual tension + before/after |
| **Giant UI element** | Oversized push notification | Recognizable pattern + aspiration trigger |
| **Luxury flat-lay** | Red wax seal on white marble | Bold color accent on neutral |
| **Surreal metaphor** | Person underwater reaching for glowing object | Impossible scene = pattern disruption |
| **VIP exclusivity** | Velvet rope + golden light | Exclusivity trigger |
| **Breaking through** | Fist through glass wall | Action + empowerment |
| **Golden ticket** | Glowing metallic ticket on black | Magical + aspirational |
| **Paparazzi flash** | Red carpet + multi-camera flash | Celebrity energy + chaos |
| **Neon sign in dark** | Neon text on wet dark alley | Cyberpunk mood + reflections |
| **Ripping paper** | Tearing up rejection letter | Visceral defiance |
| **Biometric scan** | Green fingerprint scan approved | Tech aesthetic + green on black |
| **Astronaut/epic scale** | Astronaut reaching for Earth | Surreal + aspirational |
| **Door with light** | Golden light through keyhole/door | Mystery + chiaroscuro |
| **Megaphone/pop-art** | Red megaphone + comic-style burst | Pop-art energy + red on black |

### Anti-Patterns (underperformed — AVOID)

- Clean studio portraits with soft lighting
- Object flat-lays with neutral tones (passport on desk)
- Screenshot mockups (LinkedIn posts, iMessage threads) — too much detail, no visual punch
- Before/after splits with realistic desaturated tones — not enough contrast
- UI dashboard screenshots — too busy, no focal point
- Sticky notes / written lists — too subtle

### Key Prompt Rules for Batch Mode

- Every prompt MUST specify the scroll-stop mechanism explicitly
- Always include brand text and CTA button text in the prompt
- Use dark/black backgrounds as default — they create the strongest contrast in mobile feeds
- Prefer single bold focal element over complex compositions
- Include "No watermarks, no AI labels" in every prompt

## Post-Generation Tips

- **Edit text**: Use Nanobanana2 with original as reference, draw/mark changes needed
- **Change angle/pose**: Use higgsfield.ai/app/angles or wavespeed.ai Qwen Edit
- **Vary character**: "Vary Person" prompt in Nanobanana quickly generates new character in same palette
- **Change format**: Seedream/Flux Kontext handle 9x16/16x9/4x5 format changes well
- **Style presets**: Use built-in generator presets to improve quality
- **Experiment**: Unexpected character generations often lead to top-performing creative directions
- **Stylization**: Characters don't have to be photorealistic — popular TV show styles work well
- **Image editors**: Nanobanana / Seedream / Qwen Edit (fal.ai, wavespeed.ai) / Flux Kontext for post-processing
