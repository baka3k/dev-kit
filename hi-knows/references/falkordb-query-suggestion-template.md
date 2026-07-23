# Graph Query Suggestion Template

FalkorDB is the primary graph backend (runs on Redis, Cypher-compatible). Neo4j
is a secondary fallback only. The Cypher patterns below work on both backends
because they share OpenCypher syntax; the differences are operational, not
query-level.

> Never execute these queries directly. Offer them as **suggestions** for the
> user to run in their own FalkorDB / Neo4j client, and preface each with the
> target backend.

## Suggestion Block

```text
Graph Query Suggestion (FalkorDB):
- Objective:   <what the query answers>
- Rationale:   <why this path / depth>
- Cypher:      <query>
- Expectation: <expected row shape>
- Interpretation: <how to read the result>
```

Switch the header label to `(Neo4j)` only when the user's backend is Neo4j.

## Patterns

All patterns use the relationship types graph_mcp emits (`CALLS`, `USES`,
`DEPENDS_ON`, `HAS_STEP`, `MATCHES`). They are identical on FalkorDB and Neo4j.

* **Callers:** `MATCH (caller)-[:CALLS*1..4]->(target {name: $name}) RETURN caller.name, target.name LIMIT 200;`
* **Downstream:** `MATCH p=(start {name: $name})-[:CALLS|USES|DEPENDS_ON*1..5]->(n) RETURN p LIMIT 100;`
* **Workflows:** `MATCH (w:Workflow)-[:HAS_STEP]->(f {symbol_id: $id}) RETURN w.name, f.name LIMIT 100;`

## Parameter Binding

- FalkorDB and Neo4j both use `$param` for bound parameters (not `$1` positional).
- Always parameterize user-supplied values; never string-interpolate them into Cypher.

## Backend Differences (operational, not query)

| Aspect | FalkorDB (primary) | Neo4j (secondary) |
| --- | --- | --- |
| Host | Redis module | Bolt server |
| graph_mcp tool | `db` param set to FalkorDB graph name | `db` param set to Neo4j DB name |
| Limits | Redis-backed; prefer small `LIMIT` | Can tolerate deeper traversal |

Keep traversal depth modest (≤5 hops) and always append `LIMIT` to bound the
result set — FalkorDB on Redis is less forgiving of unbounded traversals than
Neo4j.
