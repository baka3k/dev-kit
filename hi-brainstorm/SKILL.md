---
name: hi-brainstorm
description: Convene an adaptive panel of independent experts to generate competing solutions, challenge assumptions, debate tradeoffs, and select an evidence-backed option with weighted scoring before implementation. Use for ambiguous, consequential, or multi-path decisions; skip trivial work with one obvious reversible solution.
version: 1.0.0
last_updated: 2026-08-19
---

# HI Brainstorm

Run a structured expert council before implementation. The outcome is a decision and handoff, not permission to perform work beyond the user's request.

## Required Input

Establish:

- the problem or decision to make;
- desired outcomes and measurable success criteria;
- constraints and non-negotiables;
- known evidence, affected scope, and candidate options, if any.

Ask a question only when a missing answer could materially change the selected solution. Otherwise state bounded assumptions and lower confidence accordingly.

Modes:

- `quick`: three expert lenses, usually two or three credible options, one rebuttal round;
- `standard` (default): five expert lenses, three to five options, initial and final scoring;
- `deep`: standard mode plus broader evidence gathering, validation experiments, and a second rebuttal round.

## Council Structure

The moderator frames the decision, protects independence, consolidates options, calculates results, and writes the decision. The moderator does not invent a preferred option or silently change expert scores.

Default expert lenses:

1. Domain expert — domain rules, correctness, and context.
2. Systems architect — boundaries, integration, scale, and long-term fit.
3. Delivery engineer — feasibility, complexity, testing, operations, and migration.
4. User/value expert — usefulness, workflow, accessibility, adoption, and time to value.
5. Risk skeptic — hidden assumptions, security, privacy, reliability, compliance, and simpler alternatives.

Adapt or split lenses when specialist knowledge matters, but always retain an explicit skeptic. Read [references/panel-playbook.md](references/panel-playbook.md) when assembling the panel, prompting experts, or formatting the report.

In `quick` mode, choose the three most decision-relevant lenses, always including the risk skeptic and at least one domain or architecture lens. Record which lenses were omitted and the resulting confidence limitation.

## Independence and Delegation

When collaboration agents are available and delegation is allowed, assign one expert brief per subagent. Run experts concurrently or in waves when slots are limited. For initial generation, use isolated forks with no inherited conversation history (for example, `fork_turns: "none"`) and include the same neutral context packet in every brief. No initial expert may receive another expert's conclusions.

If the platform cannot provide isolated agent contexts, perform clearly separated expert passes, disclose the fallback, and lower confidence. Never describe inherited-context or sequential self-analysis as independent parallel agents.

## Workflow

### 1. Frame and Ground

Normalize the goal, success measures, constraints, decision deadline, and evidence gaps. For repository decisions, gather context through the project's prescribed search order. Distinguish verified facts, user statements, and assumptions; do not fabricate missing project context.

### 2. Generate Independently

Each expert proposes at least one solution without seeing the others. Require the mechanism, expected benefits, costs, key assumptions, failure modes, and a falsification test.

### 3. Form the Candidate Set

Merge duplicates but preserve materially different mechanisms. Aim for three to five credible options; if fewer exist, explain why. Mode counts are defaults: never drop a user-mandated candidate merely to meet a count. Include the status quo, containment, or a reversible experiment when credible. Anonymize option origin before evaluation.

Compare options over the same decision horizon and scope. Do not score an architecture, its rollout policy, and a future experiment as peer solutions unless each includes all associated costs and risks. Merge a hybrid or roadmap into its base option when the near-term mechanism is the same; deferred capabilities receive no benefit score until their costs are also counted.

### 4. Apply Hard Gates

Mark an option `fail` regardless of score when it:

- violates a user non-negotiable or verified constraint;
- has an unresolved critical security, safety, privacy, legal, or compliance issue;
- is infeasible under verified technical or operational limits;
- intrinsically depends on an action the user explicitly excludes or cannot authorize.

Lack of authorization to implement after the council is not an option failure; selection never grants that authorization. Use `conditional` when a blocker has a concrete validation or mitigation. Do not average a failed gate away.

### 5. Score Independently

Use a `1`–`5` scale where `1` is unacceptable and `5` is excellent. Default criteria and weights:

| Criterion | Weight | High score means |
|---|---:|---|
| Goal fit | 25 | Directly satisfies the desired outcome |
| Evidence and feasibility | 20 | Supported and realistically implementable |
| Risk and safety | 20 | Low residual risk with credible controls |
| Delivery cost | 15 | Lower effort, complexity, and disruption |
| Maintainability and reversibility | 10 | Easy to own, change, or roll back |
| User value and time to value | 10 | Valuable results arrive quickly and clearly |

Customize weights before scoring when the decision requires it, explain why, and keep the total at `100`. Each score needs a short evidence-based rationale, evidence or assumption identifiers, confidence, and any veto concern. Use `scripts/score_options.py` for deterministic validation and aggregation when there are multiple experts and options.

The weighted score is `sum(weight × median expert rating / 5)`, producing `0`–`100`. Preserve rating dispersion and dissent alongside the median.

### 6. Debate and Rebut

Reveal the anonymized candidate set and initial scorecard. Every expert must:

- state the strongest objection to the leading option;
- identify one assumption or failure scenario that could reverse the ranking;
- steelman at least one competing option;
- propose a mitigation, validation experiment, or reason the concern is fatal.

Revise options only in response to evidence or explicit reasoning. Before final scoring, rerun the same-horizon and material-distinctness check, remove bundled advantages, and merge candidates that differ only by deferred sequencing. Score again independently and record material score changes with their causes.

### 7. Decide

The score informs the decision; it does not replace judgment.

- `SELECT`: top score is at least `75`, leads by at least `5`, passes all gates, and has no unresolved critical objection.
- `CONDITIONAL`: top score is at least `65`, but the lead is narrow, confidence is low, or explicit mitigations/experiments are required.
- `NO DECISION`: every option fails a gate or scores below `65`, decisive information is missing, or a critical conflict remains unresolved.

For a tie, prefer stronger goal fit, then lower residual risk, then greater reversibility, then lower delivery cost. Consensus is not required; preserve principled minority dissent.

### 8. Handoff

Produce the output contract below. If implementation was already authorized in the user's request, pass the selected option and conditions into planning. Otherwise stop at the decision. Never treat council selection as new authorization.

For a high-risk selected change, use `hi-predict` afterward to stress-test that proposal before implementation. `hi-brainstorm` selects among solutions; `hi-predict` evaluates the risk of a proposed change.

## Output Contract

Return:

1. decision (`SELECT`, `CONDITIONAL`, or `NO DECISION`) and confidence;
2. problem frame, success criteria, constraints, facts, and assumptions;
3. panel composition and any fallback used;
4. candidate options with mechanisms and hard-gate status;
5. initial and final scorecards, rank, delta, and important dispersion;
6. strongest objections, rebuttals, mitigations, and unresolved dissent;
7. selected solution and why it wins, or the exact evidence needed to decide;
8. conditions, validation checks, and implementation handoff.

Save a report only when the user requests a persistent artifact; otherwise return it in the conversation.

## Non-Negotiable Rules

- Independent generation happens before cross-reading or debate.
- Compare materially distinct solutions, not cosmetic variants.
- Every rating has evidence or an explicitly marked assumption.
- A critical gate cannot be overruled by voting or a high average.
- The moderator documents score changes, tie-breaks, and dissent.
- Stop with `NO DECISION` instead of manufacturing certainty.
