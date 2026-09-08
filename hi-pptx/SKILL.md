---
name: hi-pptx
description: Create, edit, and visually validate client-ready PowerPoint presentations (.pptx) using a sanitized navy-white-orange-teal design system, with evidence-led storylines, natural executive copy, editable architecture/process/timeline/option layouts, and professional native charts derived from supplied CSV, JSON, spreadsheet, or tabular data. Use for executive proposals, consulting decks, technical architecture, current-state assessments, phased roadmaps, investment options, KPI reviews, and Japanese-customer-facing presentations where visual consistency, quantitative accuracy, privacy, and presentation readiness matter.
---

# Client-ready presentation engine

Create calm, credible executive PowerPoint decks from a sanitized, text-only design specification. Editable PowerPoint elements, including native charts — never flattened screenshots. Do not retain or depend on confidential reference presentations; never invent metrics, quotations, case studies, customer claims, or sources.

## Required resources

Read only what the request needs:

- Always: `references/reference-template.md` — design tokens, layout archetypes, placement rules.
- Storyline/copy: `references/writing-and-storyline.md`.
- Any numeric data, KPIs, charts: `references/data-visualization.md`.
- Before final QA: `references/quality-review.md`.
- Step detail: `references/workflow.md`.

## Non-negotiable outcomes

- Define audience, decision, and central takeaway before selecting layouts; one narrative job and a conclusion-led title per slide.
- Preserve source meaning; distinguish facts, calculations, assumptions, illustrative examples, and unknowns; external sources and calculations go in speaker notes.
- Navy-white base, orange emphasis, restrained teal/green/purple/blue/gold support; select from the five sanitized archetypes (architecture, current-state assessment, workflow, phased roadmap, options) before inventing a composition.
- Authentic brand assets only when user-supplied or authorized. Keep charts, tables, diagrams, timelines editable.
- Compute first, design second: validate units, denominators, time grain, missing values, sorting, totals, rounding before charting; chart from the analytical question, highlight one decision-relevant series.
- Never declare completion before rendering and inspecting every slide.

## Workflow

Detail per [workflow.md](references/workflow.md):

1. Communication job + evidence map.
2. Inspect inputs; template or sanitized visual system.
3. Narrative and layout map (one row per slide).
4. Profile data; select chart from the question.
5. Implement: `@oai/artifact-tool`, 16:9, design tokens, native charts.
6. Chart quality gates (colors, direct labels, zero baselines, units).
7. Preflight: `scripts/lint_pptx.py` + `scripts/render_pptx.py` contact sheet; inspect every slide; fix and re-render until clean.

Scripts (run from the skill directory): `analyze_pptx.py`, `profile_chart_data.py`, `lint_pptx.py`, `render_pptx.py`.

## Deliverables

Final `.pptx`; short summary of storyline, archetypes, chart choices; unresolved assumptions and editable placeholders; contact sheet only when it helps review.
