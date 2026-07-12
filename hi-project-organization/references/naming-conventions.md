# Naming Conventions

## Slugs

Convert a title to lowercase, replace spaces and special characters with hyphens, collapse repeated hyphens, trim edge hyphens, and truncate at a word boundary to 50 characters.

| Input | Slug |
| --- | --- |
| `User Authentication Flow` | `user-authentication-flow` |
| `Fix: API Rate Limiting Bug #42` | `fix-api-rate-limiting-bug-42` |
| `AI & Automation: A Guide` | `ai-automation-a-guide` |

Prefer self-documenting names over abbreviations.

## Time

Use `$HI_PLAN_DATE_FORMAT` or default to `YYMMDD-HHmm`.

- Timestamp plans, reports, logs, sessions, and time-sensitive generated content.
- Do not timestamp evergreen docs, configs, source, scripts, templates, or brand assets.

## Variants

| Variant | Pattern | Example |
| --- | --- | --- |
| Size | `{name}-{width}x{height}.{ext}` | `hero-1920x1080.png` |
| Platform | `{name}-{platform}.{ext}` | `cover-youtube.png` |
| Theme | `{name}-{variant}.{ext}` | `logo-dark.svg` |
| Version | `{name}-v{N}.{ext}` | `mockup-v2.png` |
| Sequence | `{kind}-{NN}-{name}.{ext}` | `step-01-install.md` |

## Code and Directories

Follow the repository's existing language conventions for code. Use kebab-case for new non-code directories, plural names for collections, and zero-padded sequence numbers for lexical sorting.

## Plans and Reports

- Plan folder: `{YYMMDD-HHmm}-{slug}/`
- Standalone report: `{type}-{YYMMDD-HHmm}-{slug}.md`
- Plan-scoped report: use a stable descriptive name inside the plan's `reports/` directory.

