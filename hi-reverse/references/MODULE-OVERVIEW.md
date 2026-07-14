# Module Overview

Generate a concise architectural orientation for one module after discovery saturation.

## Retrieval

1. Consolidate module identity, responsibilities, boundaries, actors, entry points, outputs, external systems, and runtime context from the discovery manifest and module map.
2. Query Graph-RAG for startup, shutdown, state ownership, adapters, side effects, and neighboring modules.
3. Use Serena only to confirm module-level declarations, configuration, and line references.
4. Reject responsibilities inferred only from filenames or class names.

## Output

Write `module-overview.md` using the registered template. Distinguish in-scope responsibilities, delegated responsibilities, and explicitly out-of-scope behavior. Include evidence and unresolved gaps.
