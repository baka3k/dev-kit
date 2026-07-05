# Chrome DevTools Scripts

CLI scripts for browser automation using Puppeteer. Requires **Node.js >= 18**. All scripts output JSON to stdout.

## Installation

```bash
# From the scripts directory:
./install.sh
```

Or manually:

```bash
# Linux/WSL: install system dependencies first
./install-deps.sh

# Then install Node packages
npm install
```

Dependencies: `puppeteer`, `sharp`, `yargs`, `debug`.

## Scripts

All scripts support: `--headless true/false`, `--close true`, `--timeout 30000`, `--wait-until networkidle2`.

### navigate.js

```bash
node navigate.js --url https://example.com [--wait-until networkidle2] [--timeout 30000]
```

Additional options:
- `--wait-for-login <pattern>` — Interactive login: open headed, wait for URL regex match
- `--login-timeout <ms>` — Max wait for login (default: 300000 = 5 min)

### screenshot.js

```bash
node screenshot.js --output screenshot.png [--url https://example.com] [--full-page true] [--selector .element]
node screenshot.js --output screenshot.png --max-size 3   # custom threshold (MB)
node screenshot.js --output screenshot.png --no-compress   # disable compression
```

Screenshots >5MB auto-compress via Sharp.

### click.js

```bash
node click.js --selector ".button" [--url https://example.com] [--wait-for ".result"]
```

### fill.js

```bash
node fill.js --selector "#input" --value "text" [--url https://example.com] [--clear true]
```

### evaluate.js

```bash
node evaluate.js --script "document.title" [--url https://example.com]
```

### snapshot.js

```bash
node snapshot.js [--url https://example.com] [--output snapshot.json]
```

Discover selectors before interacting:
```bash
node snapshot.js --url https://example.com | jq '.elements[]'
node snapshot.js --url https://example.com | jq '.elements[] | select(.tagName=="BUTTON")'
node snapshot.js --url https://example.com | jq '.elements[] | select(.tagName=="INPUT")'
```

### aria-snapshot.js

```bash
node aria-snapshot.js --url https://example.com
node aria-snapshot.js --url https://example.com --output ./snapshots/page.yaml
```

### select-ref.js

```bash
node select-ref.js --ref e5 --action click
node select-ref.js --ref e10 --action fill --value "search query"
node select-ref.js --ref e8 --action text
node select-ref.js --ref e1 --action screenshot --output ./logo.png
```

### console.js

```bash
node console.js --url https://example.com [--types error,warn] [--duration 5000]
```

### network.js

```bash
node network.js --url https://example.com [--types xhr,fetch] [--output requests.json]
```

### performance.js

```bash
node performance.js --url https://example.com [--trace trace.json] [--metrics] [--resources true]
```

### ws-debug.js / ws-full-debug.js

```bash
node ws-debug.js       # basic WebSocket events
node ws-full-debug.js  # full event/frame tracking
```

### inject-auth.js

```bash
# Inject cookies
node inject-auth.js --url https://example.com --cookies '[{"name":"session","value":"abc","domain":".example.com"}]'

# Bearer token
node inject-auth.js --url https://example.com --token "Bearer eyJhbG..."" --header Authorization

# localStorage/sessionStorage
node inject-auth.js --url https://example.com --local-storage '{"auth_token":"xyz"}'
node inject-auth.js --url https://example.com --session-storage '{"temp_key":"value"}'

# Combined
node inject-auth.js --url https://example.com --cookies '[...]' --local-storage '{"user":"data"}' --reload true

# Clear auth
node inject-auth.js --url https://example.com --cookies '[]' --clear true
```

Auth saved to `.auth-session.json` (24h) and auto-applied by subsequent scripts.

### import-cookies.js

```bash
node import-cookies.js --file ./cookies.json --url https://site.com
node import-cookies.js --file ./cookies.txt --format netscape --url https://site.com
node import-cookies.js --file ./cookies.json --url https://site.com --strict-domain
```

### connect-chrome.js

```bash
# Connect to Chrome with remote debugging (port 9222)
node connect-chrome.js --browser-url http://localhost:9222 --url https://site.com

# Launch Chrome automatically
node connect-chrome.js --launch --port 9222 --url https://site.com
```

## Selector Support

Scripts with `--selector` support both CSS and XPath (automatically detected).

### CSS

```bash
node click.js --selector "button"
node click.js --selector ".btn-submit"
node fill.js --selector "#email" --value "user@example.com"
node click.js --selector 'button[type="submit"]'
```

### XPath

XPath starts with `/` or `(//`:

```bash
node click.js --selector '//button[text()="Submit"]'
node click.js --selector '//button[contains(text(),"Submit")]'
node fill.js --selector '//input[@type="email"]' --value "user@example.com"
node click.js --selector '(//button)[2]'
```

XSS injection blocked: `javascript:`, `<script`, `onerror=`, `eval(`, `Function(`, `constructor(`. Max 1000 chars.

## Output Format

stdout:
```json
{ "success": true, "url": "https://example.com", "title": "Example Domain" }
```

stderr:
```json
{ "success": false, "error": "Error message", "stack": "..." }
```
