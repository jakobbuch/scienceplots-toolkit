# Skill: SciencePlots Visualization (`scienceplots-viz`)

## Domain: Data Visualization & Python Implementation

This skill provides a standardized workflow for implementing new visualization
scripts within the SciencePlots repository, ensuring compliance with strict
project guidelines for scientific plotting.

## Implementation Workflow

### 1. Preparation & Scope

- **Reference Utils**: Check `plotting_utils.py` and `profile_analysis.py` for
  existing functions before implementing custom logic.
- **Style Setup**: Always start by configuring the Matplotlib style.

### 2. Implementation Standards

- **Path Handling**: Use `pathlib.Path` exclusively.
- **Python Style**: Use f-strings, modern type hints, and British English.
- **Plotting API**: Use the Object-Oriented API (`fig, ax = plt.subplots()`).

### 3. Plotting Guidelines

- **Style**: Start with `configure_matplotlib_style` from `MatplotlibStyle`.
- **LaTeX**: Use raw strings (r"$\sin(x)$") for labels.
- **Energy Plots**: Use `configure_24h_axis` and `add_stats_box` for daily
  profiles.
- **Uncertainty**: Use `plot_profile_with_quantiles` for shading.
- **Saving**: Use `save_plot(fig, filename)` and `plt.close(fig)`.

### 4. Verification

- **Linting**: Run `uv run ruff check .` and `uv run ruff format .`.
- **Type Checking**: Run `uv run ty .`.
- **Markdown**: Ensure `README.md` is updated with the new script.

## Quality Criteria

- [ ] Paths use `pathlib.Path`.
- [ ] British English spelling used in docstrings.
- [ ] Matplotlib Object-Oriented API used.
- [ ] `configure_matplotlib_style` called at start.
- [ ] `constrained_layout` is active (default).
- [ ] Plots saved in both .png and .pdf.
