# Data Artifact Contract

Write `physical-erd.mmd`, `logical-erd.mmd`, `data-model.json`, `data-dictionary.md`, `ownership-access.md`, `lifecycle.md`, `schema-gaps.md`, `evidence-index.json`, and `artifact-manifest.json` when supported by scope.

Every entity and relationship declares its layer: `physical`, `orm`, `domain`, `dto`, `cache`, or `inferred`. Fields preserve declared type, nullability, default, key/index status, sensitivity, source revision, and evidence. Relationships preserve cardinality, constraint name when declared, inference status, and contradictions.

ERDs use stable sanitized IDs, a legend, text summary, evidence links, and omission notes. Split beyond 30 nodes or 80 edges. Ownership/access and lifecycle claims remain unknown without direct evidence. Validate the machine inventory against [data-output.schema.json](data-output.schema.json).
