# Module Profile

Use this profile for complete behavioral and structural reverse engineering of one module.

## Always Required

- complete use-case profile for every documented use case
- module overview and entry-point catalog
- module map and component context
- business-rule and error/recovery catalogs
- evidence ledger and open-questions log
- glossary and coverage report

## Conditional Artifacts

| Condition | Required artifacts |
|---|---|
| `stateful` | state machine |
| `ipc` | interface catalog and IPC topology |
| `persistence` | data dictionary and data-flow diagram |
| `concurrency` | concurrency model |
| `branching` | activity diagram per affected use case |
| `distributed` | deployment/runtime diagram |

Determine conditions from Graph-RAG evidence, not user wording alone. Update and rerun the artifact plan whenever discovery activates a new condition.

The module package passes only when every required artifact validates and every conditional dimension is generated or explicitly proven not applicable.
