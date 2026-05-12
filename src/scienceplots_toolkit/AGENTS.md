# AGENTS.md — Source Module (`src/scienceplots_toolkit/`)

This directory contains the core `scienceplots_toolkit` package. All implementation code lives here.

## Global Mandates

<!-- rule:S-001 -->

- **Inherit Root Mandates**: All instructions in the [Root AGENTS.md](../../AGENTS.md) apply here.

## Module Structure

```
src/scienceplots_toolkit/
├── __init__.py          # Public API exports (re-export from submodules)
├── style.py             # configure_matplotlib_style(), get_figsize()
├── utils.py             # save_plot(), configure_24h_axis(), add_stats_box()
├── analysis.py          # plot_profile_with_quantiles(), generate_profile_grid()
├── latex.py             # PreambleManager class
└── cli.py               # CLI orchestrator, @plot_function decorator
```

## Implementation Standards

<!-- rule:S-002 -->

- **Public API in `__init__.py`**: Re-export public functions from submodules
  - Users should `from scienceplots_toolkit import X` not `from scienceplots_toolkit.style import X`
  - Keep `__init__.py` minimal - only re-exports, no implementation

<!-- rule:S-003 -->

- **Type Hints Required**: All functions must have complete type annotations
  - Use modern syntax: `list[str]`, `tuple[float, ...]`, `dict[str, Any]`
  - Annotate all parameters and return types
  - Use `TYPE_CHECKING` for import-time type hints

<!-- rule:S-004 -->

- **Docstrings Required**: All public functions must have Google-style docstrings
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """One-line summary.

      Extended description if needed.

      Args:
          param1: Description of param1
          param2: Description of param2

      Returns:
          Description of return value

      Example:
          >>> function_name("value", 42)
          True
      """
  ```

<!-- rule:S-005 -->

- **Lazy Imports for Heavy Dependencies**: Use lazy imports for matplotlib, numpy, etc.
  - Prevents import errors when optional dependencies not installed
  - Import inside functions that need them
  - Use `TYPE_CHECKING` for type hints

## Module-Specific Guidelines

### `style.py` - Style Configuration

- **Single Entry Point**: `configure_matplotlib_style()` is the main function
- **Reset Before Configure**: Always call `plt.rcdefaults()` before applying styles
- **LaTeX Preamble**: Use `PreambleManager` from `latex.py` for LaTeX configuration
- **Color Cycle**: Override matplotlib's default color cycle with `cmap` library

### `utils.py` - Utility Functions

- **Path Handling**: Always use `pathlib.Path`, never `os.path` or string concatenation
- **Output Directory**: Default to `output/` relative to script location
- **Both Formats**: `save_plot()` must save both PNG and PDF
- **24h Standard**: `configure_24h_axis()` sets 0-24 range with 4h ticks

### `analysis.py` - Analysis Tools

- **Dataclass for Stats**: Use `DailyStats` dataclass for structured return values
- **Quantile Shading**: `plot_profile_with_quantiles()` uses `fill_between()` with alpha
- **Grid Generation**: `generate_profile_grid()` handles subplot sharing modes

### `latex.py` - LaTeX Management

- **Builder Pattern**: `PreambleManager` uses fluent interface for package management
- **Default Packages**: Include amsmath, amssymb, amsfonts, textcomp, gensymb, siunitx
- **Sans-Serif Math**: Support `sansmath` package for sans-serif math mode

### `cli.py` - CLI Orchestrator

- **Decorator Pattern**: `@plot_function` registers functions with metadata
- **Base Class**: `BaseOrchestrator` provides CLI argument parsing and orchestration
- **Subclass Required**: Users must implement `run_plots()` in subclasses

## Testing Requirements

<!-- rule:S-006 -->

- **Unit Tests**: Every public function must have corresponding unit tests
- **Visual Tests**: Plotting functions need visual baseline tests
- **Type Coverage**: All code must pass `ty check` with zero errors
- **Test Location**: Tests live in `tests/` directory, parallel structure

## Validation

Before committing changes to this directory:

```bash
# Type check
uv run ty check src/scienceplots_toolkit/

# Lint
uv run ruff check src/scienceplots_toolkit/

# Test
uv run pytest tests/test_*.py -v

# Validate standards
uv run python tools/agent/validate_standards.py
```

## Related Documentation

- **[Root AGENTS.md](../../AGENTS.md)**: Global mandates and workflows
- **[PYTHON_STANDARDS.md](../../docs/PYTHON_STANDARDS.md)**: Python coding standards
- **[API_DESIGN.md](../../docs/API_DESIGN.md)**: API design principles
- **[scienceplots-viz Skill](../../.agents/skills/scienceplots-viz/SKILL.md)**: Usage examples

## Gotchas

- **Don't Change Directory**: Never use `os.chdir()` - scripts must work from any directory
- **Don't Import Directly**: Always import from `scienceplots_toolkit`, not submodules
- **Don't Skip Validation**: All code must pass type checking, even if "obviously correct"
- **Don't Break Public API**: Public functions in `__init__.py` are stable - deprecate before removing
