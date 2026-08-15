# Document Lifecycle Contract

## Ownership

The orchestrator is the sole writer of `checkpoint.json`, `lifecycle-manifest.json`, `revision-ledger.json`, the accepted revision tree, and final status. Generator, refinement, and review leaves write only their assigned staging roots and local manifests. No orchestrator invokes another orchestrator.

## Run Layout

```text
document-lifecycle/<run-id>/
├── index.md
├── checkpoint.json
├── lifecycle-manifest.json
├── current/
├── revisions/
│   ├── r001-generate/
│   ├── r002-refine/
│   └── r003-review/
├── stages/
│   ├── generate/
│   ├── refinement/<attempt>/
│   └── review/<round>/
└── governance/
    ├── evidence-index.json
    ├── clarification-requests.json
    ├── clarification-answers.json
    ├── refinement-report.md
    ├── review-comments.json
    ├── review-resolution.json
    ├── revision-ledger.json
    └── validation-report.md
```

Final navigation must reference `current/` or root-owned governance artifacts, never staging roots.

## Generator Routing

| Domain | Generator | Optional prerequisites |
| --- | --- | --- |
| system/module summary | `hi-module-summary-report` | `hi-repo-recon`, `hi-tech-build-audit` |
| use case | `hi-usecase-discovery` | `hi-repo-recon` |
| technical behavior | `hi-behavior-modeling` | use-case or entry-point anchor |
| API/event contract | `hi-api-contract-discovery` | module/endpoint inventory |
| data model | `hi-data-model-discovery` | persistence/module inventory |
| command/protocol specification | `hi-command-spec-discovery` | module/command anchor |

Select exactly one generator per scoped lifecycle run. Use `hi-maintenance-docs` directly for a complete multi-domain pack.

## Three Phases

1. **Generate:** validate prerequisites, run one generator, join immutable `r001-generate`, and validate evidence, redaction, links, hashes, and diagrams.
2. **Clarify/refine:** run refinement analysis. Persist `waiting_for_input` when blocking questions lack answers. On resume, apply valid answers to candidate `r002-refine`. Default to two clarification cycles.
3. **Review/update:** when review is optional and comments are absent, record `skipped_no_comments`. When review is required and comments are absent, wait. Otherwise resolve comments against the exact base and join accepted changes as `r003-review`.

## Revision Rules

- Revisions are immutable after acceptance.
- Every candidate names one parent revision and its result hash.
- A leaf never mutates `current/` or `revisions/`.
- The orchestrator verifies candidate hashes before copying or materializing them.
- Stale inputs require explicit rejection or a separately authorized rebase; never silently rebase.
- Only the changed dependency closure is revalidated, but unchanged referenced hashes must still match the base.

## Human Input and Evidence

Clarification answers and review comments use `human_declared`, `reviewer_declared`, or `unverified_external` provenance. They may explain intent or terminology, but they cannot become implementation-verified evidence without source corroboration. Conflicts with verified source remain visible and force rejection, downgrade, or a documented contradiction.

## Diagram Render Ledger

Every accepted standalone Mermaid artifact and every `mermaid` fenced block inside Markdown requires one passing record in `diagram-render-results.json`. Use the artifact ID for a standalone `.mmd` file. Use `<artifact-id>#mermaid-N` for fenced blocks, numbered from one in document order, and hash the exact block body captured between the opening and closing fences. Validate the rendered output path and hash before completing either a scoped lifecycle or maintenance pack.

## Publication

Comment resolution and publication approval are separate. A resolved review does not set `review_state=approved`. Public visibility requires an explicit approval artifact after redaction, evidence, lifecycle, and link validation pass.
