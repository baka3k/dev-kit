# Lifecycle Transition Contract

## States

| Phase | Allowed status | Next phase/status |
| --- | --- | --- |
| `generate` | `pending` | `generate/running` |
| `generate` | `running` | `clarify_refine/pending`, `generate/failed`, or `generate/blocked` |
| `clarify_refine` | `pending` | `clarify_refine/running` |
| `clarify_refine` | `running` | `clarify_refine/waiting_for_input`, `review_update/pending`, `clarify_refine/blocked`, or `clarify_refine/failed` |
| `clarify_refine` | `waiting_for_input` | `clarify_refine/running` after valid answers, or `clarify_refine/blocked` after the cycle limit |
| `review_update` | `pending` | `review_update/running`, `review_update/skipped`, or `review_update/waiting_for_input` |
| `review_update` | `running` | `complete/succeeded`, `complete/partial`, `review_update/waiting_for_input`, `review_update/blocked`, or `review_update/failed` |
| `review_update` | `waiting_for_input` | `review_update/running`, `review_update/skipped` after explicit no-comment decision, or `review_update/blocked` |
| `complete` | `succeeded`, `partial`, `blocked`, or `failed` | terminal |

## Guards

1. `generate -> clarify_refine` requires accepted `r001-generate` with valid hashes.
2. `clarify_refine -> waiting_for_input` requires at least one open blocking question and resume state.
3. `waiting_for_input -> running` requires answers tied to the current base revision and question set.
4. `clarify_refine -> review_update` requires no unanswered blocking question and accepted `r002-refine` or an unchanged accepted `r001` when no refinement is needed.
5. `review_update -> skipped` requires `review_required=false` and an empty comment set.
6. `review_update -> waiting_for_input` requires `review_required=true` and no review decision/comments.
7. `review_update -> complete` requires every supplied comment to have one disposition and a valid accepted revision.
8. `complete/succeeded` with public visibility requires `review_state=approved`.

Reject every transition not listed above. Retry counts and clarification cycles never reset on resume.
