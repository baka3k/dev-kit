---
name: typesafe-ai
license: MIT
description: >
  Build AI-powered software with TypeSafe: System One models (flagship Jev)
  turn natural language and app state into typed judgments and probabilities
  composed in code. Use when a feature needs programmable common sense, when
  brainstorming what AI could make possible, or when a prompt-and-parse step
  could become a structured decision. Minimal query recipe: reference.md.
---

# Build with TypeSafe

System One models (Jev) return fast typed judgments with probabilities — not
generated text or reasoning. Code owns the workflow; the model adds semantic
common sense.

## Docs — source of truth; read as part of the task

- Index: https://docs.typesafe.ai/llms.txt. Fetch pages by appending `.md`; resolve relative links against https://docs.typesafe.ai. If Markdown fails, try the normal page; if offline, use local docs/SDK types, say so, and never invent version details.
- Entry pages: [System One](https://docs.typesafe.ai/concepts/system-one.md) · [building guide](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md) · [use-case map](https://docs.typesafe.ai/concepts/use-case-map.md) · [state](https://docs.typesafe.ai/concepts/state.md) · [primitives](https://docs.typesafe.ai/primitives.md) · [confidence](https://docs.typesafe.ai/confidence.md) · [HTTP API](https://docs.typesafe.ai/api.md) · [Python SDK](https://docs.typesafe.ai/sdk/python.md) · [JS SDK](https://docs.typesafe.ai/sdk/javascript.md) · [migration](https://docs.typesafe.ai/migrating-to-v1.md)
- Minimal query recipe: [reference.md](reference.md).

## Shape — work back from user-visible behavior to judgments

Keep rules, calculations, lookups, and execution in code. Patterns (cookbooks in the index; starting points, combine freely):
- **Route**: request selects handler + typed args (function calling, speculative fan-out).
- **Select, don't generate**: locate candidates in code, judge picks, code copies/normalizes (pre-parsed extraction, autoformat).
- **Evidence**: retrieve → judge relevance → select context (rerank, hierarchical classification).
- **Reusable data**: score once; weights/thresholds in code drive rankings, views, ML features (composite scoring, feature discovery).
- **Verify & escalate**: judge claims vs evidence; send uncertain cases to a human/reasoning model (citation check, extraction cascade).
- **Changing state**: inferred state ≠ observed facts; recheck freshness before reuse.

Open-ended ask → offer the few best directions, recommend one. Concrete ask → build; no mandatory brainstorm.

## Design judgments

| Need | Primitive | Distinction |
| --- | --- | --- |
| One of a defined set | [choice](https://docs.typesafe.ai/primitives/choice.md) | picks one; distribution compares options |
| Condition holds | [noul](https://docs.typesafe.ai/primitives/noul.md) | P(yes); no separate confidence; one per label |
| Degree on a dimension | [score](https://docs.typesafe.ai/primitives/score.md) | probability-weighted level; comparable per item for ranking |

- Judgment goes in `instructions`, possible answers in `criteria`. Question ids never reach the model — put full meaning in the question. Nested state: backticked paths (`ticket.messages[0].text`).
- `state`: complete relevant context (text, identities, relationships, policies, facts); named JSON fields when multi-part; strings for simple cases, structured objects when definitions/contrasts/examples clarify.
- One narrow coherent judgment per question; split independently useful dimensions. Score levels must describe concrete situations. Include a no-match outcome when nothing may fit; the model cannot select an omitted candidate.

## Compose & verify

- Batch independent questions (incl. speculative ones — state the premise explicitly) over the same state: parallel, blind to each other. Second request only to fetch evidence, build new state, or determine next options. Measure real cost and latency.
- Confidence guides behavior; thresholds come from the user's data and stakes. Choice/Score confidence = distribution concentration, not correctness or permission to act. Noul ≈ 0.5 = yes and no equally likely, not medium intensity. Several acceptable alternatives also spread probability. Ignore uncertainty on unused branches. Weights for compensating preferences; separate conditions for any-serious-violation rules; no rerun when evidence and question meanings are unchanged.
- Typed output ≠ truth — validate in the target domain. Test representative cases and app behavior; on failure inspect exact state, questions, candidates, composition, outcome; separate missing evidence vs model vs code vs service errors. Cookbook thresholds are examples, not rules. Keep API credentials server-side.
