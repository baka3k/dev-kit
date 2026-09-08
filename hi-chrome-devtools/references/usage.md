# Chrome DevTools Usage Examples

Command examples for `hi-chrome-devtools`. `$SKILL_DIR` = the resolved scripts directory (see SKILL.md).

## Setup

```bash
# One-time setup
"$SKILL_DIR/install.sh"          # auto-detects OS, handles system dependencies
# Manual: "$SKILL_DIR/install-deps.sh" then npm install in scripts directory

# Test
node "$SKILL_DIR/navigate.js" --url https://example.com
# Output: {"success": true, "url": "...", "title": "..."}
```

## Session Persistence

Browser state persists via `.browser-session.json`; scripts disconnect but keep the browser running.

```bash
node "$SKILL_DIR/navigate.js" --url https://example.com/login   # first script launches browser
node "$SKILL_DIR/fill.js" --selector "#email" --value "user@example.com"
node "$SKILL_DIR/fill.js" --selector "#password" --value "secret"
node "$SKILL_DIR/click.js" --selector "button[type=submit]"
node "$SKILL_DIR/navigate.js" --url about:blank --close true    # close browser
```

## ARIA Snapshot

```bash
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com
node "$SKILL_DIR/aria-snapshot.js" --url https://example.com --output ./snapshots/page.yaml
```

YAML output example:

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

Ref notation: `[ref=eN]` stable id · `[checked]` selected · `[disabled]` inactive · `[expanded]` open · `/url:` link target · `/placeholder:` input placeholder.

```bash
node "$SKILL_DIR/select-ref.js" --ref e5 --action click
node "$SKILL_DIR/select-ref.js" --ref e10 --action fill --value "search query"
node "$SKILL_DIR/select-ref.js" --ref e8 --action text
node "$SKILL_DIR/select-ref.js" --ref e1 --action screenshot --output ./logo.png
```

## Screenshots

```bash
node "$SKILL_DIR/screenshot.js" --url https://example.com --output ./screenshots/page.png
node "$SKILL_DIR/screenshot.js" --url https://example.com --output ./page.png --full-page true
node "$SKILL_DIR/screenshot.js" --url https://example.com --selector ".main-content" --output ./element.png
```

Auto-compression via Sharp when >5MB; `--max-size N` (MB threshold), `--no-compress`.

Scroll-triggered images:

```bash
node "$SKILL_DIR/evaluate.js" --script "document.querySelector('.lazy-image').scrollIntoView()"
node "$SKILL_DIR/evaluate.js" --script "await new Promise(r => setTimeout(r, 1000))"
node "$SKILL_DIR/screenshot.js" --output ./result.png
node "$SKILL_DIR/evaluate.js" --script "window.scrollTo(0, document.body.scrollHeight)"
node "$SKILL_DIR/screenshot.js" --output ./full-loaded.png --full-page true
```

## Console & Network

```bash
node "$SKILL_DIR/console.js" --url https://example.com --duration 10000
node "$SKILL_DIR/console.js" --url https://example.com --types error,warn --duration 5000
node "$SKILL_DIR/console.js" --url https://example.com --types error,pageerror --duration 5000 | jq '.messages'
node "$SKILL_DIR/network.js" --url https://example.com | jq '.requests[] | select(.response.status >= 400)'
```

## Finding Elements

```bash
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | {tagName, text, selector}'
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | select(.tagName=="button")'
node "$SKILL_DIR/snapshot.js" --url https://example.com | jq '.elements[] | select(.text | contains("Submit"))'
```

## Common Patterns

```bash
# Scraping
node "$SKILL_DIR/evaluate.js" --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'

# Form automation
node "$SKILL_DIR/navigate.js" --url https://example.com/form
node "$SKILL_DIR/fill.js" --selector "#search" --value "query"
node "$SKILL_DIR/click.js" --selector "button[type=submit]"

# Performance
node "$SKILL_DIR/performance.js" --url https://example.com | jq '.vitals'

# Error recovery: capture state, console errors, find selector, XPath fallback
node "$SKILL_DIR/screenshot.js" --output ./screenshots/debug.png
node "$SKILL_DIR/console.js" --url about:blank --types error --duration 1000
node "$SKILL_DIR/snapshot.js" | jq '.elements[] | select(.text | contains("Submit"))'
node "$SKILL_DIR/click.js" --selector "//button[contains(text(),'Submit')]"
```

## Local HTML Files

Never use `file://` — it blocks CORS, ES modules, fetch, service workers. Serve locally:

```bash
npx serve ./dist -p 3000 &
node "$SKILL_DIR/navigate.js" --url http://localhost:3000
```

## Authentication Examples

```bash
# Inject cookies / token
node "$SKILL_DIR/inject-auth.js" --url https://site.com \
  --cookies '[{"name":"session","value":"abc123","domain":".site.com"}]'
node "$SKILL_DIR/inject-auth.js" --url https://api.site.com \
  --token "Bearer eyJhbG..." --header Authorization

# Import from Cookie-Editor export (JSON or Netscape)
node "$SKILL_DIR/import-cookies.js" --file ./cookies.json --url https://site.com
node "$SKILL_DIR/import-cookies.js" --file ./cookies.txt --format netscape --url https://site.com
node "$SKILL_DIR/import-cookies.js" --file ./cookies.json --url https://site.com --strict-domain

# Chrome profile (Chrome must be closed for default profile)
node "$SKILL_DIR/navigate.js" --url https://site.com --use-default-profile true
node "$SKILL_DIR/navigate.js" --url https://site.com --profile "/path/to/chrome/profile"
# Profile paths: macOS ~/Library/Application Support/Google/Chrome · Windows %LOCALAPPDATA%\Google\Chrome\User Data · Linux ~/.config/google-chrome

# Connect to running Chrome (launch Chrome with --remote-debugging-port=9222 first)
node "$SKILL_DIR/connect-chrome.js" --browser-url http://localhost:9222 --url https://site.com
node "$SKILL_DIR/connect-chrome.js" --launch --port 9222 --url https://site.com

# Interactive login (OAuth/SSO) — headed browser, manual login, cookies saved to .auth-session.json (24h)
node "$SKILL_DIR/navigate.js" --url https://app.example.com/login --wait-for-login "/dashboard"
node "$SKILL_DIR/navigate.js" --url https://app.example.com/login --wait-for-login "/dashboard" --login-timeout 600000
```

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

Key rules: single-purpose, always `disconnectBrowser()`, `closeBrowser()` only to end the session, plain JS only in `page.evaluate()`.

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Cannot find package 'puppeteer'` | `npm install` in scripts directory |
| `libnss3.so` missing (Linux) | Run `./install-deps.sh` |
| Element not found | Use `snapshot.js` |
| Script hangs | `--timeout 60000` or `--wait-until load` |
| Screenshot >5MB | Auto-compressed; `--max-size 3` for lower |
| Session stale | Delete `.browser-session.json` and retry |
