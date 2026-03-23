# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **AI Agent Workflow**: Introduced a tool-agnostic agent instruction set to
  ensure high-quality code and consistent scientific visualization across
  different AI assistants (Copilot, Claude, Gemini).
  - Refactored `AGENTS.md` into high-level mandates.
  - Created `.agents/instructions/` for specialized coding, plotting,
    documentation, and data handling standards.
  - Created `.agents/skills/` for high-level task workflows.
- **Project Infrastructure**: Added `devenv` configuration and integrated
  `pre-commit` hooks for automated linting and type checking.

### Changed

- **Documentation**: Updated `README.md` with new project layout and AI agent
  workflow details.
- **Tooling**: Updated `ty` type checking command to use the `check`
  subcommand.

### Fixed

- **Type Checking**: Resolved a `ty` warning in `MatplotlibStyle.py` by
  removing an unused `type: ignore` directive.

---
*Last Updated: 2026-03-23*
