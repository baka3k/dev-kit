# High-Contrast Light Minimalist Design System

## Contents

1. Core philosophy: stark white and bold contrast
2. The 60-30-10 light theme rule (strict)
3. Palettes: pick one premium light theme per presentation
4. Extreme visual hierarchy and the hero element
5. Swiss grid: whitespace is the design
6. Strict layout architecture (Layouts 1–4)
7. Support layouts for dense content
8. Typography and spacing rules
9. Unit conversion: HTML px to PowerPoint
10. Data, diagrams, and imagery
11. Contrast and accessibility on light canvases
12. Client-brand override

## Core philosophy: stark white and bold contrast

Every slide must look and sound like it was crafted by a high-end human
design agency — Apple keynote or Pentagram editorial, not a template.
Because the canvas is light, contrast must come from **font weight, sizing,
and extremely deliberate use of color**. Three pillars:

1. **60-30-10 light discipline** — pristine white canvas, near-black
   structural ink, a tiny high-voltage accent budget.
2. **One hero element per slide** — one unmistakable focal point; everything
   else is deliberately quieter.
3. **Swiss grid where the whitespace IS the design** — do not fill empty
   corners; two or three content blocks at most; hairlines or soft shadows
   instead of heavy fills.

When a design decision is unclear, ask: does it sharpen the contrast around a
single focal point, or does it fill silence with noise? If noise, remove it.

## The 60-30-10 light theme rule (strict)

- **60% dominant canvas**: Pure White (`#FFFFFF`) or Crisp Pearl (`#F8FAFC`).
- **30% structural contrast**: Deep Obsidian (`#0F172A`) or Pitch Black
  (`#000000`) for text, headlines, and structural blocks.
- **10% high-voltage accent**: Electric Indigo (`#4338CA`), Vivid Crimson
  (`#E11D48`), or Burnt Orange (`#EA580C`).

Accent discipline:

- **Never use accent colors on more than 10% of a slide.**
- Accent is reserved for the hero number, one highlighted keyword, badge
  pills, the featured tile border, and thin 3–4 px highlight rules.
- Never set body copy in accent color. Never fill a large panel with pure
  accent except the single contrast block in Layout 2.
- One accent hue per deck. A deck that needs two accents has an unclear story.

## Palettes: pick one premium light theme per presentation

Pick exactly one palette for the whole deck. Do not mix them. A single
inverted slide (deep obsidian canvas, e.g. a closing statement) is permitted
as intentional structural contrast and uses the same palette tokens.

### Palette A: "Crisp Swiss" (Apple / tech style)

| Role | Color |
|---|---|
| Background | `#FFFFFF` Pure White |
| Card / secondary area | `#F1F5F9` Very Light Slate |
| Primary text | `#020617` Deepest Slate / near black |
| Secondary text | `#64748B` Cool Gray |
| Hero accent | `#4F46E5` Vivid Indigo, or `#059669` Emerald Green |
| Hairline border | `#E2E8F0` |
| Badge tint (8% accent) | `#F1F0FD` indigo · `#EBF7F3` emerald |

Use for: product and technology narratives, executive reviews, data stories,
anything that should feel like an Apple keynote.

### Palette B: "Warm Editorial" (high-end consulting / magazine)

| Role | Color |
|---|---|
| Background | `#FDFBF7` Warm Alabaster / off-white |
| Card / secondary area | `#F3F0E6` Muted Sand |
| Primary text | `#1C1917` Deep Stone / espresso |
| Secondary text | `#78716C` Warm Neutral Gray |
| Hero accent | `#EA580C` Burnt Orange, or `#DC2626` Classic Crimson |
| Hairline border | `#E7E2D8` |
| Badge tint (8% accent) | `#FDF2EC` orange · `#FCEEEE` crimson |

Use for: consulting proposals, strategy and editorial pitches, conservative
or risk-averse customers (including traditional Japanese enterprise).

## Extreme visual hierarchy and the hero element

- Every slide has **exactly one** unmistakable hero element: a massive key
  metric, a highlighted high-contrast quote, or a stark accent/obsidian
  contrast block.
- Because the background is white, hero type must be HUGE and ultra-bold:
  120–160 px (90–120 pt) at weight 800, in near-black or the accent color.
  The hero is at least ~6× the support type.
- If two things on a slide compete for attention, one of them moves to
  another slide, the appendix, or the speaker notes.
- Support content recedes: secondary gray, smaller sizes, hairline borders.

Hero catalog:

| Layout | Hero element |
|---|---|
| Layout 1 — Hero Metric | One giant number in accent color on vast white |
| Layout 2 — Stark Editorial Split | The solid accent or obsidian block |
| Layout 3 — Tiled Comparison | The single featured tile with accent border |
| Layout 4 — Bold Statement | One oversized sentence with accent left rule |

## Swiss grid: whitespace is the design

- 12-column grid on a 1280 × 720 canvas (13.333 × 7.5 in in PowerPoint).
- Outer padding: 60 px top/bottom, 80 px left/right (0.625 in / 0.833 in).
- **Maximum 2–3 content blocks per slide.** Do not fill empty corners.
- Define areas with ultra-thin borders (1 px `#E2E8F0`) or one soft, wide
  shadow (`0 8px 24px rgba(0, 0, 0, 0.04)`) — never both on the same card,
  never a heavier shadow.
- Badge pills: tinted accent background (8% accent over white), accent text,
  no border, uppercase, tracked, small.
- Card radius 16 px (≈ 0.16 in). Keep peer cards geometrically identical.
- Leave at least one visibly quiet zone on every slide — on a light canvas,
  silence reads as confidence.

## Strict layout architecture (Layouts 1–4)

These four layouts carry the narrative of every deck. Choose per content, not
for novelty, and never force content into a layout it does not fit.

### Layout 1 — Hero Metric / High Impact

- **Use case**: key performance indicators, market sizes, headline stats.
- Number size: 120–160 px (90–120 pt), weight 800, tight tracking.
- Accent color applies exclusively to the stat number or key symbol.
- The rest of the slide is vast, empty white space plus one tight,
  human-written explanatory paragraph (≤ 25 words) in secondary gray.
- One number per slide. Optional badge-pill eyebrow above the number.

### Layout 2 — Stark Editorial Split

- **Use case**: big statements, key takeaways, chapter dividers.
- Exactly 50/50 split.
- Left side: pure white with a massive black headline (44–56 px / 33–42 pt,
  weight 800).
- Right side: a solid block of the accent color or deep obsidian containing
  one key quote or statement — or a full-height high-resolution image.
- Text on the solid block must keep ≥ 4.5:1 contrast (see §11): white on
  indigo/obsidian, deep stone on burnt orange.
- Images bleed to the slide edge; no borders, no rounded corners on bleeds.
  Use only authentic, relevant, licensed imagery.

### Layout 3 — Minimalist Tiled Comparison / Core Pillars

- **Use case**: frameworks, three core strategies, feature breakdowns.
- **Maximum 3 tiles.** Never push 4 or 5 cluttered tiles.
- Tiles sit on the white canvas with a very light background
  (`#F1F5F9` / `#F3F0E6`) and no border by default.
- Highlight exactly one tile as the Featured Hero Tile with a crisp accent
  border, 2 px. All other tiles stay borderless and quiet.
- Tile title ≤ 6 words; tile body ≤ 20 words.

### Layout 4 — Bold Statement / Minimal Quote

- **Use case**: vision statements, customer testimonials, powerful quotes.
- Typography: 48–64 px (36–48 pt), weight 700–800, near-black, generous line
  height.
- Clean left-border highlight, 4 px (3 pt) in accent color.
- Never use this layout without an actual attributed quote or a genuinely
  owned statement.

## Support layouts for dense content

Roadmaps, layered architectures, matrices, decision tables, and risk registers
do not fit the four hero layouts. Rules:

- Put the overview slide in a hero layout (the single takeaway or number);
  keep the dense detail in support slides or an appendix.
- Support slides still obey the palette, hairline borders, and the
  one-highlight rule: only the item the audience must discuss gets the accent.
- Tables and process steps: hairline structure, near-black content, accent
  for the one active row, stage, or decision.
- Body text never below 14 pt in `.pptx`. If it does not fit, split the slide
  instead of shrinking the type.
- Prefer one diagram with a clear reading path over a dense "everything map".

## Typography and spacing rules

- **Title font**: clean geometric sans-serif — `Plus Jakarta Sans`, `Inter`,
  `Helvetica Neue`, or `SF Pro Display`. Weight 700 or 800.
- **Body font**: highly readable sans-serif — `Inter` or `Plus Jakarta Sans`.
  Weight 400.
- **Title character limit**: maximum 35 characters per title. Punchy and
  human.
- **Body text limit**: 30–40 words per text block. Concise, human-written
  phrases only.
- Badge pills / eyebrows: 14 px (10.5 pt), uppercase, letter-spacing ≈ 1 px,
  weight 600.
- Footnotes, sources, citations: 12 px (9 pt) minimum — never smaller.
- Font reality: `SF Pro Display` ships only on Apple platforms and must not
  be embedded or redistributed; treat it as a macOS presentation nicety and
  fall back to `Helvetica Neue` or `Inter` elsewhere. When web fonts cannot
  be guaranteed in `.pptx`, fall back to Arial (Latin + Vietnamese diacritics
  covered) or Aptos, and to Meiryo UI / Yu Gothic UI for Japanese runs. Verify
  the rendered font in the render step — silent substitution is a defect.

## Unit conversion: HTML px to PowerPoint

The HTML canvas is 1280 × 720 px at 96 dpi, which is exactly the 16:9
PowerPoint canvas: 13.333 × 7.5 in (960 × 540 pt). Therefore:

- 1 px = 0.75 pt = 1/96 in.
- Slide padding 60 px × 80 px = 0.625 in × 0.833 in.
- Card radius 16 px ≈ 0.16 in.
- 4 px accent rule = 3 pt. 1 px hairline = 0.75 pt. 2 px featured border =
  1.5 pt.

| HTML px | PowerPoint pt | Use |
|---|---|---|
| 120–160 px | 90–120 pt | Hero metric number |
| 48–64 px | 36–48 pt | Bold statement / quote |
| 44–56 px | 33–42 pt | Slide title / split headline |
| 18–20 px | 13.5–15 pt | Description and body (keep ≥ 14 pt in `.pptx`) |
| 14 px | 10.5 pt | Badge pill / eyebrow |
| 12 px | 9 pt | Footnote / source |

When the same design is built in HTML and in `.pptx`, the HTML values are the
source of truth; the `.pptx` uses this table.

## Data, diagrams, and imagery

- Use native PowerPoint charts when editability matters.
- Start quantitative axes at zero for counts and amounts unless a truncated
  axis is explicitly justified and labeled.
- Label units, time period, source, and whether data is actual, target, or
  illustrative.
- Direct labels beat legends. One accent color for the key series; muted
  gray tones for context series.
- Tables for precise comparison, charts for patterns.
- Icons only when they improve scanning: one icon family, one stroke style,
  subordinate to text.
- Photographs only when authentic, relevant, licensed, and compositionally
  useful. No generic "innovation" stock imagery.
- No gradients, glows, or 3D effects. The only permitted depth is the single
  soft card shadow from §5.

## Contrast and accessibility on light canvases

Verified contrast ratios, Palette A "Crisp Swiss":

| Pair | Ratio | Use |
|---|---|---|
| `#020617` primary on `#FFFFFF` | ≈ 20:1 | All reading text |
| `#64748B` secondary on `#FFFFFF` | ≈ 4.8:1 | Support copy |
| `#4F46E5` indigo on `#FFFFFF` | ≈ 6.3:1 | Hero type, badges, links |
| `#059669` emerald on `#FFFFFF` | ≈ 3.8:1 | Hero-size type and graphics only |
| White on `#4F46E5` / `#0F172A` | ≈ 6.3:1 / ≈ 17.9:1 | Text on Layout 2 blocks |
| `#020617` ink on `#059669` | ≈ 5.4:1 | Text on emerald blocks (not white) |

Verified contrast ratios, Palette B "Warm Editorial":

| Pair | Ratio | Use |
|---|---|---|
| `#1C1917` primary on `#FDFBF7` | ≈ 16.9:1 | All reading text |
| `#78716C` secondary on `#FDFBF7` | ≈ 4.6:1 | Support copy |
| `#DC2626` crimson on `#FDFBF7` | ≈ 4.7:1 | Hero type and badges |
| `#EA580C` orange on `#FDFBF7` | ≈ 3.4:1 | Hero-size type and graphics only |
| `#1C1917` stone on `#EA580C` | ≈ 4.9:1 | Text on orange blocks (not white) |

Rules:

- Keep at least 4.5:1 for all reading text; accents below 4.5:1 are for
  hero-size type and graphics only.
- Light decks wash out on bright projectors. Secondary gray is the floor —
  never go lighter than `#64748B` / `#78716C` for text that must be read.
- Do not encode meaning by color alone; pair accent with position, weight, or
  a label.
- Hairlines (`#E2E8F0`) are for structure, never for text.

## Client-brand override

When the client supplies a brand template or explicit brand colors:

1. Preserve masters, layouts, theme relationships, and brand assets.
2. Re-map the 60-30-10 roles onto the brand palette: light brand canvas at
   60%, the darkest brand neutral at 30%, the strongest brand hue at 10%.
3. Keep every rule that is not brand-specific: one hero per slide, ≤ 3 tiles,
   title ≤ 35 characters, body blocks ≤ 40 words, anti-AI voice, hairline
   geometry, and the full QA gate.
