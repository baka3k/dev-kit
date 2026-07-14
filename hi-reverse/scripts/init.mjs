#!/usr/bin/env node
"use strict";

import {
  cpSync,
  mkdirSync,
  readdirSync,
} from "node:fs";
import {
  basename,
  join,
} from "node:path";
import { parseArgs } from "node:util";

import { SKILL_DIR } from "./artifact-support.mjs";

function main() {
  const { values, positionals } = parseArgs({
    options: {
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
    strict: true,
  });
  if (values.help) {
    console.log("Usage: hi-reverse-init <output-dir>");
    return 0;
  }
  if (positionals.length !== 1) {
    console.error("Usage: hi-reverse-init <output-dir>");
    return 2;
  }

  const output = positionals[0];
  const sourceTemplates = join(SKILL_DIR, "templates");
  const outputTemplates = join(output, "templates");
  mkdirSync(join(output, "usecase"), { recursive: true });
  mkdirSync(outputTemplates, { recursive: true });

  for (const entry of readdirSync(sourceTemplates, { withFileTypes: true })) {
    cpSync(
      join(sourceTemplates, entry.name),
      join(outputTemplates, basename(entry.name)),
      { force: true, recursive: entry.isDirectory() },
    );
  }

  console.log(`Initialized: ${output}`);
  console.log(`Templates: ${outputTemplates}`);
  console.log("Evidence retrieval is not performed by this command.");
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 2;
}
