#!/usr/bin/env node
/**
 * Regenerate the agent manifest copies from AGENTS.md.
 *
 * AGENTS.md is the single source of truth. CLAUDE.md (Claude Code) and
 * .cursorrules (Cursor) are generated, because the installer ships only the
 * first two and the third would otherwise drift.
 *
 * Usage: node scripts/sync-manifests.mjs [--check]
 * Exit:  0 = files written (or already in sync with --check), 1 = drift with --check.
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CHECK = process.argv.includes("--check");
const TARGETS = ["CLAUDE.md", ".cursorrules"];
const NOTE = "Generated from AGENTS.md by scripts/sync-manifests.mjs — edit AGENTS.md, then run: node scripts/sync-manifests.mjs";

const source = readFileSync(resolve(ROOT, "AGENTS.md"), "utf8");

const render = (file) => {
  const header = file.endsWith(".md") ? `<!-- ${NOTE} -->\n\n` : `# ${NOTE}\n\n`;
  return header + source;
};

let drift = 0;
for (const file of TARGETS) {
  const path = resolve(ROOT, file);
  const next = render(file);
  const current = existsSync(path) ? readFileSync(path, "utf8") : null;
  if (current === next) {
    console.log(`  in sync  ${file}`);
    continue;
  }
  drift += 1;
  if (CHECK) {
    console.log(`  stale    ${file}`);
    continue;
  }
  writeFileSync(path, next, "utf8");
  console.log(`  written  ${file}`);
}

if (CHECK && drift) {
  console.error(`\n${drift} manifest(s) out of sync with AGENTS.md`);
  process.exit(1);
}
console.log(`\n${CHECK ? "manifests in sync" : `synced ${TARGETS.length} manifest(s) from AGENTS.md`}`);
