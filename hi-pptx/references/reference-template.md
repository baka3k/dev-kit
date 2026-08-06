# Sanitized presentation design system

Use this text-only design specification whenever no user-provided presentation
template overrides it. It contains no original slide content, logos, client
names, commercial information, or embedded media.

## Contents

1. Canvas and typography
2. Visual tokens
3. Spacing and component rules
4. Layout archetypes
5. Chart placement contract
6. Brand and privacy rules
7. Design-system QA

## 1. Canvas and typography

- Format: widescreen 16:9.
- Canvas: 13.333 x 7.5 inches; use a 1280 x 720 px planning coordinate system.
- Primary typeface: Calibri; use Aptos as the fallback when Calibri is not
  available.
- Main title: 26–28 pt bold.
- Section label: approximately 12 pt bold.
- Key-message rail: approximately 13 pt.
- Standard body: 10–13 pt; use larger text when the layout permits.
- Chart labels: target 11–14 pt and inspect the full-size render.
- Keep a title on one line. Shorten it or change the layout rather than shrinking
  below the defined hierarchy.

Use one typeface consistently within a deck unless the user-provided template
requires otherwise.

## 2. Visual tokens

| Role | Color | Use |
| --- | --- | --- |
| Primary navy | `#1F3864` | headers, title bands, primary series, key structure |
| Deep navy | `#00266A` | icons, labels, technical emphasis |
| Orange | `#F37021` | key message marker, recommendation, exception, highlight |
| Teal | `#127E84` | secondary option, supporting series, positive structure |
| Green | `#1E9E54` | achieved state, contribution, quality/review signal |
| Purple | `#7E4FB8` | testing/validation or a tertiary controlled category |
| Blue | `#2E6FD6` | digital/analysis support category |
| Gold | `#DEA548` / `#B28B34` | gates, tuning, milestones, rollout emphasis |
| Ink | `#1A284A` / `#222A36` | body text |
| Secondary text | `#5A6370` | descriptions, notes, metadata |
| Cool gray | `#EEF1F6` / `#F7F8FA` | message rails, alternating rows, soft panels |
| White | `#FFFFFF` | canvas and content surfaces |

Color discipline:

- Use navy to establish hierarchy and orange for the single most important point.
- Use teal, green, purple, blue, and gold only with stable semantic meanings.
- Use no more than three data colors in a normal chart.
- Use pale gray or a light tint of the semantic color for panel fills.
- Avoid shadows, gradients, glass effects, and heavy chart borders.

## 3. Spacing and component rules

- Use approximately 52–58 px outer margins on the 1280 x 720 planning canvas.
- Use a dark title band approximately 96–104 px high for analytical, workflow,
  and options slides.
- Use a pale key-message rail immediately below the title band when the slide
  needs an executive takeaway.
- Use rounded rectangles with thin semantic outlines for grouped content.
- Keep one dominant read: title, key message, then evidence.
- Use 20–28 px internal panel padding and at least 16 px between adjacent panels.
- Keep footers compact and visually subordinate.
- Avoid UI-like card grids when one composition or a clear flow would communicate
  the point more directly.

## 4. Layout archetypes

### Archetype 1 — architecture map

Use for platform architecture, capability maps, or actor/input -> engine ->
execution -> governance -> outcome flows.

Composition:

- centered title and optional subtitle;
- left actor/input rail;
- wide central layered system area;
- narrow governance and outcome rails on the right;
- horizontal foundation rail along the bottom;
- connectors behind nodes with concise labels.

Do not use for a simple list or a two-series chart. Dense architecture belongs on
an overview slide supported by readable detail slides.

### Archetype 2 — current state or evidence assessment

Use for current-state diagnosis, issue vs achievement/gap comparison, KPI
evidence, risk, implication, or impact summaries.

Composition:

- dark title band;
- pale key-message rail with an orange marker;
- one large left evidence zone and two smaller right zones;
- optional bottom impact/outcome strip.

This is the preferred archetype for a single large chart with side commentary.

### Archetype 3 — workflow or proposed solution

Use for multi-step workflows, swimlanes, roles, systems, human-review points,
target operating models, or contribution boundaries.

Composition:

- dark title band;
- numbered horizontal sequence across the top;
- left role/system rail;
- supporting swimlanes through the center;
- horizontal foundation or knowledge layer;
- compact legend and outcome area along the bottom.

Do not compress more than about 11 visible stages. Split the workflow when the
audience needs readable detail.

### Archetype 4 — phased roadmap

Use for delivery plans, timelines, release trains, implementation roadmaps,
gates, deliverables, tuning, and decision points.

Composition:

- dark title band with title and subtitle;
- white timeline field with subtle alternating rows;
- month or phase headers;
- navy delivery bars, gold tuning bars, and gold diamond gates;
- bottom essence or decision strip.

### Archetype 5 — options or investment structure

Use for three-option comparisons, effort/duration/scope ranges, recommendation
framing, and assumptions or exclusions.

Composition:

- dark title band and key-message rail;
- compact component band;
- three aligned option columns;
- one orange recommendation treatment;
- assumptions/exclusions panel along the bottom.

Do not present uncertain estimates as fixed commitments. Label ranges,
assumptions, and exclusions explicitly.

## 5. Chart placement contract

Use the following bounded zones on the 1280 x 720 planning canvas:

| Pattern | Bounded chart zone | Intended use |
| --- | --- | --- |
| Assessment A | x 52–628, y 192–533 | Main chart left with commentary right |
| Assessment B | x 52–1227, y 192–548 | Full-width chart under key message |
| Options A | x 52–1227, y 220–540 | Full-width comparison chart |
| Options B | x 52–840, y 220–540 | Main chart left with recommendation right |

Placement rules:

1. Select one bounded zone and record it in the layout map.
2. Keep title, key-message rail, footer, and slide number outside the zone.
3. Add one native chart with at least 24 px internal padding.
4. Use a source/data note in speaker notes and, when needed, a compact on-slide
   source line below the chart.
5. Render and verify that labels, axes, and callouts remain inside the zone.

If no zone supports the data honestly, use a table, split the content across two
slides, or document a custom chart-ready layout.

## 6. Brand and privacy rules

- Keep the default design system unbranded.
- Add a company or customer logo only from an authentic user-supplied or
  explicitly authorized asset.
- Never create lookalike logos, customer names, proposal titles, pricing, or
  commercial claims as placeholders.
- Do not retain source decks, screenshots, extracted media, or rendered previews
  inside the skill.
- Store temporary inspection files only in a task-specific temporary directory
  and remove them after delivery.
- Never copy example facts or values into a new deck unless they are provided for
  the current request.

## 7. Design-system QA

Before delivery verify:

- every output slide maps to one layout archetype or documents a custom layout;
- the visual tokens and type hierarchy are applied consistently;
- navy establishes hierarchy and orange marks only the main point;
- chart additions stay inside an approved bounded zone;
- all claims and plotted values reconcile to current user-supplied material;
- no confidential or identifying content is retained unintentionally;
- no unresolved placeholders, clipped text, broken connectors, or missing
  authorized brand assets remain in the exported PPTX.
