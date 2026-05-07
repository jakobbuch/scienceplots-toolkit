# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-07

### Added

- **Initial release** of scienceplots-toolkit v0.1.0
- **Style configuration** - `configure_matplotlib_style()` with SciencePlots integration
- **Utility functions**:
  - `save_plot()` - Save figures to PNG and PDF with logging
  - `configure_24h_axis()` - Standard 24-hour time axis configuration
  - `add_stats_box()` - Statistical annotation boxes for average/peak values
- **Analysis tools**:
  - `plot_profile_with_quantiles()` - Plot mean with shaded 10%-90% quantiles
  - `generate_profile_grid()` - Multi-panel grid generation for comparative plots
- **Colormap utilities** - `qual_cmap()` for qualitative color schemes
- **Comprehensive test suite** - 36 unit tests covering all public functions
- **Example scripts** - Basic plots and energy profile examples with CLI interface
- **Documentation** - Complete README with API reference, installation guide, and examples
- **Development tooling** - Pre-commit hooks, ruff, ty, pytest configuration

### Changed

- **Logging** - Replaced `print()` statements with proper logging in `save_plot()`
- **API** - Added optional `output_dir` parameter to `save_plot()` function
- **Documentation** - Removed Docker references, simplified to user-managed environments

### Technical Details

- **Package structure** - Modern src/ layout with PEP 621 pyproject.toml
- **Type hints** - Complete type annotations across all modules
- **Docstrings** - NumPy-style documentation for all public functions
- **Testing** - pytest suite with 100% coverage of public API

---

## [Unreleased]

### Added (Historical)

- **Workflow Instructions**: Added mandatory instructions for AI agents to
  maintain `CHANGELOG.md` with each significant change, ensuring a transparent
  and up-to-date project history without additional tools.
- **AI Agent Workflow**: Introduced a tool-agnostic agent instruction set to
  ensure high-quality code and consistent scientific visualization across
  different AI assistants (Copilot, Claude, Gemini).
  - Refactored `AGENTS.md` into high-level mandates.
  - Created `.agents/instructions/` for specialized coding, plotting,
    documentation, and data handling standards.
  - Created `.agents/skills/` for high-level task workflows.
- **Project Infrastructure**: Added `devenv` configuration and integrated
  `pre-commit` hooks for automated linting and type checking.

### Changed (Historical)

- **Documentation**: Updated `README.md` with new project layout and AI agent
  workflow details.
- **Tooling**: Updated `ty` type checking command to use the `check`
  subcommand.

### Fixed (Historical)

- **Type Checking**: Resolved a `ty` warning in `MatplotlibStyle.py` by
  removing an unused `type: ignore` directive.

---
*Last Updated: 2026-05-07*
