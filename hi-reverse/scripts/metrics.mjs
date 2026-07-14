#!/usr/bin/env node
"use strict";

import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync,
} from "node:fs";
import {
  basename,
  dirname,
  join,
} from "node:path";
import { parseArgs } from "node:util";

function isDirectory(path) {
  try {
    return statSync(path).isDirectory();
  } catch {
    return false;
  }
}

function walkFiles(root) {
  if (!isDirectory(root)) {
    return [];
  }

  const files = [];
  const pending = [root];
  while (pending.length > 0) {
    const current = pending.pop();
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const path = join(current, entry.name);
      if (entry.isDirectory()) {
        pending.push(path);
      } else if (entry.isFile()) {
        files.push(path);
      }
    }
  }
  return files;
}

function percentage(numerator, denominator) {
  return denominator > 0 ? Math.floor((100 * numerator) / denominator) : 0;
}

function localDate() {
  const now = new Date();
  const year = String(now.getFullYear()).padStart(4, "0");
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function useCaseFromPath(path) {
  const stem = basename(path, ".md");
  const separator = stem.indexOf("_");
  return separator >= 0 ? stem.slice(separator + 1) : stem;
}

function main() {
  const { values, positionals } = parseArgs({
    options: {
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
    strict: true,
  });
  if (values.help) {
    console.log("Usage: hi-reverse-metrics [usecase-dir] [metrics-file] [package-manifest]");
    return 0;
  }
  if (positionals.length > 3) {
    console.error("Usage: hi-reverse-metrics [usecase-dir] [metrics-file] [package-manifest]");
    return 2;
  }

  const base = positionals[0] ?? "usecase";
  const metricsPath = positionals[1] ?? join(base, "trace_metrics.md");
  const manifestPath = positionals[2] ?? null;
  const files = walkFiles(base);
  const useCaseFiles = files.filter((path) => {
    const name = basename(path);
    return name.startsWith("uc") && name.endsWith(".md");
  });
  const sequenceFiles = files.filter((path) => {
    const name = basename(path);
    return name.startsWith("seq_") && name.endsWith(".mmd");
  });
  const classFiles = files.filter((path) => {
    const name = basename(path);
    return name.startsWith("class_") && name.endsWith(".mmd");
  });

  let sequenceCovered = 0;
  let classCovered = 0;
  let artifactGateCovered = 0;
  const useCases = useCaseFiles.map((path) => ({
    path,
    name: useCaseFromPath(path),
  }));

  for (const useCase of useCases) {
    if (sequenceFiles.some((path) => (
      dirname(path) === dirname(useCase.path)
      && basename(path).startsWith(`seq_${useCase.name}_`)
    ))) {
      sequenceCovered += 1;
    }
    if (classFiles.some((path) => (
      dirname(path) === dirname(useCase.path)
      && basename(path).startsWith(`class_${useCase.name}_`)
    ))) {
      classCovered += 1;
    }
  }

  let profile = "not-provided";
  let packageValidated = 0;
  let packageRequired = 0;
  let packageGate = "NOT_RUN";
  if (manifestPath) {
    if (!existsSync(manifestPath)) {
      console.error(`Package manifest is missing: ${manifestPath}`);
      return 2;
    }
    const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
    const required = (manifest.artifacts ?? []).filter((item) => item.required);
    const validatedUseCases = new Set(
      required
        .filter((item) => item.id === "usecase-document" && item.status === "validated")
        .map((item) => item.use_case),
    );
    artifactGateCovered = useCases.filter((useCase) => (
      validatedUseCases.has(useCase.name)
    )).length;
    profile = manifest.profile ?? "unknown";
    packageValidated = required.filter((item) => item.status === "validated").length;
    packageRequired = required.length;
    packageGate = manifest.gates?.reverse_package ?? "NOT_RUN";
  } else {
    artifactGateCovered = useCases.filter((useCase) => (
      readFileSync(useCase.path, "utf8").includes("ARTIFACT_GATE: PASS")
    )).length;
  }

  const useCaseCount = useCases.length;
  const sequenceCoverage = percentage(sequenceCovered, useCaseCount);
  const classCoverage = percentage(classCovered, useCaseCount);
  const artifactGateCoverage = percentage(artifactGateCovered, useCaseCount);
  const packageCoverage = percentage(packageValidated, packageRequired);

  mkdirSync(dirname(metricsPath), { recursive: true });
  let metrics = existsSync(metricsPath) ? readFileSync(metricsPath, "utf8") : "";
  if (!metrics || /\{\{[^}]+\}\}/.test(metrics)) {
    metrics = `# Trace Metrics

## Definitions

| Metric | Target |
|---|---|
| SEQUENCE_UC_COVERAGE | 100% documented use cases |
| CLASS_UC_COVERAGE | 100% documented use cases |
| ARTIFACT_GATE_COVERAGE | 100% documented use cases |
| PROFILE_ARTIFACT_COVERAGE | 100% required profile artifacts |
| REVERSE_PACKAGE_STATUS | PASS |

## Snapshots
`;
  }

  metrics += `
### Snapshot ${localDate()}
- PROFILE: ${profile}
- UC_COUNT: ${useCaseCount}
- SEQUENCE_ARTIFACTS: ${sequenceFiles.length}
- CLASS_ARTIFACTS: ${classFiles.length}
- SEQUENCE_UC_COVERAGE: ${sequenceCovered} / ${useCaseCount} = ${sequenceCoverage}%
- CLASS_UC_COVERAGE: ${classCovered} / ${useCaseCount} = ${classCoverage}%
- ARTIFACT_GATE_COVERAGE: ${artifactGateCovered} / ${useCaseCount} = ${artifactGateCoverage}%
- PROFILE_ARTIFACT_COVERAGE: ${packageValidated} / ${packageRequired} = ${packageCoverage}%
- REVERSE_PACKAGE_STATUS: ${packageGate}
`;
  writeFileSync(metricsPath, metrics, "utf8");
  console.log(`Appended artifact metrics to ${metricsPath}`);
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 2;
}
