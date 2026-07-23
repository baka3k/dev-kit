---
name: hi-pptx
description: Create, edit, and visually validate calm, credible, client-ready PowerPoint presentations (.pptx) from notes, technical material, reports, proposals, or existing decks. Use for executive summaries, consulting proposals, workshops, assessments, technology and architecture narratives, roadmaps, account plans, and Japanese-customer-facing presentations where storyline, evidence discipline, natural human editorial judgment, and presentation readiness matter.
---

# Craft Client PPTX

Create presentations that are clear in a meeting, credible under client scrutiny, and visually composed without looking machine-generated.

## Non-negotiable outcome

- Preserve source meaning and distinguish facts, assumptions, and illustrative content.
- Give every slide one purpose and one audience takeaway.
- Prefer clarity, logic, and speaking flow over decoration.
- Keep the visual system consistent while varying layouts intentionally.
- Never invent metrics, cases, quotations, customer claims, or sources.
- Never declare completion before rendering and visually inspecting every slide.

## Intake

Confirm or infer only when low-risk:

1. Audience and decision makers.
2. Meeting objective and expected outcome.
3. Speaking time and likely slide count.
4. Language, tone, and localization needs.
5. Source-of-truth materials and confidentiality constraints.
6. Brand, template, or existing-deck requirements.

Ask for missing information when it could materially change the storyline or claims. Otherwise, proceed with a clearly labeled assumption register.

## Evidence discipline

Build a working evidence map before drafting:

- **Provided fact**: traceable to user material.
- **Derived statement**: a faithful synthesis of provided facts.
- **Assumption**: necessary for planning; label and request confirmation.
- **Illustrative**: fictional example or placeholder; label visibly.
- **Unknown**: do not fill. Turn it into a question, dependency, or `TBD`.

Do not turn an assumption into an asserted fact. Keep source references in speaker notes or a final source slide when the user supplies them.

## Workflow

### 1. Inspect inputs

- Inventory all source files and identify the authoritative version.
- For an existing `.pptx`, inspect slide count, size, masters, layouts, fonts, colors, and content density.
- Run `scripts/analyze_pptx.py` when a deck or template is supplied.
- Preserve confidentiality; extract reusable principles rather than copying identifying content.

### 2. Build the storyline before design

Write a slide plan containing:

| Field          | Required content                                                |
| -------------- | --------------------------------------------------------------- |
| Slide purpose  | Why the slide exists                                            |
| Takeaway title | The conclusion or question the audience should retain           |
| Evidence       | Facts, visuals, or explicit assumptions supporting the takeaway |
| Layout intent  | The simplest visual structure for the content                   |
| Transition     | Why the next slide follows                                      |

Use the decision-backward method in [writing-and-storyline.md](references/writing-and-storyline.md). Remove slides that do not advance the conversation.

### 3. Select a controlled style

Choose one primary style and, at most, one secondary style:

- **Executive Minimal** for decisions, summaries, and proposals.
- **Consulting Clean** for assessments, workshops, comparisons, and recommendations.
- **Technology Narrative** for architecture, cloud, AI, and enterprise solutions.
- **Japanese Customer Friendly** for calm, contextual, risk-transparent customer communication.

Read [design-system.md](references/design-system.md) for tokens, layout patterns, typography, and style-specific rules.

### 4. Create or edit the deck

For a new deck:

- Use the available presentation-generation toolchain.
- Prefer editable native PowerPoint text, shapes, tables, and charts.
- Use PptxGenJS with an HTML-to-PowerPoint workflow when available for precise layout.
- Use `python-pptx` for deterministic, simple layouts when it is the more reliable option.
- Use 16:9 unless the user or template requires another ratio.

For an existing deck:

- Preserve slide masters, layouts, theme relationships, notes, and brand assets.
- Use targeted OOXML edits when a library cannot preserve required features.
- Modify only slides and elements in scope.
- Re-run validation after structural edits.

Do not flatten editable diagrams into screenshots unless fidelity requires it and the user accepts the tradeoff.

### 5. Preflight

Run:

```bash
python scripts/lint_pptx.py output.pptx --output qa/lint.json
python scripts/render_pptx.py output.pptx --output-dir qa/rendered --cols 4
```

Treat automated checks as triage, not proof of quality.

### 6. Review every rendered slide

Review both:

- The contact sheet for narrative rhythm, repetition, density, and visual pacing.
- Each full-size slide for overflow, clipping, alignment, spacing, contrast, readability, chart clarity, and awkward line breaks.

Use [quality-review.md](references/quality-review.md). Fix issues, re-render the entire deck, and repeat until clean.

### 7. Deliver

Provide:

- The final `.pptx`.
- A short summary of storyline and style choices.
- Any unresolved assumptions, missing evidence, or editable placeholders.
- The render/contact sheet when useful for review.

## Natural, human editorial standard

- Write specific takeaway titles; avoid generic slogans and inflated claims.
- Vary layout according to content, not for novelty.
- Allow controlled asymmetry, different column ratios, and occasional quiet slides.
- Use one strong visual hierarchy instead of many decorative accents.
- Keep clean white or near-white surfaces dominant; avoid large saturated accent panels and uninterrupted color slabs.
- Use dark, projection-safe text and clearly visible support lines; do not rely on pale gray or low-contrast accents for structure.
- When no client brand is supplied, use the reference-derived role palette in `design-system.md` instead of generic Office theme colors.
- Use only a slight corner radius on cards and panels; reserve pill shapes for intentional tags or status badges.
- Keep repeated components aligned but avoid cloning every slide.
- Use concrete nouns and verbs. Remove filler, repetition, and marketing gloss.
- Prefer one diagram with a clear reading path over a dense “everything map.”
- Use icons only when they improve scanning; keep one icon family and stroke style.
- Use photographs only when they are authentic, relevant, licensed, and compositionally useful.
- Keep caveats, risks, dependencies, and next steps visible when they matter.

## Content limits

- Aim for one message per slide.
- Prefer 15–18 pt body text; use smaller text only for labels or citations.
- Keep most slides below roughly 80 words.
- Break dense architecture, roadmap, and matrix content into overview/detail sequences.
- Avoid more than 3–5 peer items on one slide unless the audience must compare them.
- Never use a quote layout without an actual attributed quote.

## Bundled resources

- `references/design-system.md`: four styles, typography, color, layout, and sample-derived principles.
- `references/writing-and-storyline.md`: narrative planning, title writing, evidence language, and localization.
- `references/quality-review.md`: automated and visual completion gates.
- `scripts/analyze_pptx.py`: inspect a deck without reproducing its confidential text.
- `scripts/lint_pptx.py`: flag probable overflow, out-of-bounds objects, tiny text, density, and text-on-text collisions.
- `scripts/render_pptx.py`: render all slides and build a contact sheet.
- `scripts/create_smoke_test.py`: generate a fictional deck used to test this skill.

## Example invocations

- “Use `$craft-client-pptx` to turn these workshop notes into a 12-minute Consulting Clean proposal for a Japanese manufacturing client.”
- “Use `$craft-client-pptx` to simplify this architecture deck into a customer-facing Technology Narrative. Do not change any facts.”
- “Use `$craft-client-pptx` to edit this executive review deck, tighten the storyline, and return a fully rendered, visually checked `.pptx`.”
