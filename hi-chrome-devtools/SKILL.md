---
name: hi-chrome-devtools
description: Browser automation via Puppeteer CLI scripts with persistent sessions. Screenshots, performance, network, scraping, form automation, auth, debugging.
license: Apache-2.0
argument-hint: "[url or task]"
metadata:
  author: baka3k
  version: "2.0.0"
---

# Chrome DevTools Agent Skill

## Skill Location

Skills can exist in **project-scope** (`./claude/skills/`) or **user-scope** (`~/.claude/skills/`). Priority: project > user.

```bash
SKILL_DIR=""
if [ -d ".claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR=".claude/skills/chrome-devtools/scripts"
elif [ -d "$HOME/.claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR="$HOME/.claude/skills/chrome-devtools/scripts"
fi
```

## Quick Start

```bash
# One-time setup
"$SKILL_DIR/install.sh"

# Test
node "$SKILL_DIR/navigate.js" --url https://example.com
# Output: {"success": true, "url": "...", "title": "..."}
```

`install.sh` auto-detects OS and handles system dependencies. For manual setup: `"$SKILL_DIR/install-deps.sh"` then `npm install` in the scripts directory.

## Headless Mode

Resolved automatically by `lib/browser.js`:

| Environment | Default |
|-------------|---------|
| macOS / Windows | Headed (visible) |
| Linux / WSL | Headless |
| CI (`CI`, `GITHUB_ACTIONS`, etc.) | Headless |

Override: `--headless true` or `--headless false`.

## Session Persistence

Browser state persists via `.browser-session.json`. Scripts disconnect but keep browser running.

```bash
# First script launches browser, then disconnects (browser stays)
node "$SKILL_DIR/navigate.js" --url https://example.com/login

# Subsequent scripts reuse the session
node "$SKILL_DIR/fill.js" --selector "#email" --value "user@example.com"
node "$SKILL_DIR/fill.js" --selector "#password" --value "secret"
node "$SKILL_DIR/click.js" --selector "button[type=submit]"

# Close browser
node "$SKILL_DIR/navigate.js" --url about:blank --close true
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `navigate.js` | Navigate to URLs |
| `screenshot.js` | Capture screenshots (auto-compress >5MB via Sharp) |
| `click.js` | Click elements |
| `fill.js` | Fill form fields |
| `evaluate.js` | Execute JS in page context |
| `snapshot.js` | Extract interactive elements (JSON) |
| `aria-snapshot.js` | ARIA accessibility tree (YAML with refs) |
| `select-ref.js` | Interact by ref from ARIA snapshot |
| `console.js` | Monitor console messages/errors |
| `network.js` | Track HTTP requests/responses |
| `performance.js` | Measure Core Web Vitals |
| `ws-debug.js` | WebSocket connection debugging |
| `ws-full-debug.js` | WebSocket full event/frame debugging |
| `inject-auth.js` | Inject cookies/tokens |
| `import-cookies.js` | Import cookies from JSON/Netscape |
| `connect-chrome.js` | Connect to Chrome via remote debugging |

All scripts support: `--headless true/false`, `--close true`, `--timeout 30000`, `--wait-until networkidle2`.

## ARIA Snapshot (Element Discovery)

```bash
# Get snapshot to stdout
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com

# Save to file
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com --output ./snapshots/page.yaml
```

### YAML Output (Example)

```yaml
- banner:
  - link "Hacker News" [ref=e1]
    /url: https://news.ycombinator.com
  - navigation:
    - link "new" [ref=e2]
- main:
  - list:
    - listitem:
      - link "Show HN" [ref=e8]
      - text: "128 points"
```

### Ref Notation

| Notation | Meaning |
|----------|---------|
| `[ref=eN]` | Stable identifier |
| `[checked]` | Checkbox/radio selected |
| `[disabled]` | Element inactive |
| `[expanded]` | Accordion/dropdown open |
| `/url:` | Link destination |
| `/placeholder:` | Input placeholder |

### Interact by Ref

```bash
node "$SKILL_DIR/select-ref.js" --ref e5 --action click
node "$SKILL_DIR/select-ref.js" --ref e10 --action fill --value "search query"
node "$SKILL_DIR/select-ref.js" --ref e8 --action text
node "$SKILL_DIR/select-ref.js" --ref e1 --action screenshot --output ./logo.png
```

### Unknown Page Workflow

1. **Snapshot**: `node "$SKILL_DIR/aria-snapshot.js" --url https://example.com`
2. **Identify** target from YAML (e.g., `[ref=e5]`)
3. **Interact**: `node "$SKILL_DIR/select-ref.js" --ref e5 --action click`
4. **Verify**: `node "$SKILL_DIR/screenshot.js" --output ./result.png`

## Screenshots

```bash
# Basic
node "$SKILL_DIR/screenshot.js" --url https://example.com --output ./screenshots/page.png

# Full page
node "$SKILL_DIR/screenshot.js" --url https://example.com --output ./screenshots/page.png --full-page true

# Element
node "$SKILL_DIR/screenshot.js" --url https://example.com --selector ".main-content" --output ./screenshots/element.png
```

Auto-compression via Sharp when >5MB. Options: `--max-size N` (threshold in MB), `--no-compress`.

## Console Logs

```bash
# Capture with duration
node "$SKILL_DIR/console.js" --url https://example.com --duration 10000

# Filter by type
node "$SKILL_DIR/console.js" --url https://example.com --types error,warn --duration 5000

# Root cause analysis
node "$SKILL_DIR/console.js" --url https://example.com --types error,pageerror --duration 5000 | jq '.messages'
node "$SKILL_DIR/network.js" --url https://example.com | jq '.requests[] | select(.response.status >= 400)'
```

## Finding Elements

```bash
# All interactive elements
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | {tagName, text, selector}'

# Buttons only
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | select(.tagName=="button")'

# By text
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | select(.text | contains("Submit"))'
```

## Common Patterns

### Web Scraping
```bash
node "$SKILL_DIR/evaluate.js" --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'
```

### Form Automation
```bash
node "$SKILL_DIR/navigate.js" --url https://example.com/form
node "$SKILL_DIR/fill.js" --selector "#search" --value "query"
node "$SKILL_DIR/click.js" --selector "button[type=submit]"
```

### Performance Testing
```bash
node "$SKILL_DIR/performance.js" --url https://example.com | jq '.vitals'
```

## Error Recovery

```bash
# Capture current state
node "$SKILL_DIR/screenshot.js" --output ./screenshots/debug.png

# Console errors
node "$SKILL_DIR/console.js" --url about:blank --types error --duration 1000

# Find correct selector
node "$SKILL_DIR/snapshot.js" | jq '.elements[] | select(.text | contains("Submit"))'

# XPath fallback
node "$SKILL_DIR/click.js" --selector "//button[contains(text(),'Submit')]"
```

## Local HTML Files

Never use `file://` — it blocks CORS, ES modules, fetch, service workers. Serve locally:

```bash
npx serve ./dist -p 3000 &
node "$SKILL_DIR/navigate.js" --url http://localhost:3000
```

## Authentication

### Method Comparison

| Method | Best For |
|--------|----------|
| **Inject cookies** | Simple session cookies, API tokens |
| **Import from browser** | Multi-cookie auth, OAuth tokens |
| **Chrome profile** | 2FA, SSO, complex OAuth* |
| **Connect to Chrome** | Debugging, visual verification |
| **Interactive login** | OAuth/SSO with manual interaction |

*Requires Chrome to be closed first.

### Inject Cookies
```bash
node "$SKILL_DIR/inject-auth.js" --url https://site.com \
  --cookies '[{"name":"session","value":"abc123","domain":".site.com"}]'

node "$SKILL_DIR/inject-auth.js" --url https://api.site.com \
  --token "Bearer eyJhbG..." --header Authorization
```

### Import from Browser Extension
```bash
# Export from Cookie-Editor extension → cookies.json
node "$SKILL_DIR/import-cookies.js" --file ./cookies.json --url https://site.com

# Netscape format
node "$SKILL_DIR/import-cookies.js" --file ./cookies.txt --format netscape --url https://site.com

# Strict domain filtering
node "$SKILL_DIR/import-cookies.js" --file ./cookies.json --url https://site.com --strict-domain
```

### Use Chrome Profile
```bash
node "$SKILL_DIR/navigate.js" --url https://site.com --use-default-profile true
node "$SKILL_DIR/navigate.js" --url https://site.com --profile "/path/to/chrome/profile"
```

Profile paths: macOS (`~/Library/Application Support/Google/Chrome`), Windows (`%LOCALAPPDATA%/Google/Chrome/User Data`), Linux (`~/.config/google-chrome`).

### Connect to Running Chrome
```bash
# Launch Chrome with remote debugging:
#   macOS:  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
#   Windows: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
#   Linux:   google-chrome --remote-debugging-port=9222

node "$SKILL_DIR/connect-chrome.js" --browser-url http://localhost:9222 --url https://site.com
node "$SKILL_DIR/connect-chrome.js" --launch --port 9222 --url https://site.com
```

### Interactive Login (OAuth/SSO)
```bash
node "$SKILL_DIR/navigate.js" --url https://app.example.com/login --wait-for-login "/dashboard"
node "$SKILL_DIR/navigate.js" --url https://app.example.com/login --wait-for-login "/dashboard" --login-timeout 600000
```

Opens headed browser, waits for manual login, saves cookies to `.auth-session.json` (24h reuse).

## Custom Scripts

For complex automation, write to `<project>/.claude/chrome-devtools/tmp/`:

```javascript
import { getBrowser, getPage, disconnectBrowser, outputJSON } from '../scripts/lib/browser.js';

async function myTask() {
  const browser = await getBrowser();
  const page = await getPage(browser);

  await page.goto('https://example.com');
  outputJSON({ success: true, title: await page.title() });

  await disconnectBrowser(); // keeps browser running
}
myTask();
```

Key rules: single-purpose, always call `disconnectBrowser()`, use `closeBrowser()` only to end session, plain JS only in `page.evaluate()`.

## Screenshot Troubleshooting

If images don't appear — they may be waiting for scroll/animation triggers:

```bash
# Scroll-triggered images
node "$SKILL_DIR/evaluate.js" --script "document.querySelector('.lazy-image').scrollIntoView()"
node "$SKILL_DIR/evaluate.js" --script "await new Promise(r => setTimeout(r, 1000))"
node "$SKILL_DIR/screenshot.js" --output ./result.png

# Intersection Observer
node "$SKILL_DIR/evaluate.js" --script "window.scrollTo(0, document.body.scrollHeight)"
node "$SKILL_DIR/evaluate.js" --script "await new Promise(r => setTimeout(r, 1500))"
node "$SKILL_DIR/evaluate.js" --script "window.scrollTo(0, 0)"
node "$SKILL_DIR/screenshot.js" --output ./full-loaded.png --full-page true
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Cannot find package 'puppeteer'` | `npm install` in scripts directory |
| `libnss3.so` missing (Linux) | Run `./install-deps.sh` |
| Element not found | Use `snapshot.js` |
| Script hangs | Use `--timeout 60000` or `--wait-until load` |
| Screenshot >5MB | Auto-compressed; use `--max-size 3` for lower |
| Session stale | Delete `.browser-session.json` and retry |

## Reference Documentation

- `./references/cdp-domains.md` — Chrome DevTools Protocol domains
- `./references/puppeteer-reference.md` — Puppeteer API patterns
- `./references/performance-guide.md` — Core Web Vitals optimization
- `./scripts/README.md` — Detailed script options
