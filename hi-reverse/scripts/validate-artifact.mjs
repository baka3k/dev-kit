#!/usr/bin/env node
"use strict";

import { parseArgs } from "node:util";

import {
  loadCatalog,
  validateArtifact,
} from "./artifact-support.mjs";

function main() {
  const { values, positionals } = parseArgs({
    options: {
      catalog: { type: "string" },
      "allow-placeholders": { type: "boolean", default: false },
      json: { type: "boolean", default: false },
      summary: { type: "boolean", default: false },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
    strict: true,
  });
  if (values.help) {
    console.log("Usage: hi-reverse-validate-artifact <artifact-id> <path> [--catalog <path>] [--allow-placeholders] [--json] [--summary]");
    return 0;
  }
  if (positionals.length !== 2) {
    console.error("Usage: hi-reverse-validate-artifact <artifact-id> <path> [--catalog <path>] [--allow-placeholders] [--json] [--summary]");
    return 2;
  }

  const [artifactId, path] = positionals;
  const { catalog } = loadCatalog(values.catalog);
  const result = validateArtifact(catalog, artifactId, path, {
    allowPlaceholders: values["allow-placeholders"],
  });

  if (values.json) {
    console.log(JSON.stringify(result, null, 2));
  } else if (values.summary) {
    console.log(`ARTIFACT_GATE: ${result.passed ? "PASS" : "FAIL"} (${artifactId})`);
    if (!result.passed) {
      for (const error of result.errors.slice(0, 3)) {
        console.log(`FAIL: ${error}`);
      }
    }
  } else {
    for (const check of result.checks) {
      console.log(`PASS: ${check}`);
    }
    for (const error of result.errors) {
      console.log(`FAIL: ${error}`);
    }
    console.log(`ARTIFACT_GATE: ${result.passed ? "PASS" : "FAIL"} (${artifactId})`);
  }
  return result.passed ? 0 : 1;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 2;
}
