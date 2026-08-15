# Semantic and Diagram Review

## Semantic Checks

1. Terms and stable IDs are consistent across definition, usage, tables, diagrams, and indexes.
2. Actors, permissions, preconditions, guards, branches, errors, terminal outcomes, and related API/data/state IDs are explicit when evidenced.
3. Data definitions remain separate from protocol or processing behavior.
4. Human explanations are marked by provenance and do not override verified source silently.
5. Contradictions, missing runtime behavior, caps, and stale evidence remain visible.

## Diagram Checks

For every Mermaid source verify:

- a text summary, legend, stable IDs, and evidence references exist;
- participants/nodes map to supported implementation or declared domain entities;
- messages/edges have direction, action/relationship meaning, and ordering where relevant;
- guards, alternative/error paths, states, triggers, and terminal outcomes are present when evidenced;
- labels do not expose secrets, PII, connection strings, or unsafe markup;
- meaning does not depend only on color;
- sequence diagrams stay at or below 12 lifelines and 30 messages by default;
- state diagrams stay at or below 15 primary states by default;
- architecture diagrams stay at or below 30 nodes and 80 dependency edges by default;
- oversized views split into overview and drill-down diagrams with recorded omissions;
- the source renders successfully before acceptance.

Do not add unsupported detail merely to make a diagram larger. Record absent evidence as a gap or clarification request.
