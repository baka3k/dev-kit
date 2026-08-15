# Serena and `rg` Coverage Reconciliation

## Purpose and order

Serena and `rg` do not replace graph traversal. They independently audit graph inventory and resolve gaps in this strict order:

1. graph inventory/path evidence;
2. Serena symbol/reference evidence;
3. `rg` exact source/config sweep.

Fast-fail an unavailable tool once. If all layers fail to establish the module/file inventory, stop and request scope details.

## Serena read-side function set

Call `initial_instructions` before Serena work and `get_current_config` to verify the active repository. Use these four read-side operations for coverage:

| Function | Exact role in this skill |
| --- | --- |
| `get_symbols_overview` | Inventory top-level symbols for each known file; use `depth: 1` to include immediate class members. |
| `find_symbol` | Resolve a name path, overload, class, method, or function; constrain `relative_path`; use `depth: 1` for class methods and `include_body` only for retained anchors. |
| `find_referencing_symbols` | Find callers, external entries, registrations, and source references for a resolved symbol in its file. |
| `search_for_pattern` | Search code and non-code registration surfaces: annotations, routes, DI/config, macros, SQL, messages, errors, events, callbacks, and terminal effects. |

`activate_project` and `get_current_config` are session controls. Memory and editing operations are outside this read-only skill.

### Serena inventory procedure

1. Verify `get_current_config` names the requested repository. Activate it only if necessary.
2. For every file in the source-file universe, call `get_symbols_overview(relative_path, depth: 1)`.
3. Add every top-level class/type/function and immediate method to the source inventory. Preserve name path, kind, file, and location.
4. For each class/type, call `find_symbol` with the exact name path, the containing file, and `depth: 1`. Keep overloads distinct.
5. For each graph entry, source-only public/exported symbol, callback, handler, or registration target, call `find_referencing_symbols`.
6. Use `search_for_pattern` in the canonical module path for registrations and code shapes that language servers omit. Search non-code files when framework configuration can create runtime entries.
7. Reconcile by file + qualified/name path + signature/location. Serena evidence can corroborate a graph edge; a textual reference alone does not prove runtime dispatch.

If Serena lacks directory/file-listing operations, obtain the file universe with graph file planning and finally `rg --files`; record that fallback in evidence.

## `rg` final sweep

Use `rg` only after graph and Serena leave a gap. Run from `repo_root`, always constrain the canonical module path, and save the command/pattern plus matched file/line anchors.

### Source-file universe

```bash
rg --files <module-path> \
  -g '*.{c,cc,cpp,cxx,h,hh,hpp,hxx,java,kt,kts,cs,go,rs,swift,py,js,jsx,ts,tsx,php,rb}' \
  -g '!**/{vendor,node_modules,dist,build,target,.git}/**'
```

Apply project-specific generated/test exclusions separately and record them. Do not hide test sources; place them in the test-evidence set.

### Declaration candidates

Choose patterns for the detected language rather than one universal regex. Examples:

```bash
# C/C++ class/type and function-like definitions
rg -n --pcre2 '\b(class|struct|enum|union)\s+[A-Za-z_]\w*|^[\t ]*(?:[\w:<>,*&~]+[\t ]+)+[A-Za-z_~]\w*(?:::\w+)?[\t ]*\([^;{}]*\)[\t ]*(?:const[\t ]*)?\{' <module-path>

# Java/Kotlin/C# types and callable declarations
rg -n --pcre2 '\b(class|interface|enum|record|object)\s+[A-Za-z_]\w*|\b(?:fun|void|public|protected|private|internal|static|suspend|override)\b[^;{}=]*\([^;{}]*\)[^{;=]*\{' <module-path>

# Python functions/classes
rg -n '^[[:space:]]*(async[[:space:]]+def|def|class)[[:space:]]+[A-Za-z_]\w*' <module-path>

# JavaScript/TypeScript functions, methods, and exported callables
rg -n --pcre2 '\b(function|class|interface|type|enum)\s+[A-Za-z_$]\w*|\b(export\s+)?(const|let|var)\s+[A-Za-z_$]\w*\s*=\s*(async\s*)?(\([^)]*\)|[A-Za-z_$]\w*)\s*=>' <module-path>
```

These are candidate generators. Reconcile false positives and multiline declarations with Serena/source inspection before adding them to denominators.

### Entry and registration candidates

Run scoped searches appropriate to the framework:

```bash
rg -n --pcre2 '@(Controller|RestController|RequestMapping|GetMapping|PostMapping|Scheduled|EventListener|Subscribe|Route)|\b(addEventListener|register|subscribe|on|route|router|listen|schedule|cron)\s*\(' <module-path>
rg -n --pcre2 '\b(main|WinMain|DllMain|onCreate|onStart|onResume|handle|execute|dispatch|consume|produce|callback)\s*\(' <module-path>
rg -n --pcre2 '\b(SERVICE|HANDLER|CALLBACK|ROUTE|COMMAND|EVENT|MESSAGE|TIMER)[A-Z0-9_]*\b' <module-path>
```

Also search framework XML/YAML/JSON/properties, manifest files, build descriptors, route tables, DI modules, generated binding declarations, and macro tables when they affect runtime registration.

### Branch, bridge, and terminal candidates

```bash
rg -n --pcre2 '\b(if|else|switch|case|when|catch|except|throw|throws|retry|timeout|cancel|rollback)\b' <module-path>
rg -n --pcre2 '\b(send|publish|emit|dispatch|notify|postMessage|startService|bindService|fetch|axios|executeQuery|executeUpdate)\s*\(' <module-path>
rg -n --pcre2 '\b(INSERT|UPDATE|DELETE|COMMIT|ROLLBACK)\b|\b(save|persist|remove|delete|update|commit|return|respond|redirect|navigate)\s*\(' <module-path>
```

Search exact IDs, route strings, SQL fragments, error messages, event names, and log text discovered from retained anchors. A match is evidence of source presence, not automatically a graph edge or business use case.

## Reconciliation ledger

For each file/symbol/edge, store:

| Field | Values |
| --- | --- |
| Graph state | present, absent, truncated, unavailable |
| Serena state | present, absent, unsupported, unavailable |
| `rg` state | exact match, candidate match, no match, not run |
| Resolution | verified, corroborated, inferred, unknown, contradicted, excluded_with_reason |
| Evidence | stable node ID and/or repository-relative file + symbol/line |

Resolve discrepancies as follows:

- Graph + Serena agree: `corroborated` inventory evidence.
- Graph only: inspect node details and source path; stale/missing source becomes `contradicted` or a graph-staleness gap.
- Serena/`rg` only: add a source-only symbol and unindexed-scope gap; trace source references without inventing graph edges.
- Name/signature mismatch: keep both until overload, generated code, alias, or stale index explains it.
- Reference without runtime registration: mark the bridge `inferred` or `unknown`.
- All layers absent: do not fabricate context; stop or record a scoped gap depending on whether the module inventory still exists.

The reconciliation pass is zero-delta only when it adds no new file, symbol, entry, branch, registration, bridge, terminal, or evidence conflict.
