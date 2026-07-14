#!/usr/bin/env node
"use strict";

import {
  readFileSync,
  writeFileSync,
} from "node:fs";
import { basename } from "node:path";
import { parseArgs } from "node:util";

import {
  isFile,
  loadCatalog,
  resolveOutput,
  resolveProfile,
  validateArtifact,
  validateCatalog,
} from "./artifact-support.mjs";

function expectedArtifacts(catalog, manifest) {
  const profile = resolveProfile(catalog, manifest.profile);
  const expected = new Set(profile.required);
  for (const condition of manifest.conditions ?? []) {
    for (const artifactId of profile.conditional[condition] ?? []) {
      expected.add(artifactId);
    }
  }
  return expected;
}

function findItem(artifacts, artifactId, useCase = undefined) {
  return artifacts.find((item) => (
    item.id === artifactId
    && (useCase === undefined || item.use_case === useCase)
  ));
}

function main() {
  const { values, positionals } = parseArgs({
    options: {
      catalog: { type: "string" },
      update: { type: "boolean", default: false },
      json: { type: "boolean", default: false },
      summary: { type: "boolean", default: false },
      verbose: { type: "boolean", default: false },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
    strict: true,
  });
  if (values.help) {
    console.log("Usage: hi-reverse-validate-package <manifest> [--catalog <path>] [--update] [--json] [--summary] [--verbose]");
    return 0;
  }
  if (positionals.length !== 1) {
    console.error("Usage: hi-reverse-validate-package <manifest> [--catalog <path>] [--update] [--json] [--summary] [--verbose]");
    return 2;
  }

  const manifestPath = positionals[0];
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  const { catalog, catalogPath } = loadCatalog(values.catalog ?? manifest.catalog);
  const failures = validateCatalog(catalog, catalogPath);

  if (manifest.gates?.artifact_plan !== "PASS") {
    failures.push("ARTIFACT_PLAN_GATE is not PASS.");
  }

  const expectedIds = expectedArtifacts(catalog, manifest);
  const artifacts = manifest.artifacts ?? [];
  const manifestConditions = new Set(manifest.conditions ?? []);
  const knownConditions = new Set(Object.keys(catalog.conditions ?? {}));
  for (const condition of [...manifestConditions].filter((item) => !knownConditions.has(item)).sort()) {
    failures.push(`Manifest contains unknown condition: ${condition}`);
  }

  const presentIds = new Set(
    artifacts.filter((item) => item.required).map((item) => item.id),
  );
  for (const artifactId of [...expectedIds].filter((item) => !presentIds.has(item)).sort()) {
    failures.push(`Manifest missing required artifact: ${artifactId}`);
  }

  const useCases = manifest.use_cases ?? [];
  for (const artifactId of expectedIds) {
    const spec = catalog.artifacts[artifactId];
    if (spec.scope !== "usecase") {
      continue;
    }
    if (useCases.length === 0) {
      failures.push(`No use-case instances declared for required artifact ${artifactId}.`);
      continue;
    }
    const covered = new Set(
      artifacts
        .filter((item) => item.required && item.id === artifactId)
        .map((item) => item.use_case),
    );
    for (const useCase of useCases) {
      if (!covered.has(useCase)) {
        failures.push(`${artifactId} missing use-case instance ${useCase}.`);
      }
    }
  }

  const results = [];
  for (const item of artifacts) {
    if (!item.required) {
      continue;
    }
    let result;
    if ((item.output ?? "").includes("__USE_CASE__")) {
      result = {
        artifact_id: item.id,
        path: item.output,
        passed: false,
        checks: [],
        errors: ["Use-case discovery placeholder is unresolved."],
      };
    } else {
      result = validateArtifact(
        catalog,
        item.id,
        resolveOutput(manifestPath, item.output ?? ""),
      );
    }
    results.push(result);
    item.status = result.passed ? "validated" : "failed";
    item.validation = result;
  }

  for (const result of results) {
    if (!result.passed) {
      failures.push(...result.errors.map((error) => `${result.artifact_id}: ${error}`));
    }
  }

  const discoveryItem = findItem(artifacts, "discovery-manifest");
  if (discoveryItem) {
    const discoveryPath = resolveOutput(manifestPath, discoveryItem.output ?? "");
    if (isFile(discoveryPath)) {
      let discovery = {};
      try {
        discovery = JSON.parse(readFileSync(discoveryPath, "utf8"));
      } catch {
        discovery = {};
      }
      const artifactConditions = discovery.artifact_conditions ?? {};
      for (const condition of Object.keys(catalog.conditions ?? {})) {
        if (!(condition in artifactConditions)) {
          failures.push(`Discovery manifest does not classify condition: ${condition}`);
        }
      }
      const activeConditions = Object.entries(artifactConditions)
        .filter(([, detail]) => detail && typeof detail === "object" && detail.active === true)
        .map(([condition]) => condition);
      for (const condition of activeConditions.filter((item) => !manifestConditions.has(item)).sort()) {
        failures.push(`Discovery activates condition absent from manifest: ${condition}`);
      }
    }
  }

  for (const useCase of useCases) {
    const useCaseItem = findItem(artifacts, "usecase-document", useCase);
    const sequenceItem = findItem(artifacts, "sequence-diagram", useCase);
    const classItem = findItem(artifacts, "class-diagram", useCase);
    if (!useCaseItem || !sequenceItem || !classItem) {
      continue;
    }

    const useCasePath = resolveOutput(manifestPath, useCaseItem.output ?? "");
    if (!isFile(useCasePath)) {
      continue;
    }
    const useCaseText = readFileSync(useCasePath, "utf8");
    const sequenceName = basename(sequenceItem.output ?? "");
    const className = basename(classItem.output ?? "");
    if (!useCaseText.includes(sequenceName)) {
      failures.push(`Use case ${useCase} does not link sequence artifact ${sequenceName}.`);
    }
    if (!useCaseText.includes(className)) {
      failures.push(`Use case ${useCase} does not link class artifact ${className}.`);
    }
  }

  const gate = failures.length === 0 ? "PASS" : "FAIL";
  manifest.gates ??= {};
  manifest.gates.reverse_package = gate;
  manifest.package_validation = {
    passed: failures.length === 0,
    failures,
    artifact_results: results,
  };

  if (values.update) {
    writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  }

  if (values.json) {
    console.log(JSON.stringify(manifest.package_validation, null, 2));
  } else {
    const showVerbose = values.verbose && !values.summary;
    if (showVerbose) {
      for (const result of results) {
        console.log(`${result.passed ? "PASS" : "FAIL"}: ${result.artifact_id} -> ${result.path}`);
      }
    }
    const passed = results.filter((result) => result.passed).length;
    const failedArtifacts = results
      .filter((result) => !result.passed)
      .map((result) => result.artifact_id);
    console.log(`REVERSE_PACKAGE_GATE: ${gate}`);
    console.log(`validated=${passed}/${results.length}`);
    if (failedArtifacts.length > 0) {
      console.log(`failures=${failedArtifacts.join(",")}`);
    }
    if (showVerbose || failedArtifacts.length > 0) {
      for (const failure of failures) {
        console.log(`FAIL: ${failure}`);
      }
    }
  }

  return failures.length === 0 ? 0 : 1;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 2;
}
