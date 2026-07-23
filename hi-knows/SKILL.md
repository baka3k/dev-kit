---
name: hi-knows
description: Unified knowledge retrieval skill. Build traceable answers from git, MCP, and memory files.
version: 2.0.0
last_updated: 2026-05-28
---

# Knows

Answer with evidence using sources in strict order: **Git → MCP (mind/graph) → Memory files**

## When To Use

Why-changed / impact-radius / architecture context — NOT for syntax fixes, pure impl, or DB mutations.

## Evidence Priority

| Question Type        | Priority Order                      |
| -------------------- | ----------------------------------- |
| Structure/Runtime    | graph_mcp → Git → mind_mcp → memory |
| Historical/Rationale | mind_mcp → memory → Git → graph_mcp |

## Workflow

**Phase 1 - Preflight:** Classify intent (`why-changed`, `impact-analysis`, `architecture-context`, `history-trace`)

**Phase 2 - Git:**

```bash
# Scope first, then pull detail
git log --oneline --decorate -20 -- <path>
git show <commit> --stat --format="%h %s"
git blame -L <start>,<end> --date=short <file>
```

Normalize before synthesis — git metadata, unchanged context, and ANSI codes add tokens without aiding reasoning. Pipe verbose git output through `node scripts/git-normalize.js` (default cleanup; add `--changed` for large diffs). See [Git Output Normalization](./references/git-output-normalization.md).

**Phase 3 - MCP:**

- `mind_mcp`: `hybrid_search`, `query_graph_rag_relation`, `sequential_search`
- `graph_mcp`: `semantic_search`, `query_subgraph`, `find_paths`, `analyze_workflow_impact`

**Phase 4 - Memory:** Workspace-first, then home. Allowlist: `memory*.md`, `agent*.md`, `claude*.md`, `cursor*.md`

**Phase 5 - Synthesis:** Merge by priority. Separate facts/inferences/conflicts.

## Output Format

`## Kết luận ngắn` → `## Độ tin cậy` (confidence + sources) → `## Bằng chứng` (Git/MCP/Memory) → `## Điểm chưa chắc chắn` → `## FalkorDB Query Suggestion (optional)`

## Guardrails

- Never claim from single weak source
- Every high-impact claim needs citation
- Do not execute direct FalkorDB/Neo4j queries (suggest only)
- Redact secrets before citing

## Limits

- MCP timeout: 30s/call, 5min total
- File size: 300KB max
- Files/query: 10 max
- Cache TTL: 10min

## References

- Read [Git Output Normalization](./references/git-output-normalization.md) before pulling git detail — commands and token caps.
- Read [Source Priority & Conflict](./references/source-priority-and-conflict.md) when sources disagree or to set confidence.
- Read [Retrieval Playbook](./references/retrieval-playbook.md) when a source fails or input must be validated.
- Read [Memory Source Policy](./references/memory-source-policy.md) before reading memory files.
- Read [FalkorDB Query Suggestion Template](./references/falkordb-query-suggestion-template.md) only when offering a suggested query.

## Degraded Mode

```markdown
⚠️ Degraded Mode: {reason}

- Unavailable: {failed channels}
- Missing: {limited evidence}
- Confidence: {downgraded reason}
```
