---
name: scienceplots-viz
description: How to create scientific visualizations with SciencePlots and LaTeX. Use this skill whenever the user wants to create publication-quality plots, scientific figures, data visualizations with matplotlib, or needs to follow the project's strict plotting standards. This includes 24h load profiles, energy visualizations, quantile shading, statistical annotations, or any matplotlib plotting in this repository. Also use this skill for any Python coding tasks in this project - it contains all the coding standards, path handling requirements, and implementation workflows. Make sure to use this skill even if the user doesn't explicitly mention "SciencePlots" - if they're asking for plots, charts, figures, or Python scripts in this project, trigger this skill.
---

# SciencePlots Visualization

A skill for creating publication-quality scientific visualizations using Matplotlib with SciencePlots styles and LaTeX typesetting, and for implementing Python scripts following project standards.

## Domain

Data visualization, scientific plotting, Python implementation

## When to Use

Use this skill whenever:

- Creating any matplotlib plot, chart, or figure
- Working with scientific data visualization
- Needing publication-quality plots with LaTeX typesetting
- Creating 24h time-series profiles (energy load curves, daily patterns)
- Adding statistical annotations (average, peak values)
- Visualizing uncertainty with quantile shading
- Following the project's plotting standards
- **Writing any Python code in this repository**
- **Creating or modifying scripts**
- **Implementing data processing or analysis**

## Core Mandates

These are absolute requirements that MUST be followed in all implementations:

### Path Handling

ALWAYS use `pathlib.Path` for all path operations. Scripts MUST work from any execution directory.

**NEVER use:**

- `os.chdir()` - changing directory is forbidden
- `sys.path.insert()` - manipulating import paths is forbidden
- String concatenation for paths (e.g., `dir + "/" + file`)

**ALWAYS use:**

```python
from pathlib import Path

# Correct - works from any directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Correct - relative to script location
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
```

### Plotting Excellence

Adhere strictly to the Matplotlib Object-Oriented API and the project's custom styling:

- **ALWAYS** use `fig, ax = plt.subplots()` instead of `plt.plot()`
- **ALWAYS** call `configure_matplotlib_style()` at the start
- **ALWAYS** use professional LaTeX typesetting for labels
- **ALWAYS** save plots using `save_plot(fig, filename)`

### Reliability

All findings MUST be reproducible via permanent, executable scripts:

- No interactive-only code
- All scripts must be runnable from command line
- Include `if __name__ == "__main__":` blocks
- Document dependencies and usage

## Implementation Workflow

### 1. Check Existing Utilities

Before implementing custom logic, check:

- `src/scienceplots_toolkit/utils.py` - Common plotting helpers
- `src/scienceplots_toolkit/analysis.py` - Advanced analysis tools

Common utilities:

- `save_plot(fig, filename)` - Save to PNG and PDF
- `configure_24h_axis(ax)` - Set up 0-24h x-axis
- `add_stats_box(ax, avg, peak)` - Add statistical annotations
- `plot_profile_with_quantiles(ax, x, mean, q10, q90)` - Uncertainty shading
- `generate_profile_grid(n_rows, n_cols)` - Multi-panel layouts

### 2. Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from scienceplots_toolkit import configure_matplotlib_style, save_plot
from scienceplots_toolkit.utils import configure_24h_axis, add_stats_box
```

### 3. Implementation Standards

- **Type hints**: Use modern type hints (`list[str]`, `tuple[float, ...]`)
- **Strings**: Use f-strings for formatting
- **Spelling**: Use British English in docstrings (e.g., "standardise", "colour")
- **Docstrings**: Include Args sections for all functions
- **LaTeX labels**: Use raw strings: `r"$\sin(x)$"`, `r"Power (kW)"`

### 4. Plotting Guidelines

- **LaTeX typesetting**: Professional math mode for all labels and units
- **Constrained layout**: Active by default (don't disable)
- **Saving**: Always save both PNG and PDF formats
- **Cleanup**: Always call `plt.close(fig)` after saving
- **24h profiles**: Use `configure_24h_axis(ax)` for daily time series
- **Statistics**: Use `add_stats_box()` for average/peak annotations
- **Uncertainty**: Use `plot_profile_with_quantiles()` for shaded regions

### 5. Verification

After implementation:

```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
uv run ty check .
```

## Example

```python
"""Generate a 24h load profile with uncertainty shading."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scienceplots_toolkit import configure_matplotlib_style, save_plot
from scienceplots_toolkit.utils import configure_24h_axis, add_stats_box
from scienceplots_toolkit.analysis import plot_profile_with_quantiles

def main() -> None:
    """Generate example 24h load profile."""
    configure_matplotlib_style(use_latex=True)
    
    # Generate mock data
    x = np.arange(24)
    mean = 5 + 3 * np.exp(-((x - 19) ** 2) / 20)
    q10 = mean * 0.8
    q90 = mean * 1.2
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_profile_with_quantiles(
        ax, x, mean, q10, q90,
        label="Load Profile",
        color="C0"
    )
    
    configure_24h_axis(ax)
    add_stats_box(ax, avg=mean.mean(), peak=mean.max(), unit=r"\text{kW}")
    
    ax.set_xlabel(r"Time of Day (h)")
    ax.set_ylabel(r"Power Consumption (kW)")
    ax.legend()
    
    # Save and cleanup
    save_plot(fig, "load_profile")
    plt.close(fig)

if __name__ == "__main__":
    main()
```

## Quality Checklist

Before considering a visualization or script complete:

- [ ] Paths use `pathlib.Path` (not strings or `os.chdir()`)
- [ ] British English spelling in docstrings
- [ ] Matplotlib Object-Oriented API used (`fig, ax = plt.subplots()`)
- [ ] `configure_matplotlib_style()` called at start
- [ ] LaTeX math mode for labels and units
- [ ] Both PNG and PDF formats saved
- [ ] `plt.close(fig)` called after saving
- [ ] Type hints present on all functions
- [ ] Docstrings with Args sections
- [ ] Script works from any execution directory
- [ ] No `os.chdir()` or `sys.path.insert()` calls

## Bundled Resources

- `scripts/` - Executable utilities for common tasks
- `references/` - Documentation on matplotlib best practices, coding standards
- `assets/` - Templates and style configurations

## Related Files

- `src/scienceplots_toolkit/style.py` - Style configuration
- `src/scienceplots_toolkit/utils.py` - Utility functions
- `src/scienceplots_toolkit/analysis.py` - Analysis tools
- `examples/` - Working example scripts
- `PUBLICATION_PLAN.md` - PyPI publication workflow
- `CHANGELOG.md` - Version history
