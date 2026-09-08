# Sync Recipes — Legacy and Modern Lanes

Two project-scoped lanes keep the C/Pro*C/C++ side and the Java/MyBatis/Spring side in separate
graph databases and vector collections. The `dev` CLI has **no per-side switch** — analyzers are
chosen per language automatically — so the lane exists only through explicit source roots plus
mandatory project/graph/collection flags. Never run bare `dev sync code` (interactive folder
picker) and never omit the per-side flags: an unflagged sync merges both sides into the default
project and every later query inherits the wrong parser scope.

## Naming contract

| Lane | Project / graph / collection | Sources |
| --- | --- | --- |
| legacy | `<app>-legacy` | `.c` `.h` `.cc` `.cpp` `.cxx` `.pc` `.pcc`, active build/preprocessor config, generated-lineage manifests |
| modern | `<app>-modern` | Java, MyBatis mapper XML, Spring configuration, build descriptors, test evidence |
| knowledge base docs | same lane's project via `dev sync doc`, or a doc-only project when documents span both sides | `.pdf` `.md` `.docx` `.txt` `.pptx` `.xlsx` |

Query time must match the lane: legacy → `parser_type='cplus'` (aliases `c`, `cpp`, `proc`,
`pro*c`); modern → `parser_type='spring'` primary, `'mybatis'` for mapper/DAO evidence. On shared
or multi-project hosts pass the lane's `project_id` on every call and verify results belong to it.

## Lane: sync-legacy

1. `dev status` — config exists, backend `local`, expected folders present.
2. `dev sync code add <legacy-root> [--git <url>]` — once per root (prompt answers must come from
   the user, never guessed).
3. `dev sync code --sync-mode both` — incremental ingest of the lane's roots; the first run is
   always a full scan.
   - call-graph-only refresh: `dev sync code --full-scan --sync-mode graph`
   - embeddings-only refresh: `dev sync code --full-scan --sync-mode embedding`
4. `dev sync doc` — knowledge-base documents for the lane.
5. Verify: `search_functions` / `query_subgraph` with `parser_type='cplus'` must return a known
   symbol **from an authored `.pc` file** — the cplus analyzer parses Pro*C directly (EXEC SQL
   units become `SqlStatement` nodes, host variables become `BINDS_PARAMETER` edges; verified
   2026-09-08: `.pc` sample → `parser=cplus files=1 functions=2 classes=4`). A missing expected
   symbol is a recorded gap — never claim authored-Pro*C coverage from generated-`.c` hits alone.

## Lane: sync-modern

1. `dev status` — same checks.
2. `dev sync code add <modern-root> [--git <url>]` — once per root.
3. `dev sync code --sync-mode both` (same sync-mode matrix as legacy).
4. `dev sync doc` — knowledge-base documents for the lane.
5. Verify: `parser_type='spring'` returns known controllers/services (`get_framework_context` for
   beans), and the parity chain `get_endpoints` → `find_callers_of_endpoint` →
   `get_api_call_chain` resolves a known screen → mapper → SQL route.

## Shared rules

- **Instance topology**: default is one shared instance holding both lane projects; pass
  `project_id` at query time. Named per-side instances
  (`dev start --name <app>-legacy --project <app>-legacy --port 8790`) only when the user asks
  for hard isolation — they double resident embedding-model memory — and then stop only with
  `dev stop --name <instance>`; bare `dev stop` kills every MCP on the machine.
- `--full-scan` is required with the `graph`/`embedding` sync-modes; those modes do not move the
  shared incremental baseline — return to `--sync-mode both` afterwards.
- Prefer fully flagged, non-interactive commands. Wizard-style prompts (`dev init`, `dev sync
  code add` without arguments, bare `dev sync code`) require user-provided values.
- After every sync: `dev status` plus the summary's phase results and journal state
  (`journal: ... pending=0 blocked=0` is healthy). Degraded or failed phases are reported to the
  user, never hidden — see [MCP lifecycle](./mcp-lifecycle.md) and
  [project ingestion](./project-ingestion.md) for scope/provenance doctrine.
