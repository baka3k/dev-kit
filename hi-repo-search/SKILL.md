---
name: hi-repo-search
description: "Search and understand any repository pushed into the Code Graph + Document Graph RAG system. Combines code-level analysis (call graphs, dependencies, semantic search) with document-level knowledge retrieval (vector search, entity relations)."
argument-hint: "[query] [--code|--doc|--deep] — default: full hybrid search"
metadata:
  author: baka3k
  version: "1.0.0"
---

# Repo Search - Repository Exploration

Use code graph MCP + document graph RAG MCP to understand any codebase that has been ingested into the system.

## Concept

Two MCP servers work together:

| MCP | Database | Purpose |
| --- | --- | --- |
| **code_graph** | Neo4j + Qdrant | Code structure: functions, classes, call graphs, dependencies |
| **graph_rag** | Neo4j + Qdrant | Document knowledge: paragraphs, entities, relations, semantic search |

## Intent Detection

| Input | Mode | Behavior |
| --- | --- | --- |
| `--code` | code-only | Only use code_graph MCP |
| `--doc` | doc-only | Only use graph_rag MCP |
| `--deep` | deep | Use both MCPs + cross-reference between code and doc |
| Default | hybrid | Use both MCPs, prioritizing the most relevant results |

## Process Flow

`[Discover] -> [Search] -> [Trace] -> [Synthesize]`

### Step 1: Discover (Orientation)

Objective: Know what the project contains.

**Code side** (via code_graph MCP):

* `list_databases()` — list all databases/projects that have been ingested
* `activate_project(parser_type, database_name)` — select a project to work with
* `listup_symbols_matching_file_path(modules)` — list symbols within a file/module
* `list_up_entrypoint(modules)` — find entry points / public APIs

**Doc side** (via graph_rag MCP):

* `list_source_ids(limit)` — list all documents that have been ingested
* `list_qdrant_collections()` — list Qdrant collections

### Step 2: Search (Discovery)

Objective: Find code/documents relevant to the query.

**Code side**:

* `search_functions(query, limit)` — search for functions/classes by name
* `search_by_code(query, limit)` — search for code by content
* `semantic_search(query, mode, top_k)` — search for code semantically (using natural language)
* `explore_graph(query, mode, top_k)` — hybrid search combining semantic + keyword + graph expansion

**Doc side**:

* `semantic_search(query, top_k, source_id)` — vector search within documents
* `query_graph_rag_langextract(query, top_k, expand_related)` — search + entity expansion, returning passages + entities + relations

### Step 3: Trace (Deep Dive)

Objective: Understand relationships, call chains, and dependencies.

**Code side**:

* `get_symbol(node_id)` or `get_node_details(node_ids)` — view details of a specific symbol
* `query_subgraph(function_id, max_depth, direction)` — view the call graph surrounding a function
* `find_paths(start_function_id, end_function_id)` — trace paths between 2 functions
* `find_path_between_module(source_modules, target_modules)` — trace cross-module paths

**Doc side**:

* `get_paragraph_text(source_id, paragraph_id)` — read the full text of a paragraph

### Step 4: Synthesize (Conclusion)

Synthesize results from both MCPs into a comprehensive report covering:

* Overall architecture
* Main components (modules, classes, entry points)
* Relationships and dependencies
* Domain knowledge from documentation
* Code-to-doc cross-references (if `--deep` is used)

## Workflow Patterns

### Pattern A: "What does this repo do?"

```
1. list_databases() → select database
2. activate_project(...)
3. list_up_entrypoint(["main"]) → understand the entry point
4. semantic_search("what is this project about") → doc overview
5. query_subgraph(entry_function_id) → view the call graph

```

### Pattern B: "How does feature X work?"

```
1. search_functions("X|FeatureX") → find relevant functions
2. get_symbol(node_id) → read the code
3. query_subgraph(function_id, direction="both") → understand dependencies
4. semantic_search("how X works") → find relevant documentation
5. query_graph_rag_langextract("X implementation") → doc + entities

```

### Pattern C: "Find all callers/callees of function Y"

```
1. search_functions("Y") → get function_id
2. query_subgraph(function_id, direction="in") → callers
3. query_subgraph(function_id, direction="out") → callees
4. get_node_details(all_ids) → get code for all retrieved nodes

```

### Pattern D: "What dependencies does module Z have?"

```
1. listup_symbols_matching_file_path(["z/"]) → get symbols in the module
2. find_path_between_module(source_modules=["z/"], target_modules=[]) → cross-module tracing
3. plan_dependency_order(modules=["z"]) → determine dependency order

```

### Pattern E: "Deep dive: full repository analysis"

```
1. list_databases() + activate_project()
2. list_source_ids() + list_qdrant_collections()
3. listup_symbols_matching_file_path(...) → retrieve all symbols
4. list_up_entrypoint([...]) → identify entry points
5. For each entry point: query_subgraph(...), get_node_details(...)
6. explore_graph("overall architecture", mode="graph_expanded")
7. query_graph_rag_langextract("system overview", expand_related=True)
8. Synthesize final report

```

## Important Notes

* Always call `list_databases()` first to identify available projects.
* Always call `activate_project()` before querying the code graph.
* `explore_graph` is the most powerful tool for code search — use it before `search_functions` when the exact name is unknown.
* `query_graph_rag_langextract` with `expand_related=True` returns both entities and relations — use it when a broad context is needed.
* Limit `max_depth` and `top_k` reasonably to prevent excessively large outputs.
* When analyzing large repositories, prioritize a pattern-based approach rather than attempting to dump everything.

## Reference Docs

* [Code Graph MCP Functions](https://www.google.com/search?q=./references/code_graph.md) — all functions for code_graph MCP
* [Document Graph RAG MCP Functions](https://www.google.com/search?q=./references/doc_graph_rag.md) — all functions for graph_rag MCP

---