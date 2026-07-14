# Use-Case Profile

Use this profile when the user requests one or more behavioral use cases rather than a complete module or migration package.

## Required Artifacts

Once per target module:

- discovery manifest with condition evidence and retained candidates

For every documented use case:

- use-case document
- trace manifest
- sequence diagram
- class diagram

Add an activity diagram when material branching is evidenced and the `branching` condition is active.

## Flow

1. Generate the artifact plan with every selected use-case slug.
2. Complete Graph-RAG discovery and tracing.
3. Generate the trace before either diagram.
4. Generate the sequence diagram from ordered trace evidence.
5. Generate the class diagram from types participating in that use case.
6. Link both diagrams from the use-case document.
7. Run the UC hook and package validator.

Do not mark a candidate as documented merely because it appears in the discovery manifest. A documented use case must pass the complete artifact gate.
