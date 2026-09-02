---
name: hi-command-spec-discovery
description: "Produce draft-only special command or protocol wire-format specification from implementation code, including APDU/TLV fields, CLA/INS/P1/P2/Lc/Le framing, opcodes, status words, and command-specific models. Do not use for business scenarios, API contracts, or standalone behavior modeling."
---

# Command Specification Discovery

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Operate as a draft-only leaf; lifecycle orchestrator owns refinement, review, and publication.

## Inputs

Require `repo_root`, a module path or command anchor, and `output_root`. Accept command name/opcode/header, parser/database/project/collection identity, source revision, protocol hints, visibility (`internal` by default), and explicit result/depth limits. Limits protect tools; they never prove completeness.

## Retrieval Gate

Read [retrieval-protocol.md](references/retrieval-protocol.md) and [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Reject wrong-project results. Treat names, semantic hits, comments, and existing documents as candidates until implementation paths corroborate them. Graph profile (T3 in [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md)): `search_by_code` for opcodes, literals, and status words; `list_possible_calls` and `get_ipc_message` for indirect dispatch; `find_paths` for dispatcher-to-terminal proof.

## Workflow

1. Verify repository and graph identity. Build the module file universe before reading command handlers.
2. Inventory all graph-visible files, classes/types, functions/methods, entry points, registrations, dispatch tables, constants, tags, status words, serializers, parsers, indirect calls, and terminal effects. Reconcile graph counts with Serena then `rg`.
3. Identify command seeds from names, opcodes, headers, literals, field tags, error values, and registration sites. Add retained stable symbol IDs to a deterministic trace queue.
4. Drain the queue through direct, possible, callback, function-pointer, IPC, API, UI, and cross-module edges until empty and a zero-delta discovery pass adds no symbols. Prove dispatcher-to-terminal paths; record every cap, truncation, dynamic gap, and unindexed file.
5. Reconstruct command definition, request/response fields, validation/ordering/encoding rules, success behavior, failure status words, and state transitions. Keep contradictory variants separate by version or guard.
6. Generate requested scope from [command-document-template.md](references/command-document-template.md), always retaining command and response field tables. Generate complete document with diagrams only when explicitly requested. Use `{N/A}` for unsupported sections. Never invent or reformat tags, lengths, opcodes, transitions, or status words beyond verified evidence.
7. Write inventories, trace/evidence ledgers, coverage, gaps, `command-index.json`, and local manifest per [output-contract.md](references/output-contract.md). Validate against [command-output.schema.json](references/command-output.schema.json).

## Completion

Complete only when every inventoried command seed is classified, every emitted field/status/transition cites code evidence, the trace queue is empty, graph/Serena/`rg` inventories are reconciled, and one final zero-delta pass succeeds. Any unresolved truncation, project mismatch, missing bridge, denominator mismatch, runtime-only dispatch, or unindexed source forces `partial` or `blocked`, never `succeeded`.
