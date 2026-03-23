# Coding Guidelines

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

## Documentation

- Write docstrings and comments in British English (e.g., 'analyse' instead of
  'analyze')
- Write error messages and print output in English
- Use Google-style docstrings:

  ```python
  def example(param1: str, param2: int) -> bool:
      """Brief description of function.

      Args:
          param1: Description of param1.
          param2: Description of param2.

      Returns:
          Description of return value.
      """
  ```

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
- Markdown must pass `markdownlint` rules with strict adherence:
  - **Line length**: Maximum 80 characters (MD013). Wrap text to fit.
  - **Spacing**: Always surround headings, lists, and code blocks with blank
    lines (MD022, MD031, MD032).
  - **Lists**: Use consistent indentation.

## Project Standards

- **Plotting**:
  - **Style & API**:
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
    - **Time Series & Energy**:
      - Use `plotting_utils.configure_24h_axis(ax)` for all 24-hour profiles.
      - Use `plotting_utils.add_stats_box(ax, ...)` for Avg/Peak annotations.
      - Use `profile_analysis.plot_profile_with_quantiles` for uncertainty.
    - **Grid Usage**:
      - The grid is automatically configured by `configure_matplotlib_style`
        with the "grid" style.
      - To disable the grid pass the `grid=False` parameter to
      `configure_matplotlib_style`
      - Do NOT use `ax.grid()` to simply enable the full grid.
      - You MAY use `ax.xaxis.grid(False)` (or `ax.yaxis.grid(False)`) to
        customize which axes show grid lines (e.g., for bar charts or box plots
        where vertical grid lines are distracting).
    - **Do NOT overwrite style settings** (like font size, line width) manually
      in the plot code, unless necessary for a specific element. Overwriting
      `figsize` is allowed for large/complex figures.
  - **Saving**:
    - Use a helper function (like `save_plot(fig, filename_base)`) to save
      plots to the `output/` directory.
    - Ensure plots are saved in both `.png` and `.pdf` formats with `dpi=300`.
    - Always call `plt.close(fig)` after saving plots to release memory.
  - **Layout**:
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
    - **Scale Consistency & Visibility**:
      - When multiple plots depict the same quantity, ensure they use the same
        axis scale so the plots are directly comparable. Choose the scale so
        all data across the set fit within the axes.
      - Use `ax.set_xticks(range(0, 25, 4))` for 24-hour time axes.
      - Use `ax.text()` (stats boxes) for summary metrics (Avg/Peak) within
        subplots, using a consistent position (top-left).
- **LaTeX examples**:
  - Use the single example runner with `--latex` instead of the separate
    LaTeX example file: `uv run example.py -- --latex` or
    `python example.py --latex`.

## New Script Creation

- When creating a new script:
  - Add a brief description to `README.md`.
  - Ensure it follows the "Plotting" and "Path Handling" guidelines.

## Data Handling

- Do not implement custom CSV parsing for standard data files if a loader
  is available.
- If loading time series data, ensure consistent timezone handling (prefer
  UTC or a single local timezone throughout).
