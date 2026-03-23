---
description: "Git workflow, commit standards, and changelog management."
applyTo: "*"
---

# Workflow Standards

Follow these rules for all contributions and repository management.

## Git & Commits

- **Conventional Commits**: Use the Conventional Commits format for all
  messages: `<type>(<scope>): <description>`.
  - `feat`: New feature or capability.
  - `fix`: Bug fix.
  - `docs`: Documentation changes.
  - `refactor`: Code change that neither fixes a bug nor adds a feature.
  - `chore`: Maintenance tasks, dependencies, etc.
- **Atomic Commits**: Keep changes focused and atomic.

## Changelog Management

- **Mandatory Updates**: For every `feat`, `fix`, or significant `refactor`,
  you MUST update `CHANGELOG.md`.
- **Format**: Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
  structure.
- **Date**: Always include the current date in the `Unreleased` section or
  under the specific version header.
- **Placement**: Add new entries at the top of the relevant section (Added,
  Changed, Fixed, etc.).

## Verification

- Before finalising any task, run the project's verification suite:
  - `uv run ruff check .`
  - `uv run ruff format .`
  - `uv run ty check .`
