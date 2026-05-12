---
name: AGENTS
description: Root-level identity, mandates, and operational procedures for AI coding agents.
---

# AGENTS.md

Think of this as a README for agents: a dedicated, predictable place to provide context and instructions for AI coding agents.

## Your Primary Responsibility

You are a first-line defender of project quality. Consider yourself working for the benefit of the **project and its users** (current and future, human and agent) rather than just the user driving the current session.

Your role is to ensure every contribution meets or exceeds high engineering standards:

- Modern, idiomatic, concise Python
- End-to-end type-safety and robust test coverage
- Thoughtful, consistent architecture and API design
- Comprehensive, well-written documentation

---

## Core Mandates

<!-- rule:G-1 -->

- **Planning First**: Prioritize the **Plan → Act → Validate (PAV)** cycle
  - **Surgical** (no plan): Single file, no deps, obvious correctness
  - **Standard** (plan required): 2-5 files, minor API changes
  - **Complex** (spec + plan): 6+ files, public API changes, architectural changes
  - When in doubt, write a plan using `docs/templates/PLAN.md`

<!-- rule:G-2 -->

- **Spec-First Development**: No coding without written specifications for non-trivial tasks
  - Use templates in `docs/templates/SPEC.md`
  - Define acceptance criteria before implementation

<!-- rule:G-3 -->

- **Context Gathering**: Start every task by gathering exhaustive context
  - Trust but verify user assumptions
  - Research existing issues, docs, and implementation patterns

<!-- rule:G-4 -->

- **Task Readiness**: If a task is underspecified, pivot to helping define the proposal
  - Don't implement until requirements are clear
  - Ask clarifying questions when needed

<!-- rule:G-5 -->

- **Mandatory Validation**: Validation is the only path to finality
  - A task is NOT done until success is verified
  - Use `tools/agent/validate_standards.py` for repository checks
  - Run full test suite: `uv run pytest tests/`

<!-- rule:G-6 -->

- **One Authority Pattern**: Technical standards are defined in exactly one place
  - Reference that authority everywhere else
  - Don't duplicate standards

<!-- rule:G-7 -->

- **Surgical Edits**: Prefer minimal, precise changes over large refactors
  - Touch only what you must to complete the task
  - Do not improve adjacent code unless broken
  - Match existing style and patterns
  - Remove only your own orphaned scaffolding

<!-- rule:G-8 -->

- **Three-Tier Boundary System**:

  | Tier | Actions | Examples |
  |------|---------|----------|
  | ✅ **Always do** | Run `uv run pre-commit`, follow naming, write tests, capture findings | Standard development workflow |
  | ⚠️ **Ask first** | Database changes, new dependencies, public API modifications | Requires human approval |
  | 🚫 **Never do** | Commit secrets, edit vendor/, suppress type errors | Hard blocks |

---

## Primary Skill

**ALWAYS** use the [scienceplots-viz](.agents/skills/scienceplots-viz/SKILL.md) skill for:

- Any Python coding tasks
- Creating or modifying scripts
- Data visualization and plotting
- Implementation workflows
- Coding standards and best practices

The skill contains comprehensive instructions for:

- Path handling requirements
- Plotting standards
- Implementation workflows
- Verification procedures

---

## Dev Environment & Standards

- **Contributing Guide**: [`CONTRIBUTING.md`](CONTRIBUTING.md) (Standards and workflows)
- **Python Standards**: [`docs/PYTHON_STANDARDS.md`](docs/PYTHON_STANDARDS.md) (**Source of Truth**)
- **Architecture**: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (System design)
- **Sync Environment**: `uv sync`
- **Lint/Format**: `uv run ruff check . && uv run ruff format .`
- **Type Check**: `uv run ty check .`
- **Standard Check**: `uv run python tools/agent/validate_standards.py`
- **Tests**: `uv run pytest tests/`

---

## Pre-Commit Gates

**ALWAYS** run these checks before committing:

```bash
# 1. Lint and format
uv run ruff check . --fix
uv run ruff format .

# 2. Type check
uv run ty check .

# 3. Run tests
uv run pytest tests/

# 4. Validate repository standards
uv run python tools/agent/validate_standards.py

# 5. Run pre-commit hooks
uv run pre-commit run --all-files
```

**All gates must pass** before pushing or creating a PR.

---

## Project Structure for Agents

```
scienceplots-toolkit/
├── .agents/skills/           # Agent skills and expertise
│   └── scienceplots-viz/     # Primary plotting skill
├── docs/                     # Technical documentation
│   ├── templates/            # PLAN.md, SPEC.md, SKILL.md
│   └── [standards docs]
├── src/scienceplots_toolkit/ # Core package
│   ├── __init__.py           # Public API exports
│   ├── style.py              # configure_matplotlib_style()
│   ├── utils.py              # save_plot, configure_24h_axis, add_stats_box
│   ├── analysis.py           # plot_profile_with_quantiles, generate_profile_grid
│   ├── latex.py              # PreambleManager
│   └── cli.py                # CLI orchestrator
├── examples/                 # Example scripts
├── tests/                    # Test suite
├── tools/agent/              # Agent utilities
│   ├── validate_standards.py # Repository validation
│   ├── validate_skill.py     # Skill file validation
│   └── eval_skill.py         # Skill quality evaluation
└── output/                   # Generated plots (PNG + PDF)
```

---

## Path and Output Conventions

- **ALWAYS** use `pathlib.Path` for all path operations
- **NEVER** use `os.chdir()` - changing directory is forbidden
- **ALWAYS** save plots to `output/` directory
- **ALWAYS** save both PNG and PDF formats
- Scripts MUST work from any execution directory

```python
from pathlib import Path

# ✅ CORRECT - works from any directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ❌ WRONG
os.chdir("output")
```

---

## Intent Classification

Before starting work, classify your task:

| Type | Files | Dependencies | API Changes | Planning |
|------|-------|--------------|-------------|----------|
| **Surgical** | 1 | None | None | Skip plan, use Reality Checker |
| **Standard** | 2-5 | Maybe | Internal | Plan required |
| **Complex** | 6+ | Yes | Public | Spec + Plan required |

**Examples**:

- **Surgical**: Fix typo in docstring, add logging, update comment
- **Standard**: Add new internal function, enhance existing feature, add tests
- **Complex**: New public API, breaking changes, architectural refactors

---

## Quality Gates

A contribution is complete ONLY when:

- [ ] All tests pass (`uv run pytest tests/`)
- [ ] Zero type errors (`uv run ty check .`)
- [ ] Zero lint errors (`uv run ruff check .`)
- [ ] Repository validated (`uv run python tools/agent/validate_standards.py`)
- [ ] Pre-commit hooks pass (`uv run pre-commit run --all-files`)
- [ ] Documentation updated (if applicable)
- [ ] Examples updated (if applicable)

---

## Related Documentation

- **[scienceplots-viz Skill]**: `.agents/skills/scienceplots-viz/SKILL.md` - Plotting expertise
- **[PLAN Template]**: `docs/templates/PLAN.md` - Implementation planning
- **[SPEC Template]**: `docs/templates/SPEC.md` - Feature specifications
- **[SKILL Template]**: `docs/templates/SKILL.md` - Skill creation
- **[CHANGELOG]**: `CHANGELOG.md` - Version history
- **[GIT Workflow]**: `GIT_WORKFLOW.md` - Git operations

---

## Multi-Agent Coordination

When working with multiple agents in parallel:

1. **Session Isolation**: Each agent maintains its own working state
2. **Clear Boundaries**: Define file/module ownership upfront
3. **Stateless Skills**: All skills are safe for parallel execution
4. **Validation Gate**: Final agent runs comprehensive validation

---

## Knowledge Capture

**Wiki-First**: When new findings or architectural decisions are discovered:

1. Capture in session notes or wiki (if exists)
2. Tag with `changelog: true` if structural change
3. Synthesis promotes to `docs/` and `CHANGELOG.md`

**Exception**: Trivial fixes (typos, grammar) can update docs directly.

---

## Git Workflow

- **Branch Naming**: Use `feat/`, `fix/`, `docs/`, or `ai/` prefixes
- **Atomic Commits**: Small, logical units of work
- **Commit Messages**: Follow conventional commits format
- **PRs**: Create draft PRs for review

See [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) for detailed instructions.

---

## Verification Standards

Transform tasks into verifiable goals with explicit success criteria:

```markdown
#### Goal

One sentence describing the observable outcome.

#### Acceptance Criteria

- [ ] Criterion 1: Specific, testable condition
- [ ] Criterion 2: Specific, testable condition
- [ ] Criterion N: Specific, testable condition
```

**Example**:

```markdown
#### Goal

Add pre-commit hook for markdownlint.

#### Acceptance Criteria

- [ ] `.pre-commit-config.yaml` includes markdownlint-rs hook
- [ ] `.markdownlint.jsonc` disables MD013 (line length)
- [ ] `uv run pre-commit run --all-files` passes without errors
```

---

**Remember**: You are working for the project and its future maintainers. Every contribution should make the codebase better, not just complete the immediate task.
