---
name: Architecture
description: System architecture and design decisions for scienceplots-toolkit
---

# Architecture

This document describes the system architecture of the `scienceplots-toolkit` package.

## Overview

`scienceplots-toolkit` is a Python library that provides publication-quality Matplotlib plotting utilities with SciencePlots styles and LaTeX typesetting support.

## Package Structure

```
src/scienceplots_toolkit/
├── __init__.py    # Public API exports
├── style.py       # Matplotlib style configuration
├── utils.py       # Utility functions (save_plot, configure_24h_axis, add_stats_box)
├── analysis.py    # Analysis tools (plot_profile_with_quantiles, generate_profile_grid)
├── latex.py       # LaTeX preamble management
└── cli.py         # Command-line interface
```

## Core Components

### Style Configuration (`style.py`)

The `configure_matplotlib_style()` function is the entry point for setting up publication-quality styles:

- Applies SciencePlots styles (science, ieee, grid)
- Configures font sizes, line widths, and color cycles
- Supports both mathtext and LaTeX rendering modes
- Sets default figure size and DPI

### Utilities (`utils.py`)

Core utility functions for common plotting tasks:

- `save_plot()`: Save figures to PNG and PDF formats
- `configure_24h_axis()`: Set up 24-hour time axis for daily profiles
- `add_stats_box()`: Add statistical annotations (average, peak)

### Analysis Tools (`analysis.py`)

Higher-level visualization tools:

- `plot_profile_with_quantiles()`: Plot mean with shaded quantile regions
- `generate_profile_grid()`: Create multi-panel grids for comparison

### LaTeX Support (`latex.py`)

The `PreambleManager` class handles LaTeX preamble configuration for professional typesetting.

## Design Principles

1. **Simplicity**: Easy-to-use API with sensible defaults
2. **Flexibility**: Customizable parameters for advanced users
3. **Consistency**: Uniform styling across all plots
4. **Quality**: Publication-ready output with minimal effort

## Dependencies

- **Matplotlib**: Core plotting library
- **NumPy**: Numerical operations
- **SciencePlots**: Style templates
- **LaTeX** (optional): Professional typesetting

## Related Documentation

- **[AGENTS.md](../AGENTS.md)**: Agent mandates
- **[PYTHON_STANDARDS.md](PYTHON_STANDARDS.md)**: Python coding standards
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Development workflow
