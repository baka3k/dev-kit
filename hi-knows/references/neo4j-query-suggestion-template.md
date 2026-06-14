```text
Neo4j Query Suggestion:
- Mục tiêu:
- Vì sao:
- Cypher:
- Kỳ vọng:
- Diễn giải:
```

## Patterns

- **Callers:** `MATCH (caller)-[:CALLS*1..4]->(target {name: $name}) RETURN caller.name, target.name LIMIT 200;`
- **Downstream:** `MATCH p=(start {name: $name})-[:CALLS|USES|DEPENDS_ON*1..5]->(n) RETURN p LIMIT 100;`
- **Workflows:** `MATCH (w:Workflow)-[:HAS_STEP]->(f {symbol_id: $id}) RETURN w.name, f.name LIMIT 100;`
