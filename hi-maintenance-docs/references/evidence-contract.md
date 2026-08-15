# Evidence Contract

Each evidence record contains `id`, repository-relative `source_path`, optional line/symbol/node anchor, repository/project/database/collection identity, retrieval layer, claim type and relation, status, confidence, source revision, verification time, and coverage, contradiction, omission, or redaction notes.

Allowed retrieval layers are `mind`, `graph-semantic`, `graph-verified`, `serena`, and `rg`. Allowed statuses are `verified`, `corroborated`, `inferred`, `unknown`, and `contradicted`. A verified or corroborated claim requires at least one resolvable source reference. Semantic-only evidence cannot produce verified status.

Stable IDs are reused across use-case, behavior, API, data, and system artifacts. Conflicts remain separate records linked by a contradiction ID. Wrong-project results are rejected, warned, and never counted toward coverage.
