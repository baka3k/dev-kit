# Frontend Verification

Visual verification of frontend implementations using Chrome MCP (Claude Chrome Extension) or `hi:chrome-devtools` skill fallback.

**Skip entirely if NOT frontend-related.** Indicators: files `*.tsx/jsx/vue/svelte/html/css/scss`, changes to components/layouts/pages/styles/DOM, keywords render/display/layout/responsive/animation/visual/UI/UX.

## Step 1: Detect Chrome MCP

Use `ListMcpResourcesTool` to look for tools prefixed with `chrome__` (e.g., `chrome__navigate`, `chrome__screenshot`). Available → Step 2A; not available → Step 2B.

## Step 2A: Chrome MCP Available

Ensure dev server is running, then:

```
1. chrome__navigate → http://localhost:3000
2. chrome__screenshot → capture current page
3. Read the screenshot to inspect visually
4. chrome__evaluate → "JSON.stringify(window.__consoleErrors || [])"  # check console errors
5. chrome__click / chrome__type to test interactions
6. chrome__get_content to verify rendered DOM/text
```

Inspect for: layout (no overflow/overlap), content rendered correctly, responsiveness (resize viewport if supported), interactions work, zero console errors.

## Step 2B: Fallback to chrome-devtools Skill

```bash
SKILL_DIR="$HOME/.claude/skills/chrome-devtools/scripts"
npm install --prefix "$SKILL_DIR" 2>/dev/null
node "$SKILL_DIR/screenshot.js" --url http://localhost:3000 --output ./verification-screenshot.png
node "$SKILL_DIR/console.js" --url http://localhost:3000 --types error,pageerror --duration 5000
```

If `hi:chrome-devtools` also unavailable, skip and note in report: "Visual verification skipped — no Chrome MCP or chrome-devtools available."

## Step 3: Analyze Results

Read screenshot, check console output (zero errors = pass), compare with expected design, document findings (include screenshot path and any issues in the report).
