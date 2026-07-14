#!/usr/bin/env node
"use strict";

import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs } from "node:util";

import {
  SKILL_DIR,
  loadCatalog,
  renderOutputPattern,
  resolveProfile,
  unique,
  validateCatalog,
} from "./artifact-support.mjs";

function parseCliArgs() {
  const { values } = parseArgs({
    options: {
      catalog: { type: "string" },
      profile: { type: "string" },
      module: { type: "string" },
      "use-case": { type: "string", multiple: true, default: [] },
      condition: { type: "string", multiple: true, default: [] },
      "output-root": { type: "string" },
      output: { type: "string" },
      date: { type: "string" },
      scaffold: { type: "boolean", default: false },
      "list-capabilities": { type: "boolean", default: false },
      "check-catalog": { type: "boolean", default: false },
      next: { type: "string" },
      summary: { type: "boolean", default: false },
      help: { type: "boolean", short: "h", default: false },
    },
    strict: true,
  });
  return values;
}

function printUsage() {
  console.log("Usage: hi-reverse-plan [--check-catalog | --list-capabilities]");
  console.log("       hi-reverse-plan --profile <name> --module <name> [options]");
  console.log("       hi-reverse-plan --next <manifest-path>");
  console.log("Options: --use-case <slug> --condition <name> --output-root <dir> --output <file> --date <YYYYMMDD> --scaffold --summary");
}

const PENDING_STATUSES = new Set([
  "planned",
  "awaiting-use-case-discovery",
  "failed",
  "existing",
  "scaffolded",
]);

function printNextArtifact(catalog, manifest) {
  const artifacts = manifest.artifacts ?? [];
  const pending = artifacts.find(
    (item) =>
      item.required
      && PENDING_STATUSES.has(item.status)
      && !(item.output ?? "").includes("__USE_CASE__"),
  );
  if (!pending) {
    const validated = artifacts.filter(
      (item) => item.required && item.status === "validated",
    ).length;
    console.log(
      `NO_PENDING_ARTIFACT (validated=${validated}/${artifacts.filter((item) => item.required).length})`,
    );
    return 1;
  }

  const spec = catalog.artifacts?.[pending.id] ?? {};
  let evidenceGaps;
  if (pending.use_case === null && spec.scope === "usecase") {
    evidenceGaps = "awaiting-use-case-discovery";
  } else {
    evidenceGaps = (spec.evidence ?? []).join(",") || "none";
  }

  console.log(`ARTIFACT_ID=${pending.id}`);
  console.log(`TECHNIQUE=${spec.technique ?? "none"}`);
  console.log(`OUTPUT=${pending.output ?? "none"}`);
  console.log(`EVIDENCE_GAPS=${evidenceGaps}`);
  if (pending.use_case) {
    console.log(`USE_CASE=${pending.use_case}`);
  }
  return 0;
}

function printCapabilities(catalog) {
  console.log("ARTIFACT_ID\tSTATUS\tSCOPE\tOUTPUT\tTECHNIQUE");
  for (const [artifactId, spec] of Object.entries(catalog.artifacts)) {
    console.log(`${artifactId}\t${spec.status}\t${spec.scope}\t${spec.output_pattern}\t${spec.technique ?? ""}`);
  }
}

function utcDate() {
  return new Date().toISOString().slice(0, 10).replaceAll("-", "");
}

function utcTimestamp() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00");
}

function main() {
  const args = parseCliArgs();
  if (args.help) {
    printUsage();
    return 0;
  }

  if (args.next) {
    const { catalog } = loadCatalog(args.catalog);
    const manifest = JSON.parse(readFileSync(args.next, "utf8"));
    return printNextArtifact(catalog, manifest);
  }

  const { catalog, catalogPath } = loadCatalog(args.catalog);
  const catalogErrors = validateCatalog(catalog, catalogPath);

  if (args["check-catalog"]) {
    if (catalogErrors.length > 0) {
      for (const error of catalogErrors) {
        console.log(`FAIL: ${error}`);
      }
      console.log("CATALOG_GATE: FAIL");
      return 1;
    }
    console.log(
      `CATALOG_GATE: PASS (${Object.keys(catalog.artifacts).length} artifacts, `
      + `${Object.keys(catalog.profiles).length} profiles)`,
    );
    return 0;
  }

  if (args["list-capabilities"]) {
    printCapabilities(catalog);
    return 0;
  }

  if (catalogErrors.length > 0) {
    for (const error of catalogErrors) {
      console.log(`FAIL: ${error}`);
    }
    console.log("ARTIFACT_PLAN_GATE: BLOCKED");
    return 1;
  }

  if (!args.profile || !args.module) {
    console.error("--profile and --module are required for plan generation.");
    return 2;
  }

  const profile = resolveProfile(catalog, args.profile);
  const knownConditions = new Set(Object.keys(catalog.conditions ?? {}));
  const selectedConditions = new Set(args.condition);
  const unknownConditions = [...selectedConditions]
    .filter((condition) => !knownConditions.has(condition))
    .sort();
  if (unknownConditions.length > 0) {
    console.error(`Unknown conditions: ${unknownConditions.join(", ")}`);
    return 2;
  }

  const date = args.date ?? utcDate();
  const outputRoot = args["output-root"] ?? `usecase/${args.module}`;
  const useCases = unique(args["use-case"]);
  let selectedIds = [...profile.required];
  const selectedByCondition = {};
  const availableConditionals = {};

  for (const [condition, artifactIds] of Object.entries(profile.conditional)) {
    if (selectedConditions.has(condition)) {
      selectedByCondition[condition] = artifactIds;
      selectedIds.push(...artifactIds);
    } else {
      availableConditionals[condition] = artifactIds;
    }
  }

  selectedIds = unique(selectedIds);
  const artifacts = [];
  const blocked = [];

  for (const artifactId of selectedIds) {
    const spec = catalog.artifacts[artifactId];
    if (spec.status !== "supported") {
      blocked.push(`${artifactId}:${spec.status}`);
    }

    const condition = Object.entries(selectedByCondition)
      .find(([, artifactIds]) => artifactIds.includes(artifactId))?.[0] ?? null;
    let instances = spec.scope === "usecase" ? useCases : [null];
    if (spec.scope === "usecase" && instances.length === 0) {
      instances = [null];
    }

    for (const useCase of instances) {
      const filename = renderOutputPattern(
        spec.output_pattern,
        args.module,
        useCase,
        date,
      );
      const outputPath = join(outputRoot, filename);
      const item = {
        id: artifactId,
        scope: spec.scope,
        use_case: useCase,
        condition,
        required: true,
        support_status: spec.status,
        technique: spec.technique,
        template: spec.template,
        output: outputPath,
        status: useCase || spec.scope === "module"
          ? "planned"
          : "awaiting-use-case-discovery",
        validation: null,
      };

      if (args.scaffold && !outputPath.includes("__USE_CASE__")) {
        const source = join(SKILL_DIR, spec.template);
        mkdirSync(dirname(outputPath), { recursive: true });
        if (existsSync(outputPath)) {
          item.status = "existing";
        } else {
          copyFileSync(source, outputPath);
          item.status = "scaffolded";
        }
      }

      artifacts.push(item);
    }
  }

  const gate = blocked.length > 0 ? "BLOCKED" : "PASS";
  const manifest = {
    schema_version: 1,
    catalog: catalogPath,
    module: args.module,
    profile: args.profile,
    generated_at: utcTimestamp(),
    conditions: [...selectedConditions].sort(),
    use_cases: useCases,
    output_root: outputRoot,
    artifacts,
    available_conditionals: availableConditionals,
    gates: {
      artifact_plan: gate,
      reverse_package: "PENDING",
    },
    blocked_capabilities: blocked,
  };

  const rendered = `${JSON.stringify(manifest, null, 2)}\n`;
  if (args.output) {
    mkdirSync(dirname(args.output), { recursive: true });
    writeFileSync(args.output, rendered, "utf8");
    console.log(`Manifest: ${args.output}`);
  } else if (!args.summary) {
    process.stdout.write(rendered);
  }

  const pending = artifacts.filter(
    (item) => item.status === "awaiting-use-case-discovery",
  ).length;
  console.log(
    `ARTIFACT_PLAN_GATE: ${gate} (${artifacts.length} instances, `
    + `${pending} awaiting use-case discovery)`,
  );
  return blocked.length > 0 ? 1 : 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 2;
}
