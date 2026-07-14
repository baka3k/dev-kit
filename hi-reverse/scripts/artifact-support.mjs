#!/usr/bin/env node
"use strict";

import {
  existsSync,
  readFileSync,
  statSync,
} from "node:fs";
import { homedir } from "node:os";
import {
  dirname,
  isAbsolute,
  join,
  resolve,
} from "node:path";
import { fileURLToPath } from "node:url";

export const SKILL_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
export const DEFAULT_CATALOG = join(
  SKILL_DIR,
  "references",
  "ARTIFACT-CATALOG.yaml",
);

const SUPPORT_STATUSES = new Set([
  "supported",
  "partial",
  "planned",
  "unsupported",
]);
const PLACEHOLDER_RE = /\{\{[^{}]+\}\}/g;

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export function isFile(path) {
  try {
    return statSync(path).isFile();
  } catch {
    return false;
  }
}

function expandUser(path) {
  if (path === "~") {
    return homedir();
  }
  if (path.startsWith("~/")) {
    return join(homedir(), path.slice(2));
  }
  return path;
}

export function loadCatalog(path = null) {
  const catalogPath = path
    ? resolve(expandUser(path))
    : DEFAULT_CATALOG;
  const catalog = JSON.parse(readFileSync(catalogPath, "utf8"));
  if (!isObject(catalog)) {
    throw new Error(`Catalog must be a mapping: ${catalogPath}`);
  }
  return { catalog, catalogPath };
}

export function unique(items) {
  return [...new Set(items)];
}

export function resolveProfile(catalog, profileName, stack = []) {
  const profiles = catalog.profiles ?? {};
  if (!(profileName in profiles)) {
    throw new Error(`Unknown profile: ${profileName}`);
  }
  if (stack.includes(profileName)) {
    throw new Error(`Profile inheritance cycle: ${[...stack, profileName].join(" -> ")}`);
  }

  const profile = profiles[profileName];
  const required = [];
  const conditional = {};

  for (const parent of profile.extends ?? []) {
    const inherited = resolveProfile(catalog, parent, [...stack, profileName]);
    required.push(...inherited.required);
    for (const [condition, artifactIds] of Object.entries(inherited.conditional)) {
      conditional[condition] ??= [];
      conditional[condition].push(...artifactIds);
    }
  }

  required.push(...(profile.required ?? []));
  for (const [condition, artifactIds] of Object.entries(profile.conditional ?? {})) {
    conditional[condition] ??= [];
    conditional[condition].push(...artifactIds);
  }

  return {
    name: profileName,
    description: profile.description ?? "",
    required: unique(required),
    conditional: Object.fromEntries(
      Object.entries(conditional).map(([condition, artifactIds]) => [
        condition,
        unique(artifactIds),
      ]),
    ),
  };
}

export function validateCatalog(catalog, catalogPath) {
  const errors = [];
  const artifacts = catalog.artifacts;
  const profiles = catalog.profiles;

  if (!isObject(artifacts) || Object.keys(artifacts).length === 0) {
    return ["Catalog artifacts must be a non-empty mapping."];
  }
  if (!isObject(profiles) || Object.keys(profiles).length === 0) {
    return ["Catalog profiles must be a non-empty mapping."];
  }

  for (const [artifactId, spec] of Object.entries(artifacts)) {
    if (!isObject(spec)) {
      errors.push(`${artifactId}: specification must be a mapping.`);
      continue;
    }

    if (!SUPPORT_STATUSES.has(spec.status)) {
      errors.push(`${artifactId}: invalid support status ${JSON.stringify(spec.status)}.`);
    }

    if (spec.status === "supported") {
      for (const field of [
        "scope",
        "output_pattern",
        "technique",
        "template",
        "validator",
      ]) {
        if (!spec[field]) {
          errors.push(`${artifactId}: supported artifact missing ${field}.`);
        }
      }

      for (const field of ["technique", "template"]) {
        const relative = spec[field];
        if (relative && !isFile(join(SKILL_DIR, relative))) {
          errors.push(`${artifactId}: missing ${field} file ${relative}.`);
        }
      }

      const validator = isObject(spec.validator) ? spec.validator : {};
      if (!new Set(["markdown", "json", "mermaid"]).has(validator.type)) {
        errors.push(`${artifactId}: unsupported validator type.`);
      }

      const template = spec.template;
      if (template && isFile(join(SKILL_DIR, template))) {
        const result = validateArtifact(
          catalog,
          artifactId,
          join(SKILL_DIR, template),
          { allowPlaceholders: true },
        );
        for (const error of result.errors) {
          errors.push(`${artifactId}: template fixture: ${error}`);
        }
      }
    }
  }

  const knownIds = new Set(Object.keys(artifacts));
  for (const profileName of Object.keys(profiles)) {
    let resolvedProfile;
    try {
      resolvedProfile = resolveProfile(catalog, profileName);
    } catch (error) {
      errors.push(error.message);
      continue;
    }

    const referenced = [...resolvedProfile.required];
    for (const artifactIds of Object.values(resolvedProfile.conditional)) {
      referenced.push(...artifactIds);
    }
    for (const artifactId of referenced) {
      if (!knownIds.has(artifactId)) {
        errors.push(`${profileName}: references unknown artifact ${artifactId}.`);
      }
    }
  }

  void catalogPath;
  return errors;
}

function firstContentLine(text) {
  for (const line of text.split(/\r?\n/)) {
    const stripped = line.trim();
    if (stripped && !stripped.startsWith("%%")) {
      return stripped;
    }
  }
  return "";
}

function fullMatch(pattern, value) {
  return new RegExp(`^(?:${pattern})$`).test(value);
}

export function validateArtifact(
  catalog,
  artifactId,
  path,
  { allowPlaceholders = false } = {},
) {
  const checks = [];
  const errors = [];
  const artifactPath = String(path);
  const spec = catalog.artifacts?.[artifactId];

  if (!isObject(spec)) {
    return {
      artifact_id: artifactId,
      path: artifactPath,
      passed: false,
      checks,
      errors: [`Unknown artifact id: ${artifactId}`],
    };
  }

  if (spec.status !== "supported") {
    errors.push(
      `Artifact status is ${spec.status}; only supported artifacts can pass.`,
    );
  }

  if (!isFile(artifactPath)) {
    errors.push(`Artifact file is missing: ${artifactPath}`);
    return {
      artifact_id: artifactId,
      path: artifactPath,
      passed: false,
      checks,
      errors,
    };
  }

  const text = readFileSync(artifactPath, "utf8");
  if (!text.trim()) {
    errors.push("Artifact file is empty.");
  } else {
    checks.push("file exists and is non-empty");
  }

  if (!allowPlaceholders) {
    const placeholders = unique(text.match(PLACEHOLDER_RE) ?? []).sort();
    if (placeholders.length > 0) {
      errors.push(`Unresolved template placeholders: ${placeholders.slice(0, 5).join(", ")}`);
    } else {
      checks.push("no unresolved template placeholders");
    }
  }

  const validator = isObject(spec.validator) ? spec.validator : {};
  if (validator.type === "markdown") {
    const lines = new Set(text.split(/\r?\n/).map((line) => line.trim()));
    for (const heading of validator.required_headings ?? []) {
      if (lines.has(heading)) {
        checks.push(`heading ${heading}`);
      } else {
        errors.push(`Missing required heading: ${heading}`);
      }
    }
  } else if (validator.type === "json") {
    try {
      const value = JSON.parse(text);
      if (!isObject(value)) {
        errors.push("JSON artifact must contain a top-level object.");
      } else {
        checks.push("valid JSON object");
        for (const key of validator.required_keys ?? []) {
          if (Object.hasOwn(value, key)) {
            checks.push(`JSON key ${key}`);
          } else {
            errors.push(`Missing required JSON key: ${key}`);
          }
        }
      }
    } catch (error) {
      errors.push(`Invalid JSON: ${error.message}`);
    }
  } else if (validator.type === "mermaid") {
    const root = firstContentLine(text);
    const pattern = validator.root_pattern ?? "";
    if (pattern && fullMatch(pattern, root)) {
      checks.push(`Mermaid root ${root}`);
    } else {
      errors.push(`Mermaid root ${JSON.stringify(root)} does not match ${JSON.stringify(pattern)}.`);
    }
  } else {
    errors.push(`Unsupported validator type: ${JSON.stringify(validator.type)}`);
  }

  for (const pattern of validator.required_patterns ?? []) {
    if (new RegExp(pattern, "m").test(text)) {
      checks.push(`pattern ${pattern}`);
    } else {
      errors.push(`Missing required pattern: ${pattern}`);
    }
  }

  return {
    artifact_id: artifactId,
    path: artifactPath,
    passed: errors.length === 0,
    checks,
    errors,
  };
}

export function slug(value) {
  const normalized = value.trim().replace(/[^A-Za-z0-9._-]+/g, "-").replace(/^-+|-+$/g, "");
  return normalized || "unnamed";
}

export function renderOutputPattern(pattern, moduleName, useCase, date) {
  return pattern
    .replaceAll("{module}", slug(moduleName))
    .replaceAll("{use_case}", useCase ? slug(useCase) : "__USE_CASE__")
    .replaceAll("{date}", date);
}

export function resolveOutput(manifestPath, output) {
  if (isAbsolute(output) || existsSync(output)) {
    return output;
  }
  const fromManifest = join(dirname(manifestPath), output);
  if (existsSync(fromManifest)) {
    return fromManifest;
  }
  return output;
}
