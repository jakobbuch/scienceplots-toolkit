---
name: scienceplots-viz
description: Expert guidance for creating publication-quality scientific visualizations with Matplotlib, SciencePlots, and LaTeX. Use this skill for any Python coding tasks, data visualization, plotting, or implementation work in this repository. This includes 24h load profiles, energy visualizations, quantile shading, statistical annotations, batch orchestration, or any matplotlib plotting. Make sure to use this skill even if the user doesn't explicitly mention "SciencePlots" - if they're asking for plots, charts, figures, or Python scripts in this project, trigger this skill.
---

# SciencePlots Visualization

This skill provides authoritative guidance for using the `scienceplots_toolkit` package. It ensures consistent, publication-quality scientific visualizations using Matplotlib, SciencePlots, LaTeX typesetting, and the `cmap` colormaps library.

!!! danger "Mandate"
    This skill is **authoritative** for all plotting and Python implementation tasks. Changes to standards must be tracked in project documentation.

---

## When to Use This Skill

**Always use this skill when:**

- Creating scientific plots for publications, reports, or presentations
- Working with 24-hour time series profiles (energy, load, demand data)
- Needing consistent styling across multiple figures
- Using quantile shading or statistical annotations
- Creating multi-panel figure grids for comparative analysis
- Batch-generating multiple plots with the CLI orchestrator
- Writing any Python code in this repository
- Implementing data processing or analysis scripts

**Do NOT use this skill when:**

- Quick exploratory plots during debugging (use plain Matplotlib)
- Non-scientific visualizations (charts, dashboards, web UIs)
- The user explicitly requests custom styling that conflicts with standards

---

## Core Principles

### 1. Object-Oriented API Mandate

<!-- rule:S-0701 -->

**ALWAYS** use the Object-Oriented API. **NEVER** use the pyplot state machine:

```python
# ✅ CORRECT
fig, ax = plt.subplots()
ax.plot(x, y)

# ❌ WRONG
plt.plot(x, y)
```

### 2. Style Configuration First

<!-- rule:S-0702 -->

**ALWAYS** call `configure_matplotlib_style()` **before** creating any figures:

```python
# ✅ CORRECT - Configure first
configure_matplotlib_style(fontsize=26)
fig, ax = plt.subplots()

# ❌ WRONG - Configure after creating figure
fig, ax = plt.subplots()
configure_matplotlib_style(fontsize=26)  # Won't apply to existing fig
```

### 3. Minimal Scaffolding

<!-- rule:S-0703 -->

Only import what you need. Do not import entire modules when using specific functions:

```python
# ✅ CORRECT - Import only needed functions
from scienceplots_toolkit import configure_matplotlib_style, save_plot

# ❌ WRONG - Importing everything when only using two functions
from scienceplots_toolkit import *
```

### 4. Path Handling Excellence

<!-- rule:S-0704 -->

**ALWAYS** use `pathlib.Path` for all path operations. Scripts MUST work from any execution directory:

```python
from pathlib import Path

# ✅ CORRECT - Works from any directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ❌ WRONG - String concatenation
output_dir = "output"
os.chdir(output_dir)  # NEVER change directory
```

---

## Core Patterns

<!-- rule:S-0705 -->

### Style Configuration

Always configure the style **before** creating any figures:

```python
from scienceplots_toolkit import configure_matplotlib_style
import matplotlib.pyplot as plt

# Configure once at the start
configure_matplotlib_style(fontsize=26, figsize=(16, 10))

# Then create plots
fig, ax = plt.subplots()
```

### 24h Axis Standardization

**ALWAYS** apply `configure_24h_axis()` to daily profile plots:

```python
from scienceplots_toolkit.utils import configure_24h_axis

fig, ax = plt.subplots()
ax.plot(hours, load)
configure_24h_axis(ax)  # Sets 0-24 range, ticks every 4 hours
```

### Units Convention

**ALWAYS** use LaTeX-formatted units in labels:

```python
# ✅ CORRECT
ax.set_ylabel(r"Power (kW)")
ax.set_xlabel(r"Time (h)")

# ❌ WRONG
ax.set_ylabel("Power in kW")
ax.set_xlabel("Time in hours")
```

### Saving Convention

**ALWAYS** use `save_plot()` for output. It saves both PNG and PDF:

```python
from scienceplots_toolkit import save_plot

save_plot(fig, "daily_load_profile", dpi=300)
# Creates: output/daily_load_profile.png
#          output/daily_load_profile.pdf
```

### Statistical Annotations

Use `add_stats_box()` for mean/peak statistics, not inline text:

```python
from scienceplots_toolkit.utils import add_stats_box

add_stats_box(ax, avg=125.4, peak=210.8, unit=r"\text{kW}")
```

### Quantile Shading

Use `plot_profile_with_quantiles()` for uncertainty bands:

```python
from scienceplots_toolkit import plot_profile_with_quantiles

plot_profile_with_quantiles(
    ax, x=hours, mean=mean_profile, q10=p10, q90=p90,
    label="Mean load",
)
```

### Multi-Panel Grids

Use `generate_profile_grid()` for comparative figures:

```python
from scienceplots_toolkit import generate_profile_grid

fig, axes = generate_profile_grid(n_rows=3, n_cols=2, sharey="row")
for ax, data in zip(axes, datasets):
    # Plot on each axis
```

---

## Key Functions

### `configure_matplotlib_style()`

Configure global Matplotlib style with SciencePlots.

```python
configure_matplotlib_style(
    fontsize=26,           # Base font size
    figsize=(16, 10),      # Figure dimensions
    use_latex=False,       # Enable LaTeX rendering
    grid=True,             # Show grid lines
)
```

### `save_plot()`

Save figure to PNG and PDF in `output/` directory.

```python
save_plot(fig, "filename_base", dpi=300)
```

### `configure_24h_axis()`

Apply standard 24-hour time axis (0-24, ticks every 4h).

```python
configure_24h_axis(ax)
```

### `add_stats_box()`

Add statistical annotation box.

```python
add_stats_box(ax, avg=125.4, peak=210.8, unit=r"\text{kW}")
```

### `plot_profile_with_quantiles()`

Plot mean line with 10th-90th percentile shading.

```python
plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Mean")
```

### `generate_profile_grid()`

Create multi-panel figure grid.

```python
fig, axes = generate_profile_grid(n_rows=3, n_cols=2, sharey="row")
```

### `calculate_daily_stats()`

Compute daily statistics (mean, q10, q90, peak, min) from time-series data.

```python
from scienceplots_toolkit.analysis import calculate_daily_stats

stats = calculate_daily_stats(timestamps, data)
# Returns: DailyStats(mean, q10, q90, peak, min, timestamps)
```

### `PreambleManager`

Build LaTeX preamble with package management.

```python
from scienceplots_toolkit.latex import PreambleManager

preamble = PreambleManager.default().add_package("hyperref").build()
```

---

## Complete Example

```python
"""Generate a 24h load profile with uncertainty shading."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from scienceplots_toolkit import (
    configure_matplotlib_style,
    save_plot,
    plot_profile_with_quantiles,
)
from scienceplots_toolkit.utils import configure_24h_axis, add_stats_box

# 1. Configure style (do this once)
configure_matplotlib_style(fontsize=26, figsize=(14, 7))

# 2. Create figure
fig, ax = plt.subplots()

# 3. Generate data
hours = np.arange(25)
mean = np.sin(hours / 24 * 2 * np.pi) * 100 + 150
q10 = mean - 30
q90 = mean + 30

# 4. Apply standards
configure_24h_axis(ax)
plot_profile_with_quantiles(ax, hours, mean, q10, q90, label="Mean load")
add_stats_box(ax, avg=mean.mean(), peak=mean.max(), unit=r"\text{kW}")

ax.set_xlabel(r"Time of Day (h)")
ax.set_ylabel(r"Power Consumption (kW)")
ax.legend()

# 5. Save
save_plot(fig, "daily_load_profile", dpi=300)
plt.close(fig)
```

---

## Tool Documentation

For detailed API specifications and plotting standards, read:

- **Style Configuration**: [`src/scienceplots_toolkit/style.py`](src/scienceplots_toolkit/style.py)
- **Utilities**: [`src/scienceplots_toolkit/utils.py`](src/scienceplots_toolkit/utils.py)
- **Analysis Tools**: [`src/scienceplots_toolkit/analysis.py`](src/scienceplots_toolkit/analysis.py)
- **LaTeX Management**: [`src/scienceplots_toolkit/latex.py`](src/scienceplots_toolkit/latex.py)
- **CLI Orchestrator**: [`src/scienceplots_toolkit/cli.py`](src/scienceplots_toolkit/cli.py)

For examples and usage patterns, read:

- **Basic Examples**: [`examples/example_basic.py`](examples/example_basic.py)
- **Energy Profiles**: [`examples/example_energy.py`](examples/example_energy.py)
- **Orchestrator**: [`examples/example_orchestrator.py`](examples/example_orchestrator.py)

For installation and dependency information, read:

- **README**: [`README.md`](README.md)
- **CHANGELOG**: [`CHANGELOG.md`](CHANGELOG.md)

---

## Parallel Execution & Statelessness

This skill is **stateless and parallel-safe**:

- **No Session State**: Does not maintain any session-specific state between invocations
- **Idempotent Operations**: All guidance and operations can be safely repeated
- **Parallel-Safe**: Multiple agents can safely use this skill simultaneously
- **Harness-Agnostic**: Works identically across all agent harnesses (Opencode, Cursor, Cline, Windsurf, Claude Code)

### Coordination for Parallel Work

When multiple agents use this skill:

1. **Clear Boundaries**: Each agent works on independent tasks/modules
2. **Shared Standards**: All agents follow the same documented patterns
3. **No Conflicts**: Operations are designed to avoid file collisions
4. **Verification**: Run validation after merging parallel work

### Best Practices

- Coordinate on shared abstractions before implementation
- Use task IDs for tracking parallel work
- Verify consistency with project standards after merging
- Document findings in wiki for shared knowledge

---

## Quality Checklist

Before considering a visualization or script complete:

- [ ] English spelling in docstrings
- [ ] Matplotlib Object-Oriented API used (`fig, ax = plt.subplots()`)
- [ ] `configure_matplotlib_style()` called at start
- [ ] LaTeX math mode for labels and units
- [ ] Both PNG and PDF formats saved
- [ ] `plt.close(fig)` called after saving
- [ ] Type hints present on all functions
- [ ] Docstrings with Args sections
- [ ] Script works from any execution directory

---

## Bundled Resources

- `scripts/` - Executable utilities for common tasks
- `references/` - Documentation on matplotlib best practices, coding standards
- `assets/` - Templates and style configurations

---

## Related Files

- `src/scienceplots_toolkit/style.py` - Style configuration
- `src/scienceplots_toolkit/utils.py` - Utility functions
- `src/scienceplots_toolkit/analysis.py` - Analysis tools
- `src/scienceplots_toolkit/latex.py` - LaTeX preamble management
- `src/scienceplots_toolkit/cli.py` - CLI orchestration framework
- `examples/` - Working example scripts
- `PUBLICATION_PLAN.md` - PyPI publication workflow
- `CHANGELOG.md` - Version history
