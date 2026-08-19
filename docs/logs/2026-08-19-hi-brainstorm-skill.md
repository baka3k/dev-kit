# Expert-Council Brainstorming Skill — 2026-08-19

## Context

A reusable pre-implementation workflow was needed for ambiguous decisions where several credible solutions should be generated independently, challenged by specialists, and compared before work begins. The existing `hi-predict` workflow evaluates the risk of an already-proposed change; it did not own solution generation and selection (`hi-brainstorm/SKILL.md:120`).

## Change

Added `hi-brainstorm` with quick, standard, and deep council modes; five default expert lenses; independent proposal generation; hard gates; evidence-backed weighted scoring; rebuttal; and explicit `SELECT`, `CONDITIONAL`, or `NO DECISION` outcomes (`hi-brainstorm/SKILL.md:23`, `hi-brainstorm/SKILL.md:31`, `hi-brainstorm/SKILL.md:67`, `hi-brainstorm/SKILL.md:95`, `hi-brainstorm/SKILL.md:106`). Added a panel playbook and decision-report template that preserve objections, uncertainty, and minority dissent (`hi-brainstorm/references/panel-playbook.md:156`, `hi-brainstorm/references/panel-playbook.md:176`). Added a deterministic scorer that validates evidence, weights, minimum expert coverage, gates, and veto consistency, then aggregates median ratings and ranks eligible options (`hi-brainstorm/scripts/score_options.py:78`, `hi-brainstorm/scripts/score_options.py:129`, `hi-brainstorm/scripts/score_options.py:197`, `hi-brainstorm/scripts/score_options.py:218`, `hi-brainstorm/scripts/score_options.py:235`). Registered the skill for agent discovery and in the public README catalog (`hi-brainstorm/agents/openai.yaml:1`, `README.md:154`).

## Impact

Risk level: **medium**. The change adds no application-runtime behavior, but it can influence consequential implementation decisions. Independent generation, non-overridable hard gates, evidence-linked ratings, explicit dissent, and no-decision thresholds reduce false consensus and arithmetic drift (`hi-brainstorm/SKILL.md:55`, `hi-brainstorm/SKILL.md:69`, `hi-brainstorm/SKILL.md:108`, `hi-brainstorm/SKILL.md:137`). Users and agents can now compare materially distinct approaches reproducibly before handing an authorized choice into planning.

## Decision

A new skill was chosen instead of extending `hi-predict`: brainstorming owns divergent option generation, debate, and selection, while `hi-predict` remains a focused downstream stress test for a selected high-risk proposal (`hi-brainstorm/SKILL.md:118`). This keeps each workflow's trigger and verdict semantics clear while allowing them to compose.

A deterministic scorer was chosen instead of prose-only scoring. Prose would be simpler, but would make weight totals, evidence references, medians, dispersion, gate failures, vetoes, ties, and ranking vulnerable to inconsistent arithmetic or omission. The scorer validates those invariants while leaving final judgment and dissent with the council (`hi-brainstorm/SKILL.md:91`, `hi-brainstorm/SKILL.md:108`, `hi-brainstorm/references/panel-playbook.md:154`).

## References

- commit: 2fa7d551a428f577029f0f16576d7447da149cff
