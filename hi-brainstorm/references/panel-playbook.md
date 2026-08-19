# Expert Council Playbook

Use this reference to assemble the panel, issue isolated briefs, run rebuttals, and format the final decision.

## Shared Context Packet

Give every expert the same neutral packet:

```yaml
decision:
  problem: "What must be solved or decided"
  desired_outcomes: []
  success_measures: []
  constraints: []
  non_negotiables: []
  deadline: "optional"
scope:
  affected_users: []
  affected_systems: []
evidence:
  verified_facts: [{id: "fact-1", statement: "..."}]
  user_statements: [{id: "user-1", statement: "..."}]
  assumptions: [{id: "assumption-1", statement: "..."}]
  unknowns: [{id: "unknown-1", question: "..."}]
candidate_options_from_user: []
```

Do not include a preferred answer, another expert's output, or language that anchors the panel toward one solution.

## Expert Charters

### Domain Expert

Focus on domain rules, semantic correctness, policy, edge conditions, and precedents. Ask what a technically elegant solution could misunderstand about the actual problem.

### Systems Architect

Focus on component boundaries, dependencies, data flow, compatibility, scaling, and the cost of future change. Ask whether the solution fits the existing system or creates avoidable coupling.

### Delivery Engineer

Focus on implementation path, testability, observability, rollout, migration, operations, team capability, and realistic effort. Ask what will fail during delivery or ownership.

### User/Value Expert

Focus on user outcomes, workflow, accessibility, adoption, support burden, and time to value. Ask whether users receive a clear improvement and how success will be observed.

### Risk Skeptic

Focus on false assumptions, security, privacy, reliability, compliance, abuse, reversibility, and the cost of doing nothing. Must propose a simpler option and challenge at least one core assumption.

Replace a default lens with a more relevant specialist—such as security, data, legal, finance, or operations—when that expertise is decisive. Record the substitution and rationale.

## Independent Expert Brief

```text
You are the <EXPERT LENS> on an expert decision council.

Using only the shared context packet and available evidence:
1. Restate the problem from your lens without selecting a favorite prematurely.
2. Propose one or two materially distinct solutions.
3. For each solution, explain mechanism, benefits, costs, dependencies,
   assumptions, failure modes, and a falsification test.
4. Identify missing evidence and distinguish facts from assumptions.
5. Do not infer or discuss other experts' likely views.

Return concise structured findings. Do not implement anything.
```

## Candidate Record

The moderator consolidates independent proposals into records like:

```yaml
id: option-a
name: "Short neutral name"
mechanism: "How it works"
expected_outcomes: []
costs_and_tradeoffs: []
dependencies: []
assumptions: []
failure_modes: []
validation_test: "What evidence would falsify or support it"
gate:
  status: "pass|conditional|fail"
  reasons: []
```

Merge only solutions with the same mechanism and material tradeoffs. Keep variations separate when they change risk, reversibility, cost, or user outcome within the decision horizon. A rollout sequence, optional future stage, or validation experiment is not a separate peer solution when its near-term mechanism matches another option. Never award future optionality without charging its implementation and operational costs.

## Scoring Discipline

Score anonymized options independently. Ratings mean:

| Rating | Meaning |
|---:|---|
| 1 | Unacceptable or contradicted by evidence |
| 2 | Major weaknesses; unlikely to meet the criterion |
| 3 | Viable with meaningful tradeoffs or uncertainty |
| 4 | Strong; minor or manageable weaknesses |
| 5 | Excellent and well supported |

For every rating, capture a structured record:

- one-sentence rationale;
- evidence or assumption identifiers;
- confidence: `high`, `medium`, or `low`;
- a veto-level concern as a concrete string, or `null`.

A veto requires the option gate to be `conditional` or `fail`; it cannot coexist with a `pass` gate.

Run the deterministic scorer with a JSON file:

```bash
python3 <skill-dir>/scripts/score_options.py scorecard.json --format markdown
```

Input schema:

The compact example below uses two criteria. Use the six default criteria from `SKILL.md` unless the council explicitly customizes and explains the weights.

```json
{
  "evidence_registry": [
    {"id": "fact-1", "kind": "fact", "text": "The required outcome is documented"},
    {"id": "assumption-2", "kind": "assumption", "text": "The mitigation is technically available"},
    {"id": "fact-3", "kind": "fact", "text": "The edge case is in scope"},
    {"id": "fact-4", "kind": "fact", "text": "The residual risk has an owner"}
  ],
  "criteria": [
    {"id": "goal_fit", "label": "Goal fit", "weight": 60},
    {"id": "risk_safety", "label": "Risk and safety", "weight": 40}
  ],
  "options": [
    {
      "id": "option-a",
      "name": "Example option",
      "gate": {"status": "pass", "reasons": []},
      "ratings": {
        "domain": {
          "goal_fit": {"rating": 4, "rationale": "Meets the core outcome", "evidence_ids": ["fact-1"], "confidence": "high", "veto": null},
          "risk_safety": {"rating": 3, "rationale": "One mitigation is untested", "evidence_ids": ["assumption-2"], "confidence": "medium", "veto": null}
        },
        "skeptic": {
          "goal_fit": {"rating": 3, "rationale": "Misses one edge case", "evidence_ids": ["fact-3"], "confidence": "medium", "veto": null},
          "risk_safety": {"rating": 3, "rationale": "Residual risk is bounded", "evidence_ids": ["fact-4"], "confidence": "medium", "veto": null}
        }
      }
    }
  ]
}
```

A criterion may omit one expert's rating, but at least two expert ratings are required per criterion. Every referenced evidence ID must resolve to the top-level registry, whose `kind` is `fact`, `user_statement`, `assumption`, or `unknown`. The script validates and preserves rating evidence, then reports median ratings, ranges, weighted totals, gate status, vetoes, and rank. Gate failures remain visible but are excluded from ranking. Substantively tied options share a rank; IDs are used only for stable display order.

## Rebuttal Round

Give experts the anonymized options and initial score summary, not author identities. Ask each expert:

1. What is the strongest reason the current leader should not be selected?
2. Which assumption would most likely reverse the ranking?
3. What is the strongest case for a lower-ranked option?
4. Can the objection be mitigated or tested cheaply? If not, why is it fatal?
5. Which ratings should change, and what new evidence or reasoning justifies each change?
6. Are any candidates the same near-term solution with a roadmap or optional stage receiving unearned benefit?

The moderator separates:

- resolved disagreement: evidence or reasoning changed a view;
- persistent value tradeoff: experts use different legitimate priorities;
- unresolved factual dispute: decisive evidence is missing;
- veto: a hard gate fails.

Never erase persistent dissent merely because the median is stable.

## Decision Report Template

```markdown
# Brainstorm Decision: <topic>

## Decision
- Verdict: SELECT | CONDITIONAL | NO DECISION
- Selected option: <id/name or none>
- Confidence: high | medium | low
- One-sentence rationale: <why>

## Decision Frame
- Desired outcomes:
- Success measures:
- Constraints and non-negotiables:
- Verified facts:
- Assumptions and unknowns:

## Council
| Lens | Specialist | Confidence | Notes |
|---|---|---|---|

## Options and Gates
| Option | Mechanism | Gate | Key condition |
|---|---|---|---|

## Final Scorecard
| Rank | Option | Initial | Final | Delta | Gate | Dispersion |
|---:|---|---:|---:|---:|---|---|

## Debate
| Topic | Strongest objection | Rebuttal/mitigation | Resolution |
|---|---|---|---|

## Dissent and Uncertainty
- Minority view:
- Evidence that could reverse the decision:
- Residual risks:

## Handoff
- Selected mechanism and boundaries:
- Required validations/conditions:
- Acceptance measures:
- Next authorized step:
```

If the verdict is `NO DECISION`, replace the handoff with the smallest concrete evidence-gathering step, its owner if known, and the decision rule for reconvening.
