# Quality Review

## Completion gate

Do not mark a deck complete until all items pass:

1. The `.pptx` opens successfully.
2. Automated lint has no unresolved errors.
3. Every lint warning — including banned-phrase, long-title, and wordy-block
   findings — is resolved or explicitly justified.
4. Every slide has been rendered.
5. The contact sheet has been reviewed for narrative rhythm.
6. Every full-size slide has been inspected.
7. The voice gate and the template-fidelity gate below both pass.
8. All corrections have been followed by a full re-render.

## Automated preflight

Run:

```bash
python scripts/analyze_pptx.py output.pptx --output qa/analysis.json
python scripts/lint_pptx.py output.pptx --output qa/lint.json
python scripts/render_pptx.py output.pptx --output-dir qa/rendered --cols 4
```

`lint_pptx.py` uses heuristics. Investigate its findings; do not blindly
modify intentional overlaps or small citations. Banned-phrase findings are
different: they are almost never intentional and must be rewritten, not
waived.

## Voice gate (anti-AI copy check)

Scan every title and body block, in the deck's language:

- No word from the forbidden lists in `writing-and-storyline.md` §1 — in any
  language, with or without diacritics.
- Headlines read as conclusions or observations, not category labels.
- Titles fit on one line in the selected layout title box; body blocks stay
  concise enough for their bounded content zones.
- Sentence lengths vary; no bullet list is a cloned skeleton (all bullets
  opening with the same part of speech).
- No sentence that could appear unchanged in any deck for any client.
- Quotes have real attributions; hero numbers trace to evidence or carry an
  explicit label.

## Template-fidelity gate

Check on every slide:

- The primary read is obvious: title, key message, then evidence.
- Navy establishes hierarchy; orange marks only the main decision-relevant
  point; teal/green/purple/blue/gold retain consistent semantic roles.
- The slide maps visibly to one sanitized layout archetype from
  `reference-template.md`.
- Title bars, key-message rails, footers, page markers, alignment, corner radii,
  and spacing follow the selected archetype unless the layout map documents a
  deliberate change.
- Comparisons use no more than three main options and highlight at most one
  recommendation.
- New charts remain inside an approved bounded chart zone and do not cover title,
  key-message, or footer furniture.
- On light slides, primary text remains navy or near-black and secondary text
  remains dark enough for projector use; white text is reserved for dark navy,
  teal, green, purple, or orange fields with sufficient contrast.

## Contact-sheet review

Check:

- Does the story have a visible beginning, middle, and end?
- Are section changes clear?
- Is there enough variation without visual noise?
- Are several consecutive slides too dense?
- Does the same composition repeat mechanically?
- Are the most important slides visually prominent?
- Does accent placement vary enough to stay striking, or has it become
  wallpaper?
- Does the final slide clearly support the expected outcome?

## Full-size slide review

### Content

- Title states the takeaway and remains on one line in the selected title box.
- Claims are traceable or labeled.
- Terms, abbreviations, units, dates, and capitalization are consistent.
- No confidential or identifying material is carried over unintentionally.
- No placeholder, sample, or `TBD` remains unless intentionally disclosed.

### Typography

- No clipping or awkward line breaks.
- Title and primary evidence are visibly dominant; body text remains readable at
  presentation distance without violating the defined type hierarchy.
- Font family and hierarchy are consistent; rendered fonts match intent (no
  silent substitution).
- Bold, color, and capitalization are purposeful.
- Japanese and Vietnamese glyphs render correctly when used.

### Layout

- No text or objects cross slide boundaries.
- No unintended overlaps.
- Margins, alignment, and card spacing are clean.
- Content does not feel vertically or horizontally cramped.
- The reading order is obvious and reaches the hero first.
- Icons and images are aligned and have consistent treatment.

### Color and accessibility

- Text/background contrast is sufficient (≥ 4.5:1 for reading text).
- Accents below 4.5:1 on the light canvas (emerald, burnt orange) appear
  only at hero size or as graphics.
- Color is not the only signal.
- Light decks remain legible on bright projectors (wash-out simulation).

### Charts and diagrams

- Title explains the point, not the chart type.
- Units, axes, periods, and sources are visible.
- Labels do not collide.
- One accent series; context series muted.
- The main reading path is clear in under five seconds.
- Detail belongs in an appendix if it cannot remain legible.

## Naturalness review

Remove or revise:

- Generic claims, slogans, and any surviving AI buzzword.
- Repeated sentence structures and cloned bullet skeletons.
- Identical layouts used without content justification.
- Over-polished marketing copy unsupported by evidence.
- Decorative icons, gradients, glows (except the single featured tile), and
  stock imagery.
- Repetition of the same point in title, subtitle, and bullets.
- A second focal point fighting the hero.

Keep:

- Specific language and concrete numbers.
- Visible assumptions and constraints.
- Controlled asymmetry (50/50 vs 40/60 splits).
- Quiet slides between dense analytical slides.
- Small, purposeful variations in composition.
- A clear human point of view grounded in the supplied material.
