#!/usr/bin/env node
/**
 * Sync METADATA.json from git history.
 *
 * This script extracts version and last_updated information for each skill
 * by analyzing git log history. It updates the centralized METADATA.json
 * file at the repository root.
 *
 * Usage: node scripts/sync-metadata.mjs [--check]
 * Exit:  0 = METADATA.json written (or already in sync with --check), 1 = drift with --check.
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CHECK = process.argv.includes("--check");
const METADATA_PATH = resolve(ROOT, "METADATA.json");

// Get current git commit hash
const getGitHash = () => {
  try {
    return execSync("git rev-parse --short HEAD", { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return "unknown";
  }
};

// Get last commit date for a specific file
const getLastUpdated = (filePath) => {
  try {
    const date = execSync(`git log -1 --format=%cd --date=short -- "${filePath}"`, {
      cwd: ROOT,
      encoding: "utf8",
    }).trim();
    return date || "unknown";
  } catch {
    return "unknown";
  }
};

// Extract version from git log (looks for version patterns in commit messages)
const getVersion = (skillName) => {
  try {
    // Try to find version from git tags or commit messages
    const tag = execSync(
      `git describe --tags --abbrev=0 --match "${skillName}-*" 2>/dev/null || echo ""`,
      { cwd: ROOT, encoding: "utf8" }
    ).trim();
    
    if (tag) {
      // Extract version from tag like "hi-scout-v4.0.0"
      const match = tag.match(/v?(\d+\.\d+\.\d+)/);
      if (match) return match[1];
    }
    
    // Fallback: check commit messages for version bumps
    const log = execSync(
      `git log --oneline --grep="version" -- "${skillName}/" | head -5`,
      { cwd: ROOT, encoding: "utf8" }
    );
    
    // Look for version patterns in commit messages
    const versionMatch = log.match(/v?(\d+\.\d+\.\d+)/);
    if (versionMatch) return versionMatch[1];
    
    return "1.0.0"; // Default version
  } catch {
    return "1.0.0";
  }
};

// Discover all skills
const discoverSkills = () => {
  const skills = [];
  const dirs = execSync("ls -d */", { cwd: ROOT, encoding: "utf8" })
    .trim()
    .split("\n")
    .map((d) => d.replace("/", ""));
  
  for (const dir of dirs) {
    const skillPath = resolve(ROOT, dir, "SKILL.md");
    if (existsSync(skillPath)) {
      skills.push(dir);
    }
  }
  
  return skills.sort();
};

// Build metadata object
const buildMetadata = () => {
  const skills = discoverSkills();
  const metadata = {
    kit_version: getGitHash(),
    last_updated: new Date().toISOString().split("T")[0],
    skills: {},
  };
  
  for (const skill of skills) {
    metadata.skills[skill] = {
      version: getVersion(skill),
      last_updated: getLastUpdated(`${skill}/SKILL.md`),
    };
  }
  
  return metadata;
};

// Main execution
const main = () => {
  const newMetadata = buildMetadata();
  const newContent = JSON.stringify(newMetadata, null, 2) + "\n";
  
  if (CHECK) {
    if (!existsSync(METADATA_PATH)) {
      console.error("METADATA.json does not exist. Run without --check to create it.");
      process.exit(1);
    }
    
    const existing = readFileSync(METADATA_PATH, "utf8");
    if (existing === newContent) {
      console.log("✓ METADATA.json is in sync");
      process.exit(0);
    } else {
      console.error("✗ METADATA.json is out of sync. Run: node scripts/sync-metadata.mjs");
      process.exit(1);
    }
  }
  
  writeFileSync(METADATA_PATH, newContent);
  console.log(`✓ Updated METADATA.json with ${Object.keys(newMetadata.skills).length} skills`);
  console.log(`  Kit version: ${newMetadata.kit_version}`);
  console.log(`  Last updated: ${newMetadata.last_updated}`);
};

main();
