# Context7 Lookup

Use Context7 to retrieve official, versioned documentation for a named library, framework, SDK, or public API. It is the default first step for official documentation because it scopes queries to authoritative sources and avoids generic web noise.

## When to use

- A named library, framework, SDK, runtime, or public API is the target (e.g. Next.js, Django, React, Express, PyTorch).
- The request needs API details, configuration, version behavior, or migration steps from official docs.
- You want to avoid community posts, generated summaries, and stale mirrors.

Do not use Context7 for: project-specific behavior, standards/protocols, or topics that are not tied to a published library (e.g. custom internal services). Use local sources or official-site search instead.

## Procedure

### 1. Resolve the library ID

Call `mcp__context7__resolve-library-id` with the `libraryName` and a scoped `query`.

- `libraryName`: the official product name with proper punctuation (e.g. `Next.js`, not `nextjs`; `Customer.io`, not `customerio`).
- `query`: the specific question or topic — this ranks candidate matches by relevance.

Pick the result with the best match on name, source reputation, and code-snippet coverage. Accept a `/org/project` or `/org/project/version` ID. If the user named a version, prefer a versioned ID when available.

### 2. Query the documentation

Call `mcp__context7__query-docs` with the resolved `libraryId` and a single-topic `query`.

- One concept per call. Split multi-concept questions into separate calls rather than combining them.
- Scope the query to the exact need (e.g. `how to set up JWT authentication in Express.js`), not a broad term like `auth`.
- Do not include secrets, credentials, API keys, or proprietary code in the query.

If the topic is version-sensitive and a versioned ID was resolved, use it. Otherwise rely on the default (current) docs and verify the version against release notes when it matters.

## Handling results

- Treat returned snippets as official-source evidence. Attach the library ID and topic to the answer so the claim is traceable.
- Cap calls: at most three `query-docs` calls per question. If you cannot find the answer by then, fall back to official-site search and report the gap.
- If `resolve-library-id` returns no usable match, fall back to official-site search. Do not retry the connector with rephrased names.
- Cross-check version-sensitive, conflicting, or high-impact claims against release notes or the official repository.

## Fallback order

1. Context7 (`resolve-library-id` → `query-docs`).
2. Official-site search on the product domain.
3. Official repository (docs folder, releases, tags).
4. Web search restricted to official domains, only if the above are incomplete.
