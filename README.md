# SciencePlots Toolkit

[![PyPI - Version](https://img.shields.io/pypi/v/scienceplots-toolkit.svg)](https://pypi.org/project/scienceplots-toolkit)
[![Python Version](https://img.shields.io/pypi/pyversions/scienceplots-toolkit)](https://pypi.org/project/scienceplots-toolkit)
[![License](https://img.shields.io/pypi/l/scienceplots-toolkit)](https://github.com/jakobbuch/scienceplots-toolkit/blob/main/LICENSE)

Publication-quality Matplotlib plotting utilities with SciencePlots styles and LaTeX typesetting.

## Features

- **Pre-configured SciencePlots styles** with professional defaults
- **LaTeX typesetting** for mathematical expressions and units
- **24-hour time axis** utilities for daily profiles
- **Statistical annotations** for average/peak values
- **Quantile shading** for uncertainty visualization
- **Multi-panel grid** generation for comparative plots

## Installation

### From PyPI

```bash
pip install scienceplots-toolkit
```

### From source with uv

```bash
git clone https://github.com/jakobbuch/scienceplots-toolkit.git
cd scienceplots-toolkit
uv sync
```

### From source with pip

```bash
git clone https://github.com/jakobbuch/scienceplots-toolkit.git
cd scienceplots-toolkit
pip install -e .
```

## Quick Start

```python
from scienceplots_toolkit import configure_matplotlib_style, save_plot
from scienceplots_toolkit.utils import configure_24h_axis, add_stats_box
import matplotlib.pyplot as plt
import numpy as np

# Configure the style
configure_matplotlib_style(use_latex=True)

# Create a simple plot
fig, ax = plt.subplots()
x = np.linspace(0, 10, 400)
ax.plot(x, np.sin(x), label=r"$\sin(x)$")
ax.set_xlabel(r"Time (s)")
ax.set_ylabel(r"Amplitude")
ax.legend()

# Save the plot
save_plot(fig, "my_first_plot")
```

## Examples

### Basic Plots

Run the basic examples to see all features in action:

```bash
# Without LaTeX (uses mathtext)
uv run examples/example_basic.py

# With LaTeX rendering (requires LaTeX installation)
uv run examples/example_basic.py --latex
```

### Energy Profiles

Advanced examples with 24h load profiles and quantile shading:

```bash
uv run examples/example_energy.py
uv run examples/example_energy.py --latex
```

Generated plots are saved to the `output/` directory in both PNG and PDF formats.

## API Reference

### Style Configuration

```python
from scienceplots_toolkit import configure_matplotlib_style

configure_matplotlib_style(
    styles=["science", "ieee", "grid"],  # SciencePlots styles to use
    grid_linewidth=3,                     # Grid line width in points
    lines_linewidth=4,                    # Plot line width in points
    fontsize=26,                          # Base font size
    figsize=(16, 10),                     # Default figure size (inches)
    font="serif",                         # Font family
    sans_serif_math=False,                # Use sans-serif for math
    cmap_name="seaborn:tab10_new",       # Qualitative colormap
    use_latex=False,                      # Enable LaTeX rendering
    grid=True,                            # Enable axis gridlines
    legend_framealpha=1.0,                # Legend background transparency
    legend_shadow=True,                   # Legend shadow effect
)
```

### Utilities

```python
from scienceplots_toolkit.utils import (
    save_plot,              # Save figure to PNG and PDF
    configure_24h_axis,     # Set up 0-24h x-axis with 4h ticks
    add_stats_box,          # Add average/peak annotation box
)

# Save a figure
save_plot(fig, "my_plot", dpi=300)

# Configure 24-hour axis
configure_24h_axis(ax)

# Add statistics box
add_stats_box(ax, avg=5.2, peak=12.3, unit=r"\text{kW}")
```

### Analysis Tools

```python
from scienceplots_toolkit import (
    plot_profile_with_quantiles,  # Plot mean with shaded quantiles
    generate_profile_grid,        # Create multi-panel grid of plots
)

# Plot with uncertainty shading
plot_profile_with_quantiles(
    ax, x, mean, q10, q90,
    label="Load Profile",
    color="C0"
)

# Create a 2x2 grid of subplots
fig, axes = generate_profile_grid(n_rows=2, n_cols=2)
```

## LaTeX Support

The package supports two modes:

1. **Mathtext (default)**: Uses Matplotlib's built-in math renderer. No external dependencies.
2. **LaTeX**: Uses system LaTeX for professional typesetting. Requires:
   - TeX Live or MiKTeX installation
   - Packages: `amsmath`, `amssymb`, `amsfonts`, `textcomp`, `gensymb`, `siunitx`, `graphicx`

Enable LaTeX mode:

```python
configure_matplotlib_style(use_latex=True)
```

Or via CLI:

```bash
uv run examples/example_basic.py --latex
```

## Project Structure

```text
scienceplots-toolkit/
├── src/scienceplots_toolkit/
│   ├── __init__.py          # Public API exports
│   ├── style.py             # Matplotlib style configuration
│   ├── utils.py             # Utility functions
│   └── analysis.py          # Analysis and visualization tools
├── examples/
│   ├── example_basic.py     # Basic plotting examples
│   └── example_energy.py    # Energy profile examples
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
## Development

### Setup

```bash
uv sync --group dev
```

### Run Tests

```bash
uv run pytest tests/ -v
```

### Linting and Formatting

```bash
uv run ruff format .
uv run ruff check .
uv run ty check .
```

## Acknowledgments

This package builds upon the excellent [SciencePlots](https://github.com/garrettj403/SciencePlots) library by John Garrett, which is also licensed under the MIT License.

SciencePlots provides Matplotlib styles for publication-quality plots. For more information, see: <https://github.com/garrettj403/SciencePlots>

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

Jakob Buchmeier - <jakob.buchmeier@tuwien.ac.at>

Project Link: <https://github.com/jakobbuch/scienceplots-toolkit>
