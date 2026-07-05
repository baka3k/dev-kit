# Root Cause Tracing

Systematically trace bugs backward through call stack to find original trigger. **Never fix just where error appears** — trace back to source, then add validation at every layer (see defense-in-depth.md).

**Use when:** error deep in execution, long call chain, unclear where invalid data originated, need to find which test triggers a problem.

## Trace Skeleton

```
1. Observe:        Error: <symptom> at <location>
2. Immediate cause: <code line that directly fails>
3. Call chain:     callee ← caller ← ... ← entry point
4. Bad value:      <param> = <unexpected value> ← where did it come from?
5. Original trigger: <test/setup that introduced the bad value>
```

## Adding Stack Traces

When manual tracing is hard, add instrumentation. **Use `console.error()` in tests** (logger may not show):

```typescript
async function gitInit(directory: string) {
  console.error('DEBUG git init:', { directory, cwd: process.cwd(), stack: new Error().stack });
  await execFileAsync('git', ['init'], { cwd: directory });
}
```

Capture: `npm test 2>&1 | grep 'DEBUG git init'`. Analyze for test file names, line numbers, recurring patterns.

## Finding Which Test Causes Pollution

Use `scripts/find-polluter.sh` (runs tests one-by-one, stops at first polluter):

```bash
./scripts/find-polluter.sh '.git' 'src/**/*.test.ts'
```

## Key Principle

**NEVER fix just where error appears.** Trace back to original trigger. Then add validation at every layer (see defense-in-depth.md).
