---
name: hi-pptx
description: Create, edit, and visually validate client-ready PowerPoint presentations (.pptx) using a sanitized navy-white-orange-teal design system, with evidence-led storylines, natural executive copy, editable architecture/process/timeline/option layouts, and professional native charts derived from supplied CSV, JSON, spreadsheet, or tabular data. Use for executive proposals, consulting decks, technical architecture, current-state assessments, phased roadmaps, investment options, KPI reviews, and Japanese-customer-facing presentations where visual consistency, quantitative accuracy, privacy, and presentation readiness matter.
---

# Client-ready presentation engine

Create calm, credible executive PowerPoint decks from a sanitized, text-only
design specification. Use editable PowerPoint elements, including native charts,
rather than flattened screenshots. Do not retain or depend on confidential
reference presentations.

## Required resources

Read only the resources needed for the request:

- Always read `references/reference-template.md` for the sanitized design tokens,
  layout archetypes, and placement rules.
- Read `references/writing-and-storyline.md` for audience, storyline, titles,
  evidence language, and the anti-buzzword voice gate.
- Read `references/data-visualization.md` whenever numeric data, KPIs, charts,
  comparisons, trends, distributions, or forecasts are involved.
- Read `references/quality-review.md` before final QA.

No original reference deck or rendered preview is bundled. Do not search for,
reconstruct, or reuse confidential source content. Use only the sanitized rules
documented in this skill and assets explicitly supplied for the current request.

## Non-negotiable outcomes

Story and evidence:

- Define the audience, decision, and central takeaway before selecting layouts.
- Give every slide one narrative job and a conclusion-led title.
- Preserve source meaning and distinguish provided facts, calculations,
  assumptions, illustrative examples, and unknowns.
- Never invent metrics, quotations, case studies, customer claims, or sources.
- Put external sources and calculation definitions in speaker notes.

Visual system:

- Use the navy-white base with orange emphasis and restrained teal, green,
  purple, blue, or gold support colors.
- Select from five sanitized layout archetypes before inventing a new
  composition: architecture, current-state assessment, workflow, phased roadmap,
  and options.
- Apply consistent typography, spacing, headers, footers, alignment, and panel
  geometry from `references/reference-template.md`.
- Use authentic brand assets only when the user supplies or authorizes them.
- Keep charts, tables, diagrams, and timelines editable.

Data integrity:

- Compute first, design second. Validate units, denominators, time grain, missing
  values, sorting, totals, and rounding before charting.
- Choose a chart from the analytical question, not decoration preference.
- Highlight one decision-relevant series or point; keep the rest subordinate.
- Never declare completion before rendering and inspecting every slide.

## Intake

Confirm or infer only when low-risk:

1. Audience and decision makers.
2. Meeting objective and expected decision or action.
3. Speaking time and likely slide count.
4. Language, tone, and localization needs.
5. Source-of-truth files, data definitions, and confidentiality constraints.
6. Whether supplied brand assets should be applied or the deck should remain
   unbranded.

Ask only when missing information could materially change claims, data
interpretation, branding, or storyline. Otherwise proceed with an explicit
assumption register.

## Workflow

### 1. Establish the communication job

Write one sentence in the form: by the end, the audience should take an action or
reach an understanding because of the central takeaway. Build an evidence map:

- Provided fact: directly traceable to user material.
- Derived statement: faithful synthesis or reproducible calculation.
- Assumption: necessary but unverified; label it.
- Illustrative: fictional example or placeholder; label it visibly.
- Unknown: leave as a question, dependency, or `TBD`.

### 2. Inspect inputs and select the visual system

- Inventory all inputs and identify the authoritative version.
- Run `scripts/analyze_pptx.py` on a user-supplied deck to capture slide size,
  layouts, fonts, colors, density, and object counts.
- If the user supplies a template, follow that template and preserve its
  master -> layout -> slide hierarchy.
- Otherwise use the sanitized system in `references/reference-template.md` as an
  explicit custom visual direction and build the deck from scratch.

### 3. Plan the narrative and layout map

For every output slide define:

| Field | Required content |
| --- | --- |
| Narrative job | Why the slide exists |
| Takeaway title | The conclusion the audience should retain |
| Evidence | Facts, calculations, visuals, or explicit assumptions |
| Layout archetype | Architecture, assessment, workflow, roadmap, or options |
| Content zones | Exact bounded areas for text, charts, tables, or diagrams |
| Transition | Why the next slide follows |

Every output slide must map to an archetype or document a reason for a custom
layout. Shorten copy, change archetypes, or split the content instead of shrinking
text or adding unplanned overlays.

### 4. Profile data and select the chart

When tabular data is supplied:

1. Extract a clean CSV or JSON table without altering source values.
2. Run `scripts/profile_chart_data.py <input> --output <profile.json>`.
3. Review inferred types, missing values, duplicate categories, numeric ranges,
   totals, and suggested chart families.
4. Confirm the intended analytical question and units. A script suggestion is
   evidence for selection, not an automatic design decision.
5. Read `references/data-visualization.md` and build an editable native chart in
   an approved chart zone.
6. Reconcile every plotted value and displayed label with the clean table.

If the data cannot support the requested conclusion, say so and use a table,
question, or data-gap slide instead of forcing a chart.

### 5. Implement the deck

- Use JavaScript ES modules and `@oai/artifact-tool` for PowerPoint authoring.
- Use a 16:9 canvas and central design tokens for colors, typography, margins,
  title bands, key-message rails, panels, and footers.
- Build reusable helper functions for the five sanitized archetypes rather than
  copying confidential slides.
- Keep title and body copy inside the bounded zones documented in
  `references/reference-template.md`.
- Use native `slide.charts.add(...)` charts. Do not use Python-PPTX, PptxGenJS,
  or raster chart screenshots for authoring.
- Preserve or add `[Sources]` blocks in speaker notes for non-trivial claims,
  data, and externally sourced assets.

### 6. Apply chart quality gates

- Use navy `#1F3864` for the primary series, orange `#F37021` for the single
  decision-relevant highlight, and teal `#127E84` or green `#1E9E54` for a
  secondary series.
- Prefer direct labels. Use a legend only when direct labeling would clutter.
- Start bar-chart value axes at zero. State any necessary non-zero baseline.
- Avoid 3D, decorative gradients, dual axes, rainbow palettes, tiny labels, and
  pie/doughnut charts with many slices.
- Add units to axes or labels and include source, period, scope, and denominator
  in notes or a compact footer.
- Use a takeaway title that states the computed result, not a generic topic.

### 7. Preflight and visual QA

Run the bundled checks from the skill directory:

    python scripts/lint_pptx.py output.pptx --output qa/lint.json
    python scripts/render_pptx.py output.pptx --output-dir qa/rendered --cols 4

Then:

1. Review the generated contact sheet for narrative rhythm, repeated silhouettes,
   and density.
2. Inspect every slide individually at full size.
3. Fix clipping, overflow, awkward wrapping, unintended overlaps, inconsistent
   footers, broken connectors, unresolved placeholders, and chart/data mismatches.
4. Re-render the complete deck after fixes and repeat until clean.

Automated checks are triage, not proof of quality. Do not waive a visual defect
without inspecting it and recording a valid reason.

## Deliverables

Return:

- The final `.pptx`.
- A short summary of storyline, layout archetypes, and chart choices.
- Any unresolved assumptions, missing evidence, or editable placeholders.
- The generated contact sheet only when it helps the user review the deck.

## Bundled resources

- `references/reference-template.md`: sanitized design tokens, layout archetypes,
  placement rules, and bounded chart zones.
- `references/data-visualization.md`: question-to-chart routing, native chart
  recipes, statistical integrity, and QA.
- `references/writing-and-storyline.md`: executive narrative and natural copy.
- `references/quality-review.md`: voice, visual, privacy, and completion gates.
- `scripts/profile_chart_data.py`: profile CSV/JSON and suggest chart families.
- `scripts/analyze_pptx.py`: inspect structure without reproducing slide text.
- `scripts/lint_pptx.py`: flag layout, density, type, and writing issues.
- `scripts/render_pptx.py`: render every slide and build a contact sheet.

## Example invocations

- “Use `$hi-pptx` to turn this assessment into a six-slide client proposal. Keep
  the facts unchanged and do not retain confidential inputs.”
- “Use `$hi-pptx` to chart this CSV, explain the strongest trend, and create an
  executive KPI review with editable native PowerPoint charts.”
- “Use `$hi-pptx` to build a technical architecture and phased roadmap using the
  sanitized corporate visual system.”
