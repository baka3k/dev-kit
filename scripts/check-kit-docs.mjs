#!/usr/bin/env node
/**
 * Documentation drift checker for dev-kit.
 *
 * Verifies that README.md, devkit.md, the manifests, and wiki/ still match the
 * real skill tree. Run with `make check-docs`, or `make doctor` (which includes it).
 *
 * Usage: node scripts/check-kit-docs.mjs [--json]
 * Exit:  0 = every rule passed, 1 = at least one finding.
 */

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, dirname, resolve, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const JSON_OUT = process.argv.includes("--json");

const README = "README.md";
const DEVKIT = "devkit.md";
const AGENTS = "AGENTS.md";
const GENERATED = ["CLAUDE.md", ".cursorrules"];

const SUPPORT_PACKAGE = "dev-shared";
const SKIP_DIRS = new Set([".git", "node_modules", ".serena", ".commandcode"]);
/** Scaffolding, not documentation: templates contain placeholder targets on purpose. */
const SKIP_MARKDOWN_DIRS = new Set(["assets", "templates"]);

/** Illustrative paths used as examples inside templates and guides. */
const LINK_ALLOWLIST = new Set([
  "phase-01-setup.md",
  "phase-01-name.md",
  "system/system-overview.md",
]);

const read = (p) => readFileSync(join(ROOT, p), "utf8");
const listDir = (p) => readdirSync(join(ROOT, p), { withFileTypes: true });

/** Legacy deep-dive pages written before scripts/gen-wiki-pages.mjs existed. They keep their own
 *  structure; only generated pages are held to the generator's template. Migrate pages out of this
 *  list as they are regenerated. */
const HAND_WRITTEN_WIKI = new Set([
  "wiki/en/agents-md-guide.md",
  "wiki/vi/agents-md-guide.md",
  ...[
    "hi-craft",
    "hi-debug",
    "hi-docs-seeker",
    "hi-fix",
    "hi-knows",
    "hi-log",
    "hi-plan",
    "hi-predict",
    "hi-problem-solving",
    "hi-project-organization",
    "hi-reverse",
    "hi-scenario",
    "hi-security",
    "hi-sequential-thinking",
    "slide-kit",
  ].flatMap((skill) => [`wiki/en/${skill}-skill.md`, `wiki/vi/${skill}-skill.md`]),
]);

function skillDirs() {
  return listDir(".")
    .filter((e) => e.isDirectory() && !SKIP_DIRS.has(e.name) && existsSync(join(ROOT, e.name, "SKILL.md")))
    .map((e) => e.name)
    .sort();
}

function walkMarkdown(dir = ".", out = []) {
  for (const entry of listDir(dir)) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || SKIP_MARKDOWN_DIRS.has(entry.name)) continue;
      walkMarkdown(dir === "." ? entry.name : join(dir, entry.name), out);
      continue;
    }
    if (entry.name.endsWith(".md")) out.push(dir === "." ? entry.name : join(dir, entry.name));
  }
  return out;
}

function section(text, heading, stop = /^## /) {
  const lines = text.split("\n");
  const start = lines.findIndex((l) => l.trim() === heading);
  if (start === -1) return "";
  const body = [];
  for (let i = start + 1; i < lines.length; i += 1) {
    if (stop.test(lines[i])) break;
    body.push(lines[i]);
  }
  return body.join("\n");
}

function tableRows(block) {
  return block.split("\n").filter((l) => l.startsWith("|") && !/^\|\s*-+/.test(l));
}

function frontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  return m ? m[1] : null;
}

const rules = [];
const rule = (name, run) => rules.push({ name, run });

rule("catalog-complete", () => {
  const body = section(read(README), "## What Is Included");
  const findings = [];
  const rows = [...body.matchAll(/^\|\s*`([a-z0-9-]+)\/`\s*\|\s*`([a-z0-9-]+)`\s*\|/gm)];
  if (!rows.length) return ["README catalog rows not found"];
  const listed = new Set();
  for (const [, dir, name] of rows) {
    listed.add(dir);
    if (!existsSync(join(ROOT, dir, "SKILL.md"))) {
      findings.push(`README catalog lists \`${dir}/\`, which has no SKILL.md`);
      continue;
    }
    const declared = frontmatter(read(join(dir, "SKILL.md")))?.match(/^name:\s*(.+)$/m)?.[1]?.trim();
    if (declared !== name) {
      findings.push(`README catalog maps \`${dir}/\` to \`${name}\`, frontmatter says \`${declared}\``);
    }
  }
  for (const dir of skillDirs()) {
    if (!listed.has(dir)) findings.push(`skill dir \`${dir}/\` is missing from the README catalog`);
  }
  return findings;
});

rule("catalog-count", () => {
  const m = read(README).match(/(\d+)\s+composable skills/);
  if (!m) return ["README no longer states a skill count"];
  const expected = skillDirs().filter((d) => d !== SUPPORT_PACKAGE).length;
  return Number(m[1]) === expected
    ? []
    : [`README claims ${m[1]} skills, tree has ${expected}`];
});

rule("no-duplicate-heading", () => {
  const findings = [];
  for (const file of [README, DEVKIT]) {
    const seen = new Map();
    read(file)
      .split("\n")
      .filter((l) => /^#{2,3} /.test(l))
      .map((l) => l.trim())
      .forEach((h) => {
        seen.set(h, (seen.get(h) ?? 0) + 1);
      });
    for (const [h, n] of seen) {
      if (n > 1) findings.push(`${file}: heading \`${h}\` appears ${n} times`);
    }
  }
  return findings;
});

rule("tree-matches", () => {
  const body = section(read(README), "## Folder Structure");
  const block = body.match(/```text\n([\s\S]*?)```/);
  if (!block) return ["README Folder Structure block not found"];
  const entries = [...block[1].matchAll(/^[├└]── ([A-Za-z0-9._/-]+?)(\/)?\s*(?:#.*)?$/gm)];
  const findings = [];
  const listedDirs = new Set();
  for (const [, name, isDir] of entries) {
    if (!existsSync(join(ROOT, name))) {
      findings.push(`README tree lists \`${name}${isDir ? "/" : ""}\`, which does not exist`);
      continue;
    }
    if (isDir) listedDirs.add(name);
  }
  const real = listDir(".")
    .filter((e) => e.isDirectory() && !e.name.startsWith(".") && e.name !== "node_modules")
    .map((e) => e.name);
  for (const dir of real) {
    if (!listedDirs.has(dir)) findings.push(`directory \`${dir}/\` missing from the README tree`);
  }
  const listedFiles = new Set(entries.filter(([, , isDir]) => !isDir).map(([, name]) => name));
  const realFiles = listDir(".")
    .filter((e) => e.isFile() && !e.name.startsWith(".") && !e.name.endsWith("DS_Store"))
    .map((e) => e.name);
  for (const f of realFiles) {
    if (!listedFiles.has(f)) findings.push(`file \`${f}\` missing from the README tree`);
  }
  return findings;
});

rule("links-resolve", () => {
  const findings = [];
  for (const file of walkMarkdown()) {
    const lines = read(file).split("\n");
    let fence = false;
    for (const line of lines) {
      if (/^\s*(```|~~~)/.test(line)) {
        fence = !fence;
        continue;
      }
      if (fence) continue; // links inside code fences are examples, not references
      const candidates = [];
      for (const m of line.matchAll(/\]\(([^)\s]+?)(?:#[^)\s]*)?(?:\s+"[^"]*")?\)/g)) candidates.push(m[1]);
      const ref = line.match(/^\s*\[[^\]]+\]:\s*([^)\s]+)/); // reference-style definition
      if (ref) candidates.push(ref[1]);
      for (const raw of candidates) {
        const target = raw.replace(/^\.\//, "").replace(/^<|>$/g, "");
        if (/^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith("#")) continue;
        if (target.includes("{{")) continue;
        if (LINK_ALLOWLIST.has(target)) continue;
        if (existsSync(resolve(ROOT, dirname(file), target))) continue;
        findings.push(`${file}: broken link -> ${target}`);
      }
    }
  }
  return findings;
});

rule("frontmatter-valid", () => {
  const findings = [];
  const valueOf = (fm, key) => fm.match(new RegExp(`^[ \\t]*${key}:[ \\t]*(\\S.*)?$`, "m"))?.[1];
  for (const dir of skillDirs()) {
    const fm = frontmatter(read(join(dir, "SKILL.md")));
    if (!fm) {
      findings.push(`${dir}/SKILL.md: no YAML frontmatter`);
      continue;
    }
    const name = fm.match(/^name:[ \t]*(\S.*)$/m)?.[1]?.trim();
    if (name !== dir) findings.push(`${dir}/SKILL.md: name \`${name}\` != directory name`);
    const desc = fm.match(/^description:[ \t]*(.*)$/m)?.[1]?.trim();
    if (!desc) findings.push(`${dir}/SKILL.md: description missing or empty`);
    if (/^version:/m.test(fm) || /^last_updated:/m.test(fm)) {
      findings.push(`${dir}/SKILL.md: version/last_updated must live under metadata`);
    }
    const support = /^[ \t]+support:[ \t]*true\s*$/m.test(fm);
    if (support && dir !== SUPPORT_PACKAGE) {
      findings.push(`${dir}/SKILL.md: metadata.support is reserved for ${SUPPORT_PACKAGE}`);
    }
    if (!support) {
      for (const key of ["version", "last_updated", "author"]) {
        if (!valueOf(fm, key)) findings.push(`${dir}/SKILL.md: metadata.${key} missing or empty`);
      }
    }
    if (/^\t/m.test(fm)) findings.push(`${dir}/SKILL.md: frontmatter is tab-indented (invalid YAML)`);
    for (const line of fm.split("\n")) {
      const quoted = line.match(/^[A-Za-z_][\w-]*:\s*"(.*)$/);
      if (quoted && !quoted[1].endsWith('"')) {
        findings.push(`${dir}/SKILL.md: unterminated quote in \`${line.split(":")[0]}\``);
      }
    }
  }
  return findings;
});

rule("hint-present", () => {
  // Every skill is invocable, so every skill declares how: an empty hint is drift.
  // dev-shared is the support package and is never invoked directly.
  const findings = [];
  for (const dir of skillDirs()) {
    if (dir === SUPPORT_PACKAGE) continue;
    const fm = frontmatter(read(join(dir, "SKILL.md"))) ?? "";
    const hintLine = fm.match(/^argument-hint:[ \t]*(.*)$/m);
    const hintValue = (hintLine?.[1] ?? "").trim().replace(/^["']|["']$/g, "").trim();
    if (!hintValue) {
      findings.push(`${dir}/SKILL.md: argument-hint missing or empty`);
    }
  }
  return findings;
});

function commandsSection() {
  const text = read(README);
  if (!/^## Commands And Invocation$/m.test(text)) {
    return { error: "README has no `## Commands And Invocation` section" };
  }
  return { body: section(text, "## Commands And Invocation", /^## /) };
}

rule("flags-known", () => {
  const { body, error } = commandsSection();
  if (error) return [error];
  const rows = tableRows(body).filter((l) => /^\|\s*`[a-z0-9-]+`\s*\|/.test(l));
  if (!rows.length) return ["README Commands table has no skill rows"];
  const findings = [];
  for (const row of rows) {
    const skill = row.match(/^\|\s*`([a-z0-9-]+)`\s*\|/)[1];
    if (!existsSync(join(ROOT, skill))) {
      findings.push(`README Commands table names \`${skill}\`, which does not exist`);
      continue;
    }
    const flags = new Set([...row.matchAll(/--[a-z][a-z-]+/g)].map((m) => m[0]));
    if (!flags.size) continue;
    const corpus = [join(skill, "SKILL.md"), ...walkSkillFiles(skill)]
      .map((p) => join(ROOT, p))
      .filter((p) => existsSync(p) && statSync(p).isFile())
      .map((p) => readFileSync(p, "utf8"))
      .join("\n");
    for (const flag of flags) {
      if (!corpus.includes(flag)) findings.push(`README documents \`${flag}\` for \`${skill}\`, not found in the skill`);
    }
  }
  return findings;
});

rule("commands-coverage", () => {
  const { body, error } = commandsSection();
  if (error) return [error];
  const rows = new Set(
    tableRows(body)
      .map((row) => row.match(/^\|\s*`([a-z0-9-]+)`\s*\|/)?.[1])
      .filter(Boolean),
  );
  if (!rows.size) return ["README Commands table has no skill rows"];
  // A prose mention is not an invocation: every skill needs its own table row.
  return skillDirs()
    .filter((d) => d !== SUPPORT_PACKAGE && !rows.has(d))
    .map((d) => `\`${d}\` has no row in the README Commands table`);
});

function walkSkillFiles(dir, out = []) {
  for (const entry of listDir(dir)) {
    const rel = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "node_modules" || entry.name === "templates") continue;
      walkSkillFiles(rel, out);
    } else if (/\.(md|mjs|js|py|json)$/.test(entry.name)) {
      out.push(rel);
    }
  }
  return out;
}

rule("hardgate-parity", () => {
  const readmeRows = tableRows(section(read(README), "## HARD-GATEs", /^## /)).filter((l) => l.startsWith("| `"));
  const devkitRows = tableRows(section(read(DEVKIT), "## 5. HARD-GATEs", /^### |^---/)).filter((l) => l.startsWith("| `"));
  if (!readmeRows.length) return ["README HARD-GATEs table not found"];
  if (readmeRows.join("\n") !== devkitRows.join("\n")) {
    return ["HARD-GATE tables in README.md and devkit.md differ"];
  }
  return [];
});

rule("manifests-in-sync", () => {
  const source = read(AGENTS);
  const findings = [];
  for (const file of GENERATED) {
    if (!existsSync(join(ROOT, file))) {
      findings.push(`${file} is missing (run: node scripts/sync-manifests.mjs)`);
      continue;
    }
    if (read(file) !== renderManifest(file, source)) {
      findings.push(`${file} is out of sync with AGENTS.md (run: node scripts/sync-manifests.mjs)`);
    }
  }
  return findings;
});

rule("wiki-fresh", () => {
  const proc = spawnSync(process.execPath, [join(ROOT, "scripts", "gen-wiki-pages.mjs"), "--check"], {
    encoding: "utf8",
  });
  if (proc.error) return [`could not run the wiki generator: ${proc.error.message}`];
  return (proc.stdout ?? "")
    .split("\n")
    .filter((l) => l.trim().startsWith("stale"))
    .map((l) => `${l.trim()} (run: make wiki)`);
});

rule("wiki-coverage", () => {
  const findings = [];
  for (const dir of skillDirs()) {
    if (dir === SUPPORT_PACKAGE) continue;
    for (const lang of ["en", "vi"]) {
      const page = `wiki/${lang}/${dir}-skill.md`;
      if (!existsSync(join(ROOT, page))) {
        findings.push(`missing wiki page: ${page}`);
        continue;
      }
      const body = read(page);
      if (HAND_WRITTEN_WIKI.has(page)) {
        if (!body.includes(dir)) findings.push(`${page}: never mentions \`${dir}\``);
        continue;
      }
      if (!body.includes(`# ${dir}`)) findings.push(`${page}: does not start with the \`${dir}\` title`);
      if (!body.includes(`../../${dir}/SKILL.md`)) findings.push(`${page}: no source link back to ${dir}/SKILL.md`);
      if (!body.includes("generated by scripts/gen-wiki-pages.mjs")) {
        findings.push(`${page}: not generated by scripts/gen-wiki-pages.mjs`);
      }
    }
  }
  return findings;
});

function renderManifest(file, source) {
  const note = `Generated from AGENTS.md by scripts/sync-manifests.mjs — edit AGENTS.md, then run: node scripts/sync-manifests.mjs`;
  const header = file.endsWith(".md") ? `<!-- ${note} -->\n\n` : `# ${note}\n\n`;
  return header + source;
}

const results = rules.map(({ name, run }) => {
  let findings;
  try {
    findings = run();
  } catch (error) {
    findings = [`rule crashed: ${error.message}`];
  }
  return { name, ok: findings.length === 0, findings };
});

const failed = results.filter((r) => !r.ok);

if (JSON_OUT) {
  console.log(JSON.stringify({ root: relative(process.cwd(), ROOT) || ".", rules: results, ok: !failed.length }, null, 2));
} else {
  console.log(`dev-kit docs drift check — ${rules.length} rules\n`);
  for (const r of results) {
    console.log(`  [${r.ok ? " OK " : "FAIL"}] ${r.name}${r.ok ? "" : ` (${r.findings.length})`}`);
    for (const f of r.findings) console.log(`         - ${f}`);
  }
  console.log(`\n${failed.length ? `${failed.length} rule(s) failed` : "no drift detected"}`);
}

process.exit(failed.length ? 1 : 0);
