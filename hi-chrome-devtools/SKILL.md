---
name: hi-chrome-devtools
description: Browser automation via Puppeteer CLI scripts with persistent sessions. Screenshots, performance, network, scraping, form automation, auth, debugging.
license: Apache-2.0
argument-hint: "[url or task]"
metadata:
  author: baka3k
  version: "2.1.0"
---

# Chrome DevTools Agent Skill

All examples and advanced patterns: [usage.md](references/usage.md). Deep references: `references/cdp-domains.md`, `references/puppeteer-reference.md`, `references/performance-guide.md`, `scripts/README.md`.

## Resolve Skill Directory

`$SKILL_DIR` = first existing `scripts` dir among: `./.agents/skills/hi-chrome-devtools` → `./.claude/skills/chrome-devtools` → `./hi-chrome-devtools` → `~/.agents/skills/hi-chrome-devtools` → `~/.claude/skills/chrome-devtools`. Missing → error.

## Setup

`"$SKILL_DIR/install.sh"` (auto-detects OS + dependencies; manual: `install-deps.sh` then `npm install`). Headless auto-resolves: macOS/Windows headed, Linux/WSL/CI headless; override `--headless true|false`. All scripts support `--headless`, `--close true`, `--timeout 30000`, `--wait-until networkidle2`.

## Session Persistence

State persists in `.browser-session.json`; scripts disconnect but keep the browser running; `--close true` (or `closeBrowser()`) ends it.

## Scripts

| Script | Purpose |
|--------|---------|
| `navigate.js` | Navigate to URLs |
| `screenshot.js` | Screenshots (auto-compress >5MB) |
| `click.js` / `fill.js` | Click elements / fill fields |
| `evaluate.js` | Execute JS in page context |
| `snapshot.js` | Extract interactive elements (JSON) |
| `aria-snapshot.js` | ARIA accessibility tree (YAML + refs) |
| `select-ref.js` | Interact by ref from ARIA snapshot |
| `console.js` / `network.js` | Console messages / HTTP traffic |
| `performance.js` | Core Web Vitals |
| `ws-debug.js` / `ws-full-debug.js` | WebSocket debugging |
| `inject-auth.js` / `import-cookies.js` | Cookie/token auth |
| `connect-chrome.js` | Attach to running Chrome (port 9222) |

## Core Loop (unknown page)

1. `node "$SKILL_DIR/aria-snapshot.js" --url <url>` — snapshot.
2. Identify target from YAML (`[ref=eN]`).
3. `node "$SKILL_DIR/select-ref.js" --ref eN --action click|fill|text|screenshot`.
4. `node "$SKILL_DIR/screenshot.js" --output ./result.png` — verify.

## Auth Methods

| Method | Best for |
|--------|----------|
| Inject cookies | Simple session cookies, API tokens |
| Import from browser | Multi-cookie auth, OAuth tokens |
| Chrome profile | 2FA, SSO, complex OAuth (Chrome closed first) |
| Connect to Chrome | Debugging, visual verification |
| Interactive login | OAuth/SSO with manual interaction (`--wait-for-login`) |

## Hard Rules

- Never `file://` for local HTML — serve via `npx serve` (CORS/modules/fetch/service workers).
- Custom scripts: single-purpose, always `disconnectBrowser()`, plain JS only in `page.evaluate()`.
- Never commit `.browser-session.json`, `.auth-session.json`, cookies, or tokens.
