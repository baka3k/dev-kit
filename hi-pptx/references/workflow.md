# PPTX Workflow Detail

Step-level detail for `hi-pptx`. The SKILL.md owns gates and resource routing.

## Intake

Confirm or infer only when low-risk: audience and decision makers; meeting objective and expected decision/action; speaking time and likely slide count; language, tone, localization needs; source-of-truth files, data definitions, confidentiality constraints; whether supplied brand assets apply or the deck stays unbranded. Ask only when missing information could materially change claims, data interpretation, branding, or storyline; otherwise proceed with an explicit assumption register.

### 1. Establish the communication job

Write one sentence: by the end, the audience should take an action or reach an understanding because of the central takeaway. Build an evidence map:

- Provided fact: directly traceable to user material.
- Derived statement: faithful synthesis or reproducible calculation.
- Assumption: necessary but unverified; label it.
- Illustrative: fictional example or placeholder; label it visibly.
- Unknown: leave as a question, dependency, or `TBD`.

### 2. Inspect inputs and select the visual system

Inventory all inputs; identify the authoritative version. Run `scripts/analyze_pptx.py` on a user-supplied deck to capture slide size, layouts, fonts, colors, density, object counts. If the user supplies a template, follow it and preserve its master → layout → slide hierarchy. Otherwise use the sanitized system in `references/reference-template.md` as an explicit custom visual direction and build from scratch.

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

Every slide maps to an archetype or documents a reason for a custom layout. Shorten copy, change archetypes, or split content instead of shrinking text or adding unplanned overlays.

### 4. Profile data and select the chart

1. Extract a clean CSV/JSON table without altering source values.
2. Run `scripts/profile_chart_data.py <input> --output <profile.json>`.
3. Review inferred types, missing values, duplicate categories, numeric ranges, totals, suggested chart families.
4. Confirm the intended analytical question and units — a script suggestion is evidence, not an automatic design decision.
5. Read `references/data-visualization.md`; build an editable native chart in an approved chart zone.
6. Reconcile every plotted value and displayed label with the clean table.

If the data cannot support the requested conclusion, say so; use a table, question, or data-gap slide instead of forcing a chart.

### 5. Implement the deck

- JavaScript ES modules and `@oai/artifact-tool`; 16:9 canvas; central design tokens for colors, typography, margins, title bands, key-message rails, panels, footers.
- Build reusable helper functions for the five sanitized archetypes rather than copying confidential slides.
- Keep title and body copy inside the bounded zones in `references/reference-template.md`.
- Native `slide.charts.add(...)` charts only — no Python-PPTX, PptxGenJS, or raster chart screenshots.
- Preserve or add `[Sources]` blocks in speaker notes for non-trivial claims, data, and externally sourced assets.

### 6. Chart quality gates

- Navy `#1F3864` primary series; orange `#F37021` for the single decision-relevant highlight; teal `#127E84` or green `#1E9E54` secondary.
- Prefer direct labels; legend only when direct labeling clutters. Start bar-chart value axes at zero; state any necessary non-zero baseline.
- Avoid 3D, decorative gradients, dual axes, rainbow palettes, tiny labels, many-slice pie/doughnut charts.
- Add units to axes/labels; include source, period, scope, denominator in notes or a compact footer.
- Takeaway title states the computed result, not a generic topic.

### 7. Preflight and visual QA

    python scripts/lint_pptx.py output.pptx --output qa/lint.json
    python scripts/render_pptx.py output.pptx --output-dir qa/rendered --cols 4

1. Review the contact sheet for narrative rhythm, repeated silhouettes, density.
2. Inspect every slide individually at full size.
3. Fix clipping, overflow, awkward wrapping, unintended overlaps, inconsistent footers, broken connectors, unresolved placeholders, chart/data mismatches.
4. Re-render the complete deck after fixes; repeat until clean.

Automated checks are triage, not proof of quality. Never waive a visual defect without inspecting it and recording a valid reason.
