# Cross-Artifact Validation Contract

## Output Schema

`cross-validation-results.json` contains:

```json
{
  "schema_version": "1.0",
  "producer_skill": "hi-cross-artifact-validation",
  "run_id": "<id>",
  "domains_validated": ["usecase", "api", "data", "behavior", "command"],
  "stable_id_index": [
    { "id": "<stable-id>", "domains": ["usecase", "api"], "entity": "<name>", "status": "resolved|orphaned|ambiguous" }
  ],
  "findings": [
    {
      "id": "<finding-id>",
      "check": "stable_id|actor_auth|state_lifecycle|schema_compat|evidence_coherence|dependency_coverage",
      "severity": "error|warning|info",
      "domains": ["<domain-a>", "<domain-b>"],
      "affected_ids": ["<stable-id>"],
      "description": "<human-readable>",
      "evidence": { "source_a": "<path>", "source_b": "<path>" },
      "recommendation": "<action>"
    }
  ],
  "summary": {
    "total_checks": 6,
    "checks_run": 4,
    "checks_skipped": 2,
    "skip_reasons": [],
    "errors": 1,
    "warnings": 3,
    "info": 5
  },
  "status": "succeeded|partial|blocked",
  "strict_mode": false,
  "created_at": "<ISO-8601>"
}
```

## Severity Rules

- `error`: Cross-domain contradiction that blocks reliable document assembly (e.g., verified status in one domain contradicted in another, actor with no auth mapping when auth is required).
- `warning`: Potential inconsistency requiring human judgment (e.g., stable ID present in one domain but not another where presence is expected).
- `info`: Observations for completeness (e.g., domain has no cross-references to another domain).

## Status Rules

- `succeeded`: All applicable checks run with zero errors.
- `partial`: Checks run with warnings or skipped domains (non-strict mode).
- `blocked`: Strict mode with errors, or fewer than two domains available.

## Integration Points

- `hi-maintenance-docs`: Run as optional stage 6 after all leaf manifests join (before synthesis).
- `hi-document-lifecycle`: Run as optional pre-synthesis check when multiple prerequisite domains exist.
- Standalone: Invoke directly with an output root containing discovery artifacts.
