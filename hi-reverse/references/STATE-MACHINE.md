# State Machine

Generate a Mermaid state machine when the `stateful` condition is active.

## Retrieval

1. Query state enums, mode flags, transition setters, dispatch switches, guards, initialization, terminal states, invalid transitions, and recovery states.
2. Expand each state-changing anchor through FalkorDB for triggers, guards, effects, and next states.
3. Use Serena to confirm enum values, switch cases, assignments, and transition conditions.
4. Build a transition table before drawing the diagram.
5. Mark transitions as `PROVEN`, `LIKELY`, or `TENTATIVE`; omit rejected transitions.

## Output

Write `state-machine.mmd` beginning with `stateDiagram-v2`. Include initial/final states, guarded transitions, error/recovery paths, and evidence IDs in labels or an adjacent table. Never infer a transition from enum ordering.
