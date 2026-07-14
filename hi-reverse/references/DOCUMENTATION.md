# Use-Case Documentation

Create a use-case document from discovery, trace, diagram, module-map, class, and glossary evidence. Read `GRAPH-RAG-PROTOCOL.md` before retrieving any missing fact.

## Evidence Gate

Before writing:

1. require an evidence status for every candidate;
2. require a trace manifest for every `PROVEN` use case;
3. require a use-case-specific sequence diagram generated from that trace;
4. require a use-case-specific class diagram generated from retained type and relationship evidence;
5. re-enter Graph-RAG for missing trigger, guard, actor, outcome, branch, message, state, external-system, or type-relationship evidence;
6. use Serena only for remaining conditions and line references;
7. preserve uncertainties and unavailable areas in the document.

Do not upgrade `LIKELY` or `TENTATIVE` behavior through prose. Do not copy existing project documentation when the user prohibited it.

## Document Structure

1. metadata: UC ID, module, status, confidence, date
2. goal and observable outcome
3. actors and external systems
4. trigger, preconditions, modes, and guards
5. main flow: business step, symbol/node ID, relation, state change, evidence
6. alternate/error/timeout/recovery flows
7. postconditions and terminal side effects
8. IPC/callback/shared-state bridges and uncertainties
9. code references with file/line and graph node IDs
10. sequence diagram link and evidence summary
11. class diagram link and relationship evidence summary
12. retrieval trace, query coverage, saturation, and unresolved gaps
13. artifact gate result and version history

## Output

Write the complete bundle:

- `usecase/<MODULE>/ucXXX_<name>.md`
- `usecase/<MODULE>/trace_<name>.json`
- `usecase/<MODULE>/seq_<name>_<YYYYMMDD>_v1.mmd`
- `usecase/<MODULE>/class_<name>_<YYYYMMDD>_v1.mmd`

The document must contain `## Sequence Diagram` and `## Class Diagram` sections linking the exact files. Run `npx --yes --offline --package=. hi-reverse-validate-package <package-manifest.json> --update` from the skill directory and require `REVERSE_PACKAGE_GATE: PASS` before review or delivery. Keep business language readable while making every executable claim traceable to the evidence ledger.
