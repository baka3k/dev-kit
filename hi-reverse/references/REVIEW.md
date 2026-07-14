# Evidence Review

Validate `<UC_FILE>` independently against FalkorDB, Qdrant, and Serena evidence. Read `GRAPH-RAG-PROTOCOL.md` first.

## Review Flow

1. Run `npx --yes --offline --package=. hi-reverse-validate-package <package-manifest.json> --update` from the skill directory; stop review if `REVERSE_PACKAGE_GATE` fails.
2. Confirm the sequence diagram follows the trace order and the class diagram contains only use-case participants and evidenced relationships.
3. Extract every factual claim: actor, trigger, guard, ordered step, state change, branch, message, external system, and outcome.
4. Run fresh Qdrant semantic queries using paraphrases that differ from the document wording.
5. Pair every query with `explore_graph`; resolve claimed symbols and retain independent FalkorDB relationships and path evidence.
6. Verify each consecutive executable step with focused caller/callee and source/target path queries.
7. At every non-direct transition, query callback/virtual/function-pointer registration, IPC both directions, shared state, and cross-module relationships.
8. Query workflow ownership/impact semantically when workflow nodes or concepts appear.
9. Search independently for missing lifecycle, state, integration, side-effect, cancel, invalid, timeout, retry, error, and recovery behavior.
10. After Graph-RAG saturation, use Serena to verify exact symbols, references, branch conditions, constants, and line locations.
11. Classify each claim as `CONFIRMED`, `PARTIAL`, `UNSUPPORTED`, `CONTRADICTED`, or `STALE`.
12. Re-run artifact, completeness, and saturation gates; list omissions instead of silently editing them away.

For module or migration delivery, run `npx --yes --offline --package=. hi-reverse-validate-package <package-manifest.json> --update` from the skill directory after claim review. Do not pass the review package until `REVERSE_PACKAGE_GATE: PASS`.

## Review Output

Return findings ordered by severity, then:

| Claim | Status | FalkorDB/Qdrant evidence | Serena evidence | Required correction |
|---|---|---|---|---|

Mark the UC `Reviewed` only when `ARTIFACT_GATE: PASS`, both diagrams agree with the evidence ledger, no material `UNSUPPORTED` or `CONTRADICTED` claim remains, and all applicable dimensions are evidenced or explicitly unresolved.
