# Retrieval Playbook

## Validation
- Block path traversal: `../`, `..\\`
- Query length: 1000 chars max
- Sanitize: `;`, `|`, `&`, `$`
- Validate commit hash: `/^[a-f0-9]{7,40}$/`

## Fallback

| Failure | Fallback | Confidence |
|---------|----------|------------|
| mind_mcp | Git + graph + memory | medium |
| graph_mcp | Git + mind + memory | medium |
| Both MCP | Git + memory only | low |

Always notify user of degraded mode with specific missing evidence.
