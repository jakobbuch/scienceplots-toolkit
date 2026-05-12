# Contributing to SciencePlots Toolkit

This guide covers everything you need to get started contributing to this repository, ensuring that both human and AI agent workflows remain high-quality and consistent.

## Core Philosophy

This project adheres to a set of guiding principles to ensure technical excellence and maintainability:

1. **Boring Technicals**: Use battle-tested, industry-standard tools and practices. Prefer `uv`, `ruff`, and `pytest` over custom scripts or experimental frameworks. Simplicity over cleverness.

2. **Small and Extensible Core**: Keep core logic focused and auditable. Complex or experimental features should be isolated or implemented as extensions.

3. **Simplicity is a Feature**: Every line of code is a maintenance burden. Prefer direct solutions, explicit code, and fewer dependencies.

4. **Data Portability**: Avoid vendor lock-in. Use standard, open formats and ensure data can be easily exported and migrated.

5. **Testing First**: No feature is complete without verification. Follow the [Testing Pyramid](tests/AGENTS.md) to ensure reliability at all levels.

## Prerequisites

**Required:**

- **Python** 3.12+ (managed by `uv`)
- **uv** (for package management and tool execution)
- **git** (for local hook installation)

**Optional:**

- **Nix** (for devenv-based development environments)
- **LaTeX** (for testing LaTeX rendering in plots)

## Getting Started

```bash
git clone https://github.com/jakobbuch/scienceplots-toolkit.git
cd scienceplots-toolkit
uv sync
```

## Development Workflow

1. **Fork** the repository and create a feature branch
   - Use `feat/`, `fix/`, `docs/`, or `ai/` prefixes
   - Example: `feat/add-new-plot-type`

2. **Make your changes** using the **Plan → Act → Validate (PAV)** cycle
   - See [PAV Cycle Guide](docs/PAV_CYCLE.md) for detailed instructions
   - Classify intent: Surgical vs Standard vs Complex

3. **Install local hooks** once: `uv run pre-commit install`

4. **Run the full check suite** before committing (see below)

5. **Open a Draft Pull Request** for review

## Check Suite

Before committing or submitting a PR, ensure all checks pass:

```bash
# Recommended: Run the standards validator first
uv run python tools/agent/validate_standards.py

# Quality Assurance
uv run ruff check --fix   # Lint and auto-fix
uv run ruff format        # Format
uv run ty check           # Type check (strict)
uv run pytest             # Run all tests
uv run pre-commit run --all-files  # Run local pre-commit hooks
```

### Pre-Commit Hooks

The following hooks run automatically on `git commit`:

- **markdownlint-rs**: Markdown linting (line-length rule MD013 disabled)
- **ruff-format**: Python code formatting
- **ruff**: Python linting with auto-fix
- **ty**: Type checking
- **shellcheck**: Shell script validation
- **pytest**: Run all tests
- **validate-standards**: Repository structure validation

**All hooks must pass** before the commit succeeds.

## Coding Standards

### Python

- **Authority**: All Python code must follow [`docs/PYTHON_STANDARDS.md`](docs/PYTHON_STANDARDS.md)
- **Type Hints**: Required for all functions
- **Docstrings**: Google-style for all public functions
- **Formatting**: Ruff format (88 char line length)
- **Linting**: Ruff with custom rule set

### Git

- **Authority**: All Git workflows follow [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md)
- **Atomic Commits**: Small, logical units of work
- **Commit Messages**: Conventional commits format
  ```
  type(scope): description

  [optional body]

  [optional footer]
  ```
- **AI Attribution**: Use trailers for AI-assisted work
  ```text
  Generated-by: AI-Agent
  Assisted-by: @username
  ```

### Documentation

- **Authority**: All documentation follows [`docs/AGENTS.md`](docs/AGENTS.md)
- **Structure**: Progressive disclosure (concept → capabilities → examples)
- **Examples**: Context → Code → Details
- **Formatting**: MkDocs admonitions for callouts

## Testing

### Test Organization

Tests follow the testing pyramid:

- **Unit Tests**: Fast, isolated, test individual functions
- **Integration Tests**: Test module interactions
- **Visual Tests**: Validate plot output with baseline comparison

See [`tests/AGENTS.md`](tests/AGENTS.md) for detailed testing standards.

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=scienceplots_toolkit --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_style.py -v

# Run visual tests only
uv run pytest tests/test_visual_baselines.py -v
```

### Adding New Tests

When adding new functionality:

1. Create test file if module doesn't have tests
2. Add test class for the new function/class
3. Write test methods for:
   - Normal case (expected behavior)
   - Edge cases (boundary conditions)
   - Error cases (invalid input)
4. Add visual baseline if function creates plots
5. Verify coverage with `pytest-cov`

## Contributor Resources

### Updating Documentation

- **Test examples**: All code examples must be tested and working
- **Link related docs**: Provide "See Also" sections
- **Update CHANGELOG**: Document structural changes
- **Follow templates**: Use `docs/templates/` for plans and specs

### Wiki-First Knowledge Capture

When new findings or architectural decisions are discovered:

1. Capture in `wiki/sessions/` or `wiki/decisions/`
2. Tag with `changelog: true` if structural change
3. Synthesis promotes to `docs/` and `CHANGELOG.md`

**Exception**: Trivial fixes (typos, grammar) can update docs directly.

See [`wiki/README.md`](wiki/README.md) for detailed workflow.

## Submitting Changes

### Pull Request Process

1. **Create Draft PR**: Mark as draft initially
2. **Link Issues**: Reference related issues in description
3. **Add Labels**: Apply appropriate labels (feat, fix, docs, etc.)
4. **Request Review**: Tag appropriate reviewers
5. **Address Feedback**: Make requested changes
6. **Mark Ready**: Remove draft status when ready
7. **Merge**: Squash and merge after approval

### PR Description Template

```markdown
## Summary

[Brief description of changes]

## Changes

- [Change 1]
- [Change 2]

## Testing

- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Visual baselines updated (if applicable)

## Related Issues

Fixes #123
Related to #456
```

## Code Review

### Reviewer Checklist

- [ ] Code follows Python standards
- [ ] Type hints are complete
- [ ] Docstrings are present and accurate
- [ ] Tests cover all code paths
- [ ] Documentation is updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No unintended side effects

### Review Guidelines

- **Be Constructive**: Provide specific, actionable feedback
- **Be Timely**: Review within 24-48 hours
- **Be Thorough**: Check all changed files
- **Be Kind**: Remember we're all learning

## Release Process

See [`RELEASE.md`](RELEASE.md) for detailed release process.

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Questions?

- **Documentation**: Check [`docs/`](docs/) directory
- **Issues**: Search existing issues or create new one
- **Discussions**: Use GitHub Discussions for questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
