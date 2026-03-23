---
description: "Standards for data visualization, Matplotlib usage, and plot saving."
applyTo: "**/*.py"
---

# Plotting Standards

Follow these rules for all data visualization in this repository.

## Style & API

- Always import and use `configure_matplotlib_style` from `MatplotlibStyle`
  at the start.
- Use the **Object-Oriented API** (`fig, ax = plt.subplots()`) for all
  plots. Avoid `plt.plot()`.
- Use **raw strings** (`r"$\sin(x)$"`) for all text/labels containing
  LaTeX math.
- Use LaTeX math where applicable (e.g., for units, fractions, chemical formulas)
- Rely on the default color cycle set by `configure_matplotlib_style` for
  line plots.
- **Do NOT manually set `linewidth`** for normal plot lines. Rely on the
  default set by `configure_matplotlib_style`.
- **Do NOT overwrite style settings** (like font size, line width) manually
  in the plot code, unless necessary for a specific element. Overwriting
  `figsize` is allowed for large/complex figures.

## Grid Usage

- The grid is automatically configured by `configure_matplotlib_style`
  with the "grid" style.
- To disable the grid pass the `grid=False` parameter to
  `configure_matplotlib_style`
- Do NOT use `ax.grid()` to simply enable the full grid.
- You MAY use `ax.xaxis.grid(False)` (or `ax.yaxis.grid(False)`) to
  customize which axes show grid lines (e.g., for bar charts or box plots
  where vertical grid lines are distracting).

## Time Series & Energy

- Use `plotting_utils.configure_24h_axis(ax)` for all 24-hour profiles.
- Use `plotting_utils.add_stats_box(ax, ...)` for Avg/Peak annotations.
- Use `profile_analysis.plot_profile_with_quantiles` for uncertainty.
- Use `ax.set_xticks(range(0, 25, 4))` for 24-hour time axes.
- Use `ax.text()` (stats boxes) for summary metrics (Avg/Peak) within
  subplots, using a consistent position (top-left).

## Layout

- **Do NOT use `fig.tight_layout()`**. `figure.constrained_layout.use` is
  already enabled in `MatplotlibStyle.py`.
- **Legend Placement**:
  - For single-panel plots, leave legend placement to Matplotlib.
  - For multi-panel plots (e.g., 4x3, 2x4), use a **shared figure legend**
    centered at the top of the entire figure:
    `fig.legend(handles, labels, loc="upper center",`
    `bbox_to_anchor=(0.5, 1.08), ncol=len(labels))`
    or below the figure if it has a title:
    `fig.legend(handles, labels, loc="upper center",`
    `bbox_to_anchor=(0.5, -0.02), ncol=len(labels))`
  - For single-panel plots where a manual placement is needed, use the above
    coordinates or place it outside the axes:
    (`loc="lower center", bbox_to_anchor=(0.5, -0.1)`).

## Scale Consistency & Visibility

- When multiple plots depict the same quantity, ensure they use the same
  axis scale so the plots are directly comparable. Choose the scale so
  all data across the set fit within the axes.

## Saving

- Use a helper function (like `save_plot(fig, filename_base)`) to save
  plots to the `output/` directory.
- Ensure plots are saved in both `.png` and `.pdf` formats with `dpi=300`.
- Always call `plt.close(fig)` after saving plots to release memory.

## LaTeX examples

- Use the single example runner with `--latex` instead of the separate
  LaTeX example file: `uv run example.py -- --latex` or
  `python example.py --latex`.
