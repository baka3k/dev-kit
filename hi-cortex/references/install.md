# Installing the Cortex `dev` Command

Follow this file only when the preflight fails: `command -v dev` is empty **and**
`"$HOME/.local/bin/dev"` does not exist. If `dev` is already installed, skip straight to the
sync recipes — never reinstall over a working installation without being asked.

## Preflight

```bash
command -v dev || [ -x "$HOME/.local/bin/dev" ] && echo "dev present"
```

- A `dev` wrapper may pin its own checkout — read `~/.local/bin/dev` to find
  `CORTEX_HARNESS_DIR` before assuming anything about the repository location.
- If `dev` exists but errors, run `dev doctor` first; reinstall only on its explicit advice.

## Prerequisites

- git, Python 3.12+, and `uv` (`uv --version`; install uv first if missing — pass
  `make build UV=/path/to/uv` when it is off the default `PATH`).
- macOS/Linux bash or Windows PowerShell. Qdrant and FalkorDBLite run as embedded file-backed
  libraries: no database daemon or container is required for local backends.

## Install (once per machine)

The checkout location is the user's decision — never invent one. Reuse the checkout an existing
wrapper points at, or clone to a user-approved directory:

```bash
git clone https://github.com/baka3k/cortex-harness.git <target-dir>
cd <target-dir>
make build          # create/reuse .venv and install dependencies with uv
make storage-init   # create ~/.cortext-harness/v1/instances/default + manifest
make install        # install the global `dev` command into ~/.local/bin
make doctor         # embedded Qdrant/FalkorDBLite round-trips + MCP port diagnostics
```

Verify `dev help` runs from any directory; `~/.local/bin` must stay on `PATH` — when an agent
shell cannot find `dev`, export `PATH="$HOME/.local/bin:$PATH"` before declaring it missing.
The install is editable: `git pull` inside the checkout updates it, no reinstall.
`make uninstall` removes the global command.

## First config (once per indexed project root)

- `dev init --project-dir <project-root>` is an **interactive wizard**: answer prompts only with
  user-provided values; Enter accepts defaults (project id, `local` backend, falkordb provider).
  An agent must never guess wizard answers.
- Confirm with `dev status` — it shows the resolved FalkorDB path, Qdrant directory, vector
  collection, embedding model, and registered source/doc folders.
- Backend defaults to `local` (ports pinned to `127.0.0.1`). Choose `remote` only on explicit
  user instruction; the wizard will prompt for credentials.

## Hygiene

- `.cortext-harness/config/{env}.json` stores settings — and remote credentials — in
  **plaintext**: never commit populated configs, never echo their contents into logs or reports.
- Never run bare `dev stop` (it stops every MCP); always scope with `--name`.
- `CORTEX_DATA_HOME` / `CORTEX_STORAGE_INSTANCE` give an isolated data root for tests so the
  default instance stays untouched.
