# Dev Kit — skill installer and Cortex Harness bootstrap
# Run `make` (or `make help`) to list targets.

CORTEX_REPO  ?= https://github.com/baka3k/cortex-harness.git
CORTEX_DIR   ?= $(HOME)/AI/cortex-harness
# Install from this checkout; only bare `npx skill-dev` (install-latest) pulls the newest GitHub revision.
SKILL_SOURCE ?= .
SKILL_DEV    ?= npx --yes skill-dev

.DEFAULT_GOAL := help
.PHONY: help install install-latest doctor prepare

help:
	@echo "dev-kit targets:"
	@echo "  make install         Install skills from THIS local checkout ($(SKILL_SOURCE)) via skill-dev"
	@echo "  make install-latest  Install the newest skills from GitHub (baka3/dev-kit) instead"
	@echo "  make doctor          Health check: git/node/npx, uv, skills, Cortex 'dev' command"
	@echo "  make prepare         Clone cortex-harness into $(CORTEX_DIR) and install 'dev' (no-op if already installed)"
	@echo ""
	@echo "Variables: CORTEX_DIR=$(CORTEX_DIR)  CORTEX_REPO=$(CORTEX_REPO)  SKILL_SOURCE=$(SKILL_SOURCE)"

install:
	@echo "==> Installing skills from local checkout ($(SKILL_SOURCE)) — pick skills/agent/location in the installer"
	@$(SKILL_DEV) $(SKILL_SOURCE)

install-latest:
	@echo "==> Installing latest skills from GitHub (baka3/dev-kit)"
	@$(SKILL_DEV)

doctor:
	@echo "==> dev-kit doctor"
	@status=0; \
	fail() { printf '  [FAIL] %s\n' "$$1"; status=1; }; \
	warn() { printf '  [WARN] %s\n' "$$1"; }; \
	ok()   { printf '  [ OK ] %s\n' "$$1"; }; \
	if command -v git >/dev/null 2>&1; then ok "git: $$(git --version)"; else fail "git not found"; fi; \
	if command -v node >/dev/null 2>&1; then ok "node: $$(node --version)"; else fail "node not found (needed by skill-dev)"; fi; \
	if command -v npx >/dev/null 2>&1; then ok "npx: $$(command -v npx)"; else fail "npx not found (needed by skill-dev)"; fi; \
	if command -v python3 >/dev/null 2>&1; then ok "python3: $$(python3 --version 2>&1)"; else warn "python3 not found (uv can provision one for cortex-harness)"; fi; \
	if command -v uv >/dev/null 2>&1; then ok "uv: $$(uv --version 2>&1)"; else warn "uv not found — required by 'make prepare' (curl -LsSf https://astral.sh/uv/install.sh | sh)"; fi; \
	DEV=; \
	if command -v dev >/dev/null 2>&1; then DEV=dev; \
	elif [ -x "$$HOME/.local/bin/dev" ]; then DEV="$$HOME/.local/bin/dev"; fi; \
	if [ -n "$$DEV" ]; then ok "cortex 'dev' command: $$DEV"; else warn "cortex 'dev' not found — run 'make prepare' (if installed, add ~/.local/bin to PATH)"; fi; \
	if [ -d "$(CORTEX_DIR)/.git" ]; then ok "cortex checkout: $(CORTEX_DIR)"; else warn "no cortex checkout at $(CORTEX_DIR) — run 'make prepare'"; fi; \
	if [ -d "$$HOME/.agents/skills" ]; then \
		if [ -d "$$HOME/.agents/skills/hi-cortex" ]; then ok "skills installed (~/.agents/skills/hi-cortex present)"; \
		else warn "skills dir exists but hi-cortex is missing — run 'make install'"; fi; \
	else warn "no ~/.agents/skills — run 'make install'"; fi; \
	if [ -n "$$DEV" ]; then \
		echo "==> running cortex health check ($$DEV doctor)"; \
		$$DEV doctor || fail "'dev doctor' reported failures"; \
	fi; \
	exit $$status

prepare:
	@if command -v dev >/dev/null 2>&1 || [ -x "$$HOME/.local/bin/dev" ]; then \
		echo "==> 'dev' already installed — prepare is a no-op (never reinstall over a working installation)."; \
		echo "    To update: git -C $(CORTEX_DIR) pull, then run 'make doctor'."; \
		exit 0; \
	fi; \
	command -v uv >/dev/null 2>&1 || { echo "uv is required: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2; exit 1; }; \
	if [ -d "$(CORTEX_DIR)/.git" ]; then \
		echo "==> Reusing existing checkout at $(CORTEX_DIR)"; \
		git -C "$(CORTEX_DIR)" pull --ff-only || echo "    (pull skipped — continuing with current revision)"; \
	else \
		echo "==> Cloning $(CORTEX_REPO) into $(CORTEX_DIR)"; \
		git clone "$(CORTEX_REPO)" "$(CORTEX_DIR)"; \
	fi; \
	echo "==> Building cortex-harness"; \
	$(MAKE) -C "$(CORTEX_DIR)" build; \
	echo "==> Initializing storage"; \
	$(MAKE) -C "$(CORTEX_DIR)" storage-init; \
	echo "==> Installing 'dev' command"; \
	$(MAKE) -C "$(CORTEX_DIR)" install; \
	echo "==> Verifying with cortex doctor"; \
	$(MAKE) -C "$(CORTEX_DIR)" doctor; \
	echo "==> Cortex Harness ready — run 'dev help'"
