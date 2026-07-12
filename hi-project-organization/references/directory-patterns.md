# Directory Patterns

Use these defaults only when the repository has no established structure.

## Documentation

```text
docs/
├── system-architecture.md
├── code-standards.md
├── logs/{YYMMDD-HHmm}-{slug}.md
├── decisions/{YYMMDD}-{slug}.md
└── guides/{topic}.md
```

- Keep evergreen documents untimestamped.
- Timestamp logs and architecture decisions.
- Split large documents by topic when that improves navigation.

## Plans

```text
plans/
├── {YYMMDD-HHmm}-{slug}/
│   ├── plan.md
│   ├── phase-{NN}-{name}.md
│   ├── research/
│   └── reports/
├── research/
├── reports/
├── templates/
└── visuals/
```

- Zero-pad phase numbers.
- Keep scoped artifacts inside their plan; use top-level research or reports only for standalone work.
- Keep `plan.md` concise and link detailed phase files.

## Tests

```text
tests/
├── unit/
├── integration/
├── e2e/
├── fixtures/
└── helpers/
```

Follow the existing test root and suffix convention. Mirror source structure where practical.

## Scripts

Use `scripts/{action}-{target}.{ext}`. Group scripts by category only when the collection is large enough to benefit from navigation. Include a shebang where required.

## Assets

```text
assets/
├── images/
├── videos/
├── designs/
├── branding/
└── generated/{type}/
```

- Keep single assets flat and multi-file outputs self-contained.
- Express size, platform, and theme variants as filename suffixes.
- Timestamp generated content when its creation time matters.

## Configuration

Keep ecosystem-mandated files such as manifests and compiler configs at their standard paths. Put tool configs in `.config/` only when the tool and repository support it. Never relocate secrets or commit populated `.env` files.

