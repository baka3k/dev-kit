# Git Output Normalization

Git emits metadata, hunk headers, unchanged context lines, and verbose
author/committer blocks that add tokens but rarely aid reasoning. Normalize
raw git output **before** synthesis so only decision-relevant text enters context.

## Tool

Use `scripts/git-normalize.js` — a cross-platform Node.js tool that reads raw
git output from stdin, strips noise, and returns clean text. Runs identically
on macOS, Windows, and Linux. Prefer the tool over hand-rolled pipes.

```bash
git show <commit> | node scripts/git-normalize.js                  # default cleanup
git show <commit> | node scripts/git-normalize.js --changed        # diff body only
git log -p         | node scripts/git-normalize.js --changed --max-lines 400
```

| Flag | Effect |
| --- | --- |
| *(none)* | Strip ANSI codes, drop commit metadata, collapse blank lines, cap 200 lines |
| `-c, --changed` | Keep only file headers + `+`/`-` lines; drop unchanged context |
| `--max-lines N` | Cap to N lines (default 200; `0` = no cap) |

What the tool strips: ANSI escape codes, `tree`/`parent`/`object`/`type`/`tag`/
`author`/`committer`/`gpgsig`/`encoding`/`index` metadata lines, `Date:` lines,
runs of blank lines. What it keeps: commit subject, file paths, `+`/`-` lines,
hunk markers, blame author + code.

## Principles

1. **Summarize first.** Use `--stat` / `--oneline` to gauge scope; pull full
   diffs only when the summary does not answer the question.
2. **Run the tool on any verbose output** that will enter synthesis.
3. **Use `--changed`** when the diff exceeds ~100 lines to drop unchanged context.
4. **Cap size.** Default 200 lines is tuned for token budget; raise only when
   the agent needs more diff body.

## Commands

### Level 0 — Summarize (always start here)

```bash
git log --oneline --decorate -20                       # scope before detail
git show <commit> --stat --format="%h %s"              # files changed, no body
```

### Level 1 — Compact log (no tool needed)

```bash
git log --format="%h|%ad|%an|%s" --date=short -20
```

### Level 2 — Full diff, normalized (default)

```bash
git show <commit> | node scripts/git-normalize.js
```

### Level 3 — Changed lines only (large diffs)

```bash
git show <commit> | node scripts/git-normalize.js --changed
```

### Blame — author + date + code only

```bash
git blame -L <start>,<end> --date=short <file>
```

## Token Caps

| Output | Cap |
| --- | --- |
| Per git command | ~2 KB / 200 lines (`--max-lines`), then truncate |
| Commit hash | short form (7 chars) |
| Diff body | use `--changed` when > 100 lines |
| Multi-commit log | newest 20 first; request older only if needed |
