# Jev AI — Query Reference

How to actually ask Jev a question: no CLI, query the HTTP API directly.
Full skill guide: [SKILL.md](SKILL.md) · Live docs: https://docs.typesafe.ai/llms.txt

## Minimal query (curl)

```bash
curl -s -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "<context the judgment needs>",
    "model": "jev-latest",
    "questions": {
      "q": {"type": "noul", "instructions": "<yes/no question>"}
    }
  }'
```

- Auth: `Authorization: Bearer $TYPESAFE_API_KEY` (exported in `~/.zshrc`).
- Response: `{"model": "jev-...", "answers": {"q": {"type": "noul", "noul": 0.95}}, "usage": {...}}` — read the answer under the same question id you sent.

## Primitives

| Need | Type | Returns |
| --- | --- | --- |
| Pick one of a defined set | `choice` | selected option + confidence/distribution |
| Whether a condition holds | `noul` | probability 0..1 |
| Degree along a described dimension | `score` | probability-weighted level |

Rules of thumb: one narrow judgment per question; put the judgment in `instructions`, define possible answers in `criteria`; give enough `state`; batch independent questions over the same state into one request (they run in parallel).
