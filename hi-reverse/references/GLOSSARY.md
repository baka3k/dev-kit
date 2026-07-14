# Domain Glossary

Build a Japanese/romaji/English-to-code glossary for `<MODULE>` from Graph-RAG and source evidence. Read `GRAPH-RAG-PROTOCOL.md` first.

## Retrieval

1. Seed terms from allowed knowledge Graph-RAG, user wording, semantic query analysis, comments, symbols, states, messages, and use-case candidates.
2. Query each concept as Japanese, romaji variants, English business terms, abbreviations, and observed code prefixes with `semantic_search(expand_graph:false)`.
3. Pair each semantic query with `explore_graph` to retrieve contextual symbols, relationships, paths, and WHY evidence from FalkorDB.
4. Query high-value term anchors for callers/triggers, callees/outcomes, states, messages, and neighboring modules to distinguish business meaning from utilities and homonyms.
5. After Graph-RAG saturation, use Serena patterns and symbol bodies to confirm comments, enum/state meanings, message constants, and ambiguous abbreviations.
6. Repeat with discovered synonyms until two passes add no term, mapping, or context.

Do not preload a generic business glossary as fact. Query seeds enter the output only when this module supplies evidence.

## Output

Write `usecase/<MODULE>/glossary.md`:

| Japanese | Romaji | English | Code symbols | Context/use case | Evidence | Confidence |
|---|---|---|---|---|---|---|

Append the Falkor Graph gate, retrieval trace, rejected homonyms, saturation result, and unresolved translations.
