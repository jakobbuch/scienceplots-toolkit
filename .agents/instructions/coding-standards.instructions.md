---
description: "Detailed Python coding standards, styling, and organization rules."
applyTo: "**/*.py"
---

# Coding Standards

Follow these rules for all Python code in this repository.

## Path Handling

- Use `pathlib.Path` for all path operations (cross-platform compatibility)
- Assume scripts are executed with `uv` (e.g., `uv run script.py`) which
  standardises the environment and working directory.
- Use `Path(__file__).parent` to resolve paths relative to the script location.
- Never use string concatenation for paths

## Code Style

- Keep code simple and readable - avoid unnecessary complexity
- Use try-except only where errors are expected (API calls, file I/O,
  subprocess, network)
- Do NOT wrap every method in try-except blocks
- Prefer flat code over deeply nested structures
- Avoid decorative symbols in output - keep it professional

## Code Organization

- Define all configurable values as UPPER_CASE constants in the file header
- Group related constants together with comments
- Use functions for reusable logic
- When adding new features: refactor similar existing functions into one generic
  function instead of creating duplicates

## Functions

- One function should do one thing
- If two functions share >50% logic, combine them with parameters
- Prefer parameters over hardcoded values inside functions
- Add docstrings to all functions explaining purpose, parameters, and return
  values

## Python Specific

- Use `subprocess.run()` instead of `os.system()`
- Use f-strings for string formatting
- Use `pathlib` or `os.path` - never string concatenation for paths
- Use type hints for function parameters and return values
- When accessing datetime properties of a DataFrame index (e.g.,
  `df.index.hour`), explicitly cast the index to `pd.DatetimeIndex` to satisfy
  `mypy`: `df.index = pd.DatetimeIndex(df.index)`

## Tooling & Environment

- Use `uv` for dependency management and script execution (`uv run script.py`)
- Code must pass `ruff` linting:
  - No multiple statements on one line (e.g., `if x: return y` must be split)
  - Remove unused variables
  - Sort imports
- Code must pass `mypy` and `ty` type checking
