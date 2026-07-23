# Quality Review

## Completion gate

Do not mark a deck complete until all items pass:

1. The `.pptx` opens successfully.
2. Automated lint has no unresolved errors.
3. Every slide has been rendered.
4. The contact sheet has been reviewed for narrative rhythm.
5. Every full-size slide has been inspected.
6. All corrections have been followed by a full re-render.

## Automated preflight

Run:

```bash
python scripts/analyze_pptx.py output.pptx --output qa/analysis.json
python scripts/lint_pptx.py output.pptx --output qa/lint.json
python scripts/render_pptx.py output.pptx --output-dir qa/rendered --cols 4
```

`lint_pptx.py` uses heuristics. Investigate its findings; do not blindly modify intentional overlaps or small citations.

## Contact-sheet review

Check:

- Does the story have a visible beginning, middle, and end?
- Are section changes clear?
- Is there enough variation without visual noise?
- Are several consecutive slides too dense?
- Does the same card grid repeat mechanically?
- Are the most important slides visually prominent?
- Does the final slide clearly support the expected outcome?

## Full-size slide review

### Content

- Title states the takeaway.
- Claims are traceable or labeled.
- Terms, abbreviations, units, dates, and capitalization are consistent.
- No confidential or identifying material is carried over unintentionally.
- No placeholder, sample, or `TBD` remains unless intentionally disclosed.

### Typography

- No clipping or awkward line breaks.
- Body text is readable at presentation distance.
- Font family and hierarchy are consistent.
- Bold, color, and capitalization are purposeful.
- Japanese glyphs render correctly when used.

### Layout

- No text or objects cross slide boundaries.
- No unintended overlaps.
- Margins, alignment, and card spacing are clean.
- Content does not feel vertically or horizontally cramped.
- The reading order is obvious.
- Icons and images are aligned and have consistent treatment.

### Color and accessibility

- Text/background contrast is sufficient.
- Accent colors communicate hierarchy rather than decoration.
- Color is not the only signal.
- Charts and diagrams remain understandable when projected.

### Charts and diagrams

- Title explains the point, not the chart type.
- Units, axes, periods, and sources are visible.
- Labels do not collide.
- Architecture arrows have explicit meaning.
- The main reading path is clear in under five seconds.
- Detail belongs in an appendix if it cannot remain legible.

## Naturalness review

Remove or revise:

- Generic claims and “AI-style” slogans.
- Repeated sentence structures.
- Identical layouts used without content justification.
- Over-polished marketing copy unsupported by evidence.
- Decorative icons, gradients, glows, and stock imagery.
- Repetition of the same point in title, subtitle, and bullets.

Keep:

- Specific language.
- Visible assumptions and constraints.
- Controlled asymmetry.
- Quiet slides between dense analytical slides.
- Small, purposeful variations in composition.
- A clear human point of view grounded in the supplied material.
