# Problem-Solving Skills - Attribution

These skills were derived from agent patterns in the Microsoft Amplifier project.

## Source Repository

- **Name:** Amplifier
- **URL:** https://github.com/microsoft/amplifier
- **Commit:** 2adb63f858e7d760e188197c8e8d4c1ef721e2a6
- **Date:** 2025-10-10

## Skills Derived from Amplifier Agents

### From insight-synthesizer agent:
- **simplification-cascades** - Finding insights that eliminate multiple components
- **collision-zone-thinking** - Forcing unrelated concepts together for breakthroughs
- **meta-pattern-recognition** - Spotting patterns across 3+ domains
- **inversion-exercise** - Flipping assumptions to reveal alternatives
- **scale-game** - Testing at extremes to expose fundamental truths

### Dispatch pattern:
- **when-stuck** - Maps stuck-symptoms to appropriate technique

## What Was Adapted

The Amplifier agents are specialized long-lived agents with structured JSON output. These skills extract the core problem-solving techniques and adapt them as scannable quick-reference guides (~60-80 lines each) with symptom-based discovery, immediate application without special tooling, composable patterns through dispatch system, and progressive disclosure via SKILL.md + references structure.

The core insight: agent capabilities are domain-agnostic patterns. Whether packaged as "amplifier agent" or "problem-solving skill", the underlying technique is the same. We extracted the techniques and made them portable, immediately applicable, token-efficient through progressive disclosure, discoverable through symptom-matching, and combinable for complex problems. Original Amplifier project uses MIT License; these adapted skills maintain attribution and follow the same open spirit.

## Adaptation Notes

- Converted from long-lived agent to scannable reference
- Added symptom-based dispatch system, removed JSON output requirements
- Added concrete examples, structured for progressive disclosure
