# Environment Setup

Use this when Cortex Harness is not installed, the `dev` command is missing, dependencies are broken, or database infrastructure is down.

## Discovery

1. Check whether `dev` is available:

```powershell
Get-Command dev -ErrorAction SilentlyContinue
```

2. Check for the standard local clone:

```powershell
Test-Path C:\ai\cortex-harness
```

3. If missing, clone it:

```powershell
git clone https://github.com/baka3k/cortex-harness.git C:\ai\cortex-harness
```

4. If present, update it without discarding local work:

```powershell
git -C C:\ai\cortex-harness status --short
git -C C:\ai\cortex-harness pull --ff-only
```

Stop and ask the user before pulling if there are local changes that may conflict.

## Install

From `C:\ai\cortex-harness`:

```powershell
make install
make build
```

If `make` is unavailable on Windows, use the repository scripts in this order:

```powershell
.\install-windows.ps1
.\dev.ps1 doctor
```

## Infrastructure

Start database services:

```powershell
make infra-up
```

Run health checks:

```powershell
make doctor
```

If `dev` is not on `PATH`, use:

```powershell
C:\ai\cortex-harness\.venv\Scripts\dev.exe status
```

## Windows Repairs

- If Python modules are missing, install the relevant requirements from `code-tiny` or `doc-tiny`.
- If CUDA PyTorch is required, install the CUDA wheel set that matches the local driver and GPU.
- If `dev` is not recognized, add `%USERPROFILE%\.local\bin` to `PATH` or use the `.venv\Scripts\dev.exe` fallback.
