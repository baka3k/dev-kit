# Shared Expert Council Contract

Rules for any skill that convenes independent experts — a brainstorm panel, a predict persona set, or a future council. It fixes evidence, neutrality, independence, and debate conduct; each skill's playbook keeps its domain content (expert charters, scoring, verdicts, report formats).

## Evidence Ledger

Every packet carries one ledger with stable IDs that findings and ratings cite:

```yaml
evidence:
  verified_facts: [{id: "fact-1", statement: "..."}]
  user_statements: [{id: "user-1", statement: "..."}]
  assumptions: [{id: "assumption-1", statement: "..."}]
  unknowns: [{id: "unknown-1", question: "..."}]
```

- Gather evidence per [retrieval-protocol.md](retrieval-protocol.md); record the retrieval layer and confidence.
- A semantic match is a candidate, not proof; only verified relationships count as facts.
- Every expert finding cites ledger IDs or is explicitly marked as an assumption.
- Record code/document contradictions instead of choosing silently.

## Shared Context Packet

Assemble one packet per run and give the same packet to every expert:

- the ledger above, plus the skill's domain sections (e.g. decision frame, proposal + impact evidence) with the same ID discipline;
- no preferred answer, no draft verdict, no other expert's output, no language that anchors the panel toward one option or one verdict;
- unavailable retrieval is recorded once in the packet's coverage, never retried per expert.

## Independence Contract

- Preferred mode: one expert brief per isolated subagent (isolated forks, same packet, run concurrently). Experts never see each other's output before the debate phase.
- Fallback: when isolated contexts are unavailable, run clearly separated sequential passes, disclose the fallback in the report, and lower confidence. Never describe sequential self-analysis as independent parallel agents.
- The report states the isolation mode actually used.
- Debate inputs are anonymized: experts see findings and summaries, not author identities.

## Brief Rules

Each expert brief states the lens, the packet as the only evidence source, the domain deliverable the skill defines, and these shared constraints:

1. Use only the packet and the code or documents it references.
2. Do not infer or discuss other experts' likely views.
3. Separate facts from assumptions; cite ledger IDs.
4. Do not implement anything.

## Debate Discipline

After independent output, compare anonymized results. Each expert answers, at minimum:

1. What is the strongest reason the current leader or draft consensus is wrong?
2. Which assumption, if false, most likely reverses the ranking or the verdict?
3. What is the strongest case for a rival option or an under-weighted risk?
4. Can the objection be mitigated or tested cheaply? If not, why is it fatal?
5. What evidence, if obtained, would change the outcome?

The moderator consolidates and separates:

- resolved disagreement: evidence or reasoning changed a view;
- persistent value tradeoff: experts hold different legitimate priorities;
- unresolved factual dispute: decisive evidence is missing;
- veto: a hard gate fails.

Revise findings only on evidence or reasoning; record every change and its cause. Never erase persistent dissent or average a failure away. Deeper modes add debate rounds, not new rules.
