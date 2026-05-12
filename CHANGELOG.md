# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-12

### Added

- **AI Agent Infrastructure** - Comprehensive tooling and documentation for AI-assisted development
  - `tools/agent/validate_standards.py` - Repository structure validator
  - `tools/agent/validate_skill.py` - SKILL.md structural validator with name collision checks
  - `tools/agent/eval_skill.py` - Skill quality evaluator (10 criteria, 70% threshold)
- **Agent Documentation** - Multi-level AGENTS.md files for standardized agent behavior
  - Root `AGENTS.md` with 8 core mandates (G-1 through G-8)
  - Module-specific guidance in `src/`, `tests/`, and `docs/` directories
  - `CONTRIBUTING.md` for human and agent contributors
- **Workflow Templates** - Standardized templates in `docs/templates/`
  - `PLAN.md` - Implementation plans with intent classification (Surgical/Standard/Complex)
  - `SPEC.md` - Feature specifications with acceptance criteria
  - `SKILL.md` - Agent skill documentation (2 layouts: tool-focused and role-focused)
- **Coordination Documentation** - Multi-agent coordination protocols
  - `docs/coordination/QUICKSTART.md` - Quick start guide for multi-agent workflows
  - `docs/coordination/ARTIFACTS.md` - Coordination artifact structure
  - `docs/PAV_CYCLE.md` - Plan → Act → Validate workflow documentation
- **Knowledge Base** - Wiki-first documentation structure
  - `wiki/README.md` - Knowledge capture workflow
  - `wiki/sessions/`, `wiki/decisions/`, `wiki/research/` directories
- **Testing Infrastructure**
  - `tests/conftest.py` - 10 shared pytest fixtures with autouse figure cleanup
  - Visual baseline tests with pytest-mpl
  - Coverage enforcement (90% threshold)
- **Technical Documentation**
  - `docs/ARCHITECTURE.md` - System architecture and design decisions
  - `docs/PYTHON_STANDARDS.md` - Python coding standards and best practices
  - `llms.txt` - High-signal index for AI agents
  - `.aiignore` - AI agent session exclusion patterns
- **Pre-commit Enhancements**
  - `validate-standards` hook for repository compliance
  - Markdown linting with markdownlint-rs
  - Type checking with ty
  - Visual regression tests with pytest-mpl

### Changed

- **Version Management** - Switched to VCS-based versioning via hatch-vcs
- **Documentation Structure** - Reorganized into task-oriented guides with progressive disclosure
- **Agent Workflows** - Standardized on Plan → Act → Validate (PAV) cycle

### Technical Details

- **Total Lines Added**: ~5,000+ lines of agent infrastructure
- **New Files**: 24 files (tools, templates, documentation)
- **Test Coverage**: 53 passing tests (coverage temporarily at 53% due to untested CLI module)
- **Validation Tools**: 3 Python validators (960 lines combined)

---

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


*Last Updated: 2026-05-12*
*Last Updated: 2026-05-12*
