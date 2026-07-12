
---

# Graph RAG MCP — Document Knowledge Functions

MCP server: `graph_rag` | Transport: `streamable-http` | Default port: `8789`

Backend: **Neo4j/FalkorDB** (entities, relations, paragraphs) + **Qdrant** (vector embeddings of documents)

## Functions

### `list_source_ids`

Lists all source_ids (documents) that have been ingested into VectorDB/GraphDb.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `limit` | int | No | 50 | Maximum number of results |

**Returns**: `List[str]` — list of source_ids

**Use when**: Initial exploration — when you want to know what documents are available in the system.

---

### `list_qdrant_collections`

Lists all Qdrant collections.

**No params**

**Returns**: `List[str]` — list of collection names

**Use when**: You need to know the available vector collections to choose the `collection` parameter for search functions.

---

### `semantic_search`

Vector-only search within Qdrant. **Does not expand the graph.** Only returns passages.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Natural language query |
| `top_k` | int | No | 5 | Number of passages to return |
| `source_id` | str | No | None | Filter by a specific document |
| `collection` | str | No | "documents" | Qdrant collection name |
| `max_passage_chars` | int | No | None | Truncate the text passage if it is too long |
| `include_entity_ids` | bool | No | True | Whether to include entity_ids in the results |
| `include_entity_mentions` | bool | No | False | Whether to include detailed entity_mentions |

**Returns**:

```json
{
  "query": "...",
  "top_k": 5,
  "source_id": null,
  "collection": "documents",
  "passages": [
    {
      "text": "...",
      "score": 0.95,
      "source_id": "...",
      "paragraph_id": 42,
      "entity_ids": ["ent_1", "ent_2"],
      "entity_mentions": [...] // if include_entity_mentions=True
    }
  }
}

```

**Use when**: You need to quickly find text segments relevant to the question without requiring entity/relation expansion.

---

### `query_graph_rag_langextract`

**Primary function** — search + entity/relation expansion. Queries Qdrant to retrieve passages, then fetches entities and relations from Neo4j/FalkorDb based on the entity_ids found in those passages.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | The query string |
| `top_k` | int | No | 5 | Number of passages to return |
| `source_id` | str | No | None | Filter by document |
| `collection` | str | No | "documents" | Qdrant collection |
| `include_entities` | bool | No | True | Fetch entity details from Neo4j/FalkorDb |
| `include_relations` | bool | No | True | Fetch relations between entities |
| `expand_related` | bool | No | True | Expand relationships (only works if `include_relations` is enabled) |
| `related_k` | int | No | 50 | Maximum number of relations |
| `graph_depth` | int | No | 1 | Depth of graph expansion (1 = direct neighbors, 2 = neighbors of neighbors...) |
| `entity_types` | str/list | No | DEFAULT_ENTITY_TYPES | Filter entities by type. String format: "ORG,PRODUCT,TECH" |
| `max_passage_chars` | int | No | None | Truncate text |
| `min_score_to_expand` | float | No | None | Minimum score threshold to expand an entity. If max score is less than threshold → do not expand |
| `min_entity_occurrences` | int | No | None | An entity must appear at least N times in the passages to be expanded |
| `rerank` | bool | No | False | Enable heuristic re-ranking |
| `rerank_entity_weight` | float | No | 0.05 | Weight for entity count |
| `rerank_type_weight` | float | No | 0.1 | Weight for type match |
| `rerank_confidence_weight` | float | No | 0.3 | Weight for confidence |
| `rerank_length_penalty` | float | No | 0.0002 | Penalty for excessively long passages |

**Returns**:

```json
{
  "query": "...",
  "top_k": 5,
  "source_id": "...",
  "collection": "documents",
  "graph_depth": 1,
  "min_score_to_expand": null,
  "min_entity_occurrences": null,
  "rerank_applied": false,
  "rerank_strategy": null,
  "passages": [
    {"text": "...", "score": 0.95, "source_id": "...", "paragraph_id": 42}
  ],
  "entities": [
    {"id": "ent_1", "name": "EntityName", "type": "ORG"}
  ],
  "relations": [
    {"source_id": "ent_1", "source": "A", "source_type": "ORG",
     "relation": "USES", "target_id": "ent_2", "target": "B", "target_type": "TECH"}
  ]
}

```

**Use when**: Deep understanding is required — needing not just the passages but also the entities and the relationships between them. This is the most powerful function of the graph_rag MCP.

**Default Entity Types**: ORG, PRODUCT, STANDARD, TECH, CRYPTO, SECURITY, PROTOCOL, VEHICLE, DEVICE, SERVER, APP, CERTIFICATE, KEY

---

### `get_paragraph_text`

Fetches the full text of a specific paragraph from Neo4j/FalkorDb.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_id` | str | **Yes** |  | Document ID (from search results) |
| `paragraph_id` | int | **Yes** |  | Paragraph ID (from search results) |

**Returns**:

```json
{
  "text": "Full paragraph text...",
  "short": "Short summary if available",
  "source_id": "...",
  "paragraph_id": 42
}

```

Or `{"source_id": "...", "paragraph_id": 42, "text": null, "warning": "Paragraph not found."}`

**Use when**: The search returns a truncated passage (due to `max_passage_chars`) and you need to read the full text.

## Typical Usage Flow

```
1. list_source_ids(limit=100)           → Identify available documents
2. list_qdrant_collections()            → Identify available collections
3. semantic_search("query", top_k=10)   → Quickly find relevant passages
4. query_graph_rag_langextract(         → Deep search with entity + relation expansion
     "query",
     top_k=10,
     expand_related=True,
     graph_depth=2,
     rerank=True
   )
5. get_paragraph_text(source_id, paragraph_id) → Read full text if needed

```

---
