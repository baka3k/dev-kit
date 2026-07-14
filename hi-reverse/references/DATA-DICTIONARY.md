# Data Dictionary

Generate the data dictionary when the `persistence` condition is active or the user requests data semantics.

## Retrieval

1. Inventory business structs, classes, enums, flags, records, messages, shared-memory objects, persistent files, and database fields.
2. Record type, width, signedness, units, valid range, encoding, default, ownership, lifetime, mutability, persistence, and serialization.
3. Trace reads, writes, transformations, and state effects for high-value fields.
4. Use Serena declarations and bodies only after Graph-RAG identifies relevant types and fields.
5. Separate proven semantics from name-based hypotheses.

Write `data-dictionary.md`. Highlight layout, encoding, and ownership behavior that can affect migration parity.
