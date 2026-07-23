#!/usr/bin/env node
/**
 * git-normalize.js — Strip noise from raw git output before it enters context.
 *
 * Reads git output from stdin, removes commit metadata, ANSI codes, and blank
 * runs, optionally keeps changed lines only, and caps the line count. Used to
 * reduce tokens fed to the agent when investigating git history.
 *
 * Cross-platform: runs on Node.js (macOS, Windows, Linux). No shell or
 * grep/awk/sed dependency.
 *
 * Usage:
 *   git show <commit> | node git-normalize.js                  # default cleanup
 *   git show <commit> | node git-normalize.js --changed        # diff body only (+/-)
 *   git log -p         | node git-normalize.js --changed --max-lines 400
 *   git show <commit> | node git-normalize.js --help
 *
 * Exit code: 0 on success, 2 on usage error. Empty stdin produces no output.
 */

'use strict';

// --- Config ---
let maxLines = 200;
let changedOnly = false;

function usage() {
  process.stdout.write(
`git-normalize.js — normalize raw git output for agent context.

Usage: <git command> | node git-normalize.js [options]

Options:
  -c, --changed        Keep changed lines only (additions/deletions + file
                       headers). Drops unchanged context. Use for large diffs.
      --max-lines N    Cap output to N lines (default: 200). 0 = no cap.
  -h, --help           Show this help and exit.

Default cleanup (no flags):
  - strips ANSI color codes
  - strips commit metadata (tree/parent/author/committer/gpgsig/object/type/
    tag/encoding/Date/index)
  - collapses runs of blank lines
  - caps to --max-lines

Example:
  git show abc1234 | node git-normalize.js --changed
`);
}

// --- Parse args ---
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '-c' || a === '--changed') {
    changedOnly = true;
  } else if (a === '--max-lines') {
    const v = args[++i];
    if (!/^\d+$/.test(v || '')) {
      process.stderr.write('git-normalize: --max-lines must be a non-negative integer\n');
      process.exit(2);
    }
    maxLines = parseInt(v, 10);
  } else if (a.startsWith('--max-lines=')) {
    const v = a.slice('--max-lines='.length);
    if (!/^\d+$/.test(v)) {
      process.stderr.write('git-normalize: --max-lines must be a non-negative integer\n');
      process.exit(2);
    }
    maxLines = parseInt(v, 10);
  } else if (a === '-h' || a === '--help') {
    usage();
    process.exit(0);
  } else {
    process.stderr.write(`git-normalize: unknown option '${a}' (try --help)\n`);
    process.exit(2);
  }
}

// --- Filters ---

// ANSI escape sequences: SGR (m), cursor movement (G/K/H), erase.
// Single global regex, reused per line.
const ANSI_RE = /\x1b\[[0-9;]*[mGKH]/g;

// Commit metadata prefixes git prepends to show/log raw output.
// "Date:" matched separately because it has a trailing colon in the line.
const META_KEYS = ['tree', 'parent', 'object', 'type', 'tag', 'gpgsig', 'encoding', 'author', 'committer', 'index'];
// Precompute a regex that matches "<key> " or "<key>\t" at line start.
const META_RE = new RegExp('^(?:' + META_KEYS.join('|') + ')[ \\t]');

function stripAnsi(line) {
  return line.replace(ANSI_RE, '');
}

function isMetadata(line) {
  return META_RE.test(line) || line.startsWith('Date:');
}

// For --changed: keep file headers, hunk markers, and +/- diff lines.
function isChanged(line) {
  if (line.startsWith('diff --git')) return true;
  if (line.startsWith('+++ ')) return true;
  if (line.startsWith('--- ')) return true;
  if (line.startsWith('@@ ')) return true;
  if (line.startsWith('+') || line.startsWith('-')) return true;
  return false;
}

function isBlank(line) {
  return line.length === 0 || /^[ \t]*$/.test(line);
}

// --- Process stdin line-by-line, stream output ---
let out = 0;
let prevBlank = false;
let truncated = false;

const rl = require('readline').createInterface({
  input: process.stdin,
  crlfDelay: Infinity, // handle \r\n and \r correctly across platforms
});

rl.on('line', (raw) => {
  if (truncated) return;

  let line = stripAnsi(raw);

  if (isMetadata(line)) return;

  if (changedOnly && !isChanged(line)) return;

  // Collapse runs of blank lines (2+ -> 1).
  if (isBlank(line)) {
    if (prevBlank) return;
    prevBlank = true;
    line = '';
  } else {
    prevBlank = false;
  }

  // Cap output lines. If at limit, emit truncation marker and stop accepting.
  if (maxLines > 0 && out >= maxLines) {
    process.stdout.write(`...[truncated at ${maxLines} lines]\n`);
    truncated = true;
    rl.close();
    return;
  }

  process.stdout.write(line + '\n');
  out++;
});

rl.on('close', () => {
  process.exit(0);
});
