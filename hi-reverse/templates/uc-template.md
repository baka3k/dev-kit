# Use Case UCXXX - {{USE_CASE_NAME}}

## Meta

| Field | Value |
|---|---|
| UC ID | UCXXX |
| Module | {{MODULE}} |
| Date | {{DATE}} |
| Status | Draft |
| Confidence | {{PROVEN_LIKELY_OR_TENTATIVE}} |

## Goal

{{OBSERVABLE_BUSINESS_GOAL_AND_TERMINAL_OUTCOME}}

## Actors

| Actor | Type | Description |
|---|---|---|
| {{ACTOR}} | Primary | {{ROLE}} |

## Preconditions And Guards

{{STATES_MODES_PERMISSIONS_AND_VALIDATIONS}}

## Main Flow

| Step | Business action | Symbol/node | Relationship | State change | Evidence |
|---|---|---|---|---|---|
| 1 | {{ACTION}} | {{SYMBOL}} | entry | {{STATE_CHANGE}} | {{TOOL_QUERY_OR_CLAIM_ID}} |

## Alternate And Error Flows

| Branch | Trigger/guard | Steps | Outcome | Evidence |
|---|---|---|---|---|
| ERROR | {{CONDITION}} | {{STEPS}} | {{OUTCOME}} | {{CLAIM_ID}} |

## Code References

| Symbol | File:Line | Role | Graph node | Notes |
|---|---|---|---|---|
| `{{SYMBOL}}` | {{FILE_LINE}} | ENTRYPOINT | {{NODE_ID}} | {{NOTES}} |

## Sequence Diagram

[Open sequence diagram]({{SEQUENCE_FILE}})

| Participant/step | Evidence | Uncertainty |
|---|---|---|
| {{PARTICIPANT}} | {{NODE_PATH_SOURCE}} | {{LOW_MEDIUM_HIGH}} |

## Class Diagram

[Open class diagram]({{CLASS_FILE}})

| Type/relationship | Evidence | Uncertainty |
|---|---|---|
| {{TYPE_RELATIONSHIP}} | {{NODE_SOURCE}} | {{LOW_MEDIUM_HIGH}} |

## Retrieval Trace

| Step | Tool call | Information returned | Decision |
|---|---|---|---|
| 1 | {{CALL}} | {{EVIDENCE}} | {{NEXT_DECISION}} |

## Unresolved Gaps

- {{GAP_OR_NONE}}

## Artifact Gate

`ARTIFACT_GATE: PENDING`

## Version History

| Version | Date | Change |
|---|---|---|
| v1 | {{DATE}} | Initial evidence-backed use case |
