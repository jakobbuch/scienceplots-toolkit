---
name: Python Standards
description: Python coding standards and best practices for scienceplots-toolkit
---

# Python Standards

This document defines the Python coding standards for the `scienceplots-toolkit` package.

## Code Style

### Formatting

- **Tool**: `ruff format` (Black-compatible)
- **Line length**: 88 characters (default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings

### Linting

- **Tool**: `ruff check`
- **Rules**: All default ruff rules enabled
- **Fix**: Run `ruff check . --fix` to auto-fix issues

### Type Checking

- **Tool**: `ty`
- **Requirement**: All public functions must have type annotations
- **No suppression**: Never use `# type: ignore` without justification

## Naming Conventions

- **Functions**: `snake_case` (e.g., `configure_matplotlib_style`)
- **Classes**: `PascalCase` (e.g., `PreambleManager`)
- **Constants**: `UPPER_CASE` (e.g., `DEFAULT_DPI`)
- **Private**: Leading underscore (e.g., `_internal_helper`)

## Documentation

### Docstrings

Use Google-style docstrings for all public functions:

```python
def save_plot(
    fig: "Figure",
    name: str,
    output_dir: Path | None = None,
    dpi: int = 300,
) -> None:
    """Save a matplotlib figure to PNG and PDF formats.

    Args:
        fig: Matplotlib figure to save
        name: Filename (without extension)
        output_dir: Output directory (default: "output")
        dpi: Resolution for PNG export (default: 300)
    """
```

### Type Annotations

All function signatures must include type annotations:

```python
# ✅ GOOD
def calculate_mean(data: np.ndarray) -> float:
    return float(data.mean())

# ❌ BAD
def calculate_mean(data):
    return data.mean()
```

## Error Handling

### Raise Specific Exceptions

```python
# ✅ GOOD
if len(data) == 0:
    raise ValueError("Data array cannot be empty")

# ❌ BAD
if len(data) == 0:
    raise Exception("Error")
```

### Use Context Managers

```python
# ✅ GOOD
with Path.open("file.txt") as f:
    content = f.read()

# ❌ BAD
f = Path.open("file.txt")
content = f.read()
f.close()
```

## Testing

### Coverage Requirement

- **Minimum**: 90% line coverage
- **Tool**: `pytest-cov`
- **Command**: `uv run pytest tests/ --cov=scienceplots_toolkit`

### Test Organization

- **File naming**: `test_*.py`
- **Class naming**: `Test*ClassName*`
- **Method naming**: `test_*_behavior`

### Fixtures

Use `conftest.py` for shared fixtures:

```python
@pytest.fixture
def sample_data() -> np.ndarray:
    """Generate sample data for testing."""
    return np.arange(24)
```

## Imports

### Order

1. Standard library imports
2. Third-party imports
3. Local imports

### Style

```python
# ✅ GOOD
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from scienceplots_toolkit import configure_matplotlib_style

# ❌ BAD
import numpy as np, matplotlib.pyplot as plt
from scienceplots_toolkit import *
```

## Path Handling

### Use pathlib

```python
# ✅ GOOD
from pathlib import Path
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

# ❌ BAD
import os
output_dir = "output"
os.makedirs(output_dir)
```

### Never Change Directory

```python
# ✅ GOOD
output_path = OUTPUT_DIR / "plot.png"

# ❌ BAD
os.chdir("output")
```

## Related Documentation

- **[AGENTS.md](AGENTS.md)**: Agent mandates
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Development workflow
