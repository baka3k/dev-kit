# Defense-in-Depth Validation

Validate at every layer data passes through to make bugs structurally impossible. Single check can be bypassed by different code paths, refactoring, or mocks — multiple layers make the bug impossible.

## Why Multiple Layers

| Single validation | Multiple layers |
|-------------------|-----------------|
| "We fixed bug" | "We made bug impossible" |

Different layers catch different cases: entry catches most, business logic catches edge cases, environment guards prevent context-specific dangers, debug logging helps when other layers fail.

## The Four Layers

| Layer | Purpose | Example |
|-------|---------|---------|
| 1. Entry point | Reject obviously invalid input at API boundary | `if (!workingDirectory \|\| !existsSync(workingDirectory)) throw …` |
| 2. Business logic | Ensure data makes sense for this operation | `if (!projectDir) throw new Error('projectDir required')` |
| 3. Environment guards | Prevent dangerous operations in specific contexts | `if (NODE_ENV==='test' && !isTmpDir(directory)) throw …` |
| 4. Debug instrumentation | Capture context for forensics | `logger.debug('About to git init', { directory, cwd, stack })` |

## Applying the Pattern

When you find a bug: (1) trace data flow to find where the bad value originates and where it's used, (2) map every checkpoint data passes through, (3) add validation at each of the four layers, (4) test each layer (try to bypass L1, verify L2 catches it).
