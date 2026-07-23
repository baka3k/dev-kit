# Source Selection

Use the highest available source in this order:

1. Official versioned documentation or API reference.
2. Official release notes, changelog, specification, or repository.
3. Maintainer-authored examples or announcements.
4. Reputable secondary material when primary sources are incomplete.

## Capability Routing

| Target | Preferred capability |
| --- | --- |
| Official library, framework, or API documentation | **Context7 connector first** — `resolve-library-id`, then `query-docs` for the scoped topic. Fall back to official-site search if the library is not indexed or the answer is out of scope. |
| Known official page | Open and inspect the page directly |
| Current or broad topic | Search the web, restricted to official domains when practical |
| Official repository evidence | Search the repository, then open the exact file, release, or issue |
| Standard or protocol | Use the standards body, specification publisher, or original paper |
| Project-specific behavior | Search local project documents and code before external sources |

Context7 is the default for official library/framework/API docs because it indexes versioned, authoritative sources directly and scopes queries to one topic. Prefer it over broad web search when the target is a named library, framework, SDK, or public API. When it returns no match, switch to official-site search — do not retry the same connector on a different phrasing.

## Checks

- Match the requested version, runtime, language, and platform.
- Prefer a page that directly states the claim over an index or search result.
- Check publication or update dates for changing behavior.
- Use repository code as evidence only when documentation is missing; label the conclusion as code-derived.
- When sources conflict, prefer the source matching the requested version and explain the mismatch.

Avoid community posts, generated summaries, and archived pages when a current primary source exists.
