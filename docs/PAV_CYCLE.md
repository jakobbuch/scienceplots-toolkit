# Plan → Act → Validate (PAV) Cycle

Step-by-step example of the PAV cycle in action.

## Overview

The PAV cycle is the fundamental workflow for all non-trivial tasks:

```
┌─────────────┐
│    PLAN     │ ← Understand, research, design
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     ACT     │ ← Implement, test, document
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATE   │ ← Verify, measure, prove
└──────┬──────┘
       │
       ▼
   [Complete]
```

---

## Phase 1: PLAN

**Goal**: Understand the problem, gather context, design solution.

### Step 1.1: Intent Classification

Classify the task to determine planning requirements:

```markdown
#### Intent: Standard (Plan Required)

- **Files**: 2-5 files changed
- **Dependencies**: May add new dependency
- **API**: Internal function changes only
- **Tests**: Will add/modify tests

**Decision**: Create plan document, no spec needed
```

**Classification Guide**:

| Type | Files | Dependencies | API | Planning |
|------|-------|--------------|-----|----------|
| **Surgical** | 1 | None | None | Skip plan, use Reality Checker |
| **Standard** | 2-5 | Maybe | Internal | Plan required |
| **Complex** | 6+ | Yes | Public | Spec + Plan required |

### Step 1.2: Context Gathering

Research existing code, patterns, and constraints:

```bash
# Search for existing patterns
grep -r "configure_matplotlib_style" src/
grep -r "save_plot" examples/

# Read relevant documentation
cat docs/PYTHON_STANDARDS.md
cat .agents/skills/scienceplots-viz/SKILL.md

# Check existing tests
ls tests/test_*.py
```

**Document Findings**:

```markdown
## Context

**Existing Patterns**:
- Style configuration in `src/style.py`
- Utility functions in `src/utils.py`
- Tests follow class-per-module pattern

**Constraints**:
- Must use pathlib.Path (rule:S-0704)
- Must save both PNG and PDF
- Must work from any directory
```

### Step 1.3: Design Solution

Create implementation plan:

```markdown
## Plan: Add Monthly Profile Plot

### Overview

Add `create_monthly_profile()` function to generate 4×3 grid of monthly load profiles.

### Assumptions

- Repository structure stable
- Existing test infrastructure adequate
- No breaking changes to public API

### Tradeoffs

- **Scope**: Focused on monthly grids only
  - *Rationale*: Keeps work bounded
- **Implementation**: Use existing `generate_profile_grid()`
  - *Rationale*: Reuse tested code

### Sub-Tasks

#### Task 1: Add `create_monthly_profile()` to `src/analysis.py`

**Goal**: Create function that generates monthly profile grid

**Steps**:
1. Add function signature with type hints
2. Create 4×3 grid using `generate_profile_grid()`
3. Plot data for each month
4. Add month labels
5. Save both PNG and PDF

**Acceptance Criteria**:
- [ ] Function has complete type hints
- [ ] Function has Google-style docstring
- [ ] Grid has 4 rows × 3 columns
- [ ] Each subplot shows one month
- [ ] Month labels are Jan, Feb, Mar, ..., Dec
- [ ] Output saved to `output/monthly_profile.png` and `.pdf`

**Validation**:
- [ ] `uv run ty check src/analysis.py`
- [ ] `uv run ruff check src/analysis.py`
- [ ] `uv run pytest tests/test_analysis.py::TestCreateMonthlyProfile -v`

#### Task 2: Add Tests to `tests/test_analysis.py`

**Goal**: Test new function thoroughly

**Steps**:
1. Add `TestCreateMonthlyProfile` class
2. Test normal case (valid data)
3. Test edge cases (empty data, invalid months)
4. Test output file creation

**Acceptance Criteria**:
- [ ] Test class follows naming convention
- [ ] Test normal case with sample data
- [ ] Test edge cases (empty, invalid)
- [ ] Test output files created
- [ ] 100% code coverage for new function

**Validation**:
- [ ] `uv run pytest tests/test_analysis.py -v`
- [ ] `uv run pytest --cov=scienceplots_toolkit --cov-report=term-missing`

#### Task 3: Update Documentation

**Goal**: Document new function

**Steps**:
1. Add docstring example
2. Update README.md if public API
3. Add to CHANGELOG.md

**Acceptance Criteria**:
- [ ] Docstring has working example
- [ ] README.md updated (if applicable)
- [ ] CHANGELOG.md entry added

### Final Verification

- [ ] All tests pass
- [ ] Zero type errors
- [ ] Zero lint errors
- [ ] Repository standards validated
```

### Step 1.4: Create Plan Document

Save plan to standard location:

```bash
# Opencode (default)
.sisyphus/ses_[id]/plans/T-[uuid]-monthly-profile.md

# Or use docs/templates/PLAN.md as base
cp docs/templates/PLAN.md .sisyphus/ses_[id]/plans/T-monthly-profile.md
```

---

## Phase 2: ACT

**Goal**: Implement the solution according to plan.

### Step 2.1: Setup

Prepare your environment:

```bash
# Ensure environment is synced
uv sync

# Install pre-commit hooks (if not already)
uv run pre-commit install

# Open plan document
cat .sisyphus/ses_[id]/plans/T-monthly-profile.md
```

### Step 2.2: Implement Task 1

Add `create_monthly_profile()` to `src/analysis.py`:

```python
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

def create_monthly_profile(
    data: dict[str, np.ndarray],
    output_dir: Path = Path("output"),
) -> tuple["Figure", list["Axes"]]:
    """Create a 4×3 grid of monthly load profiles.
    
    Args:
        data: Dictionary mapping month names to load data arrays
        output_dir: Directory to save output files
        
    Returns:
        Tuple of (figure, axes_list)
        
    Example:
        >>> data = {
        ...     "Jan": np.random.randn(24),
        ...     "Feb": np.random.randn(24),
        ...     # ... more months
        ... }
        >>> fig, axes = create_monthly_profile(data)
    """
    from .utils import generate_profile_grid, save_plot
    
    # Validate input
    if len(data) != 12:
        msg = f"Expected 12 months, got {len(data)}"
        raise ValueError(msg)
    
    # Create 4×3 grid
    fig, axes = generate_profile_grid(n_rows=4, n_cols=3, figsize=(16, 12))
    
    # Month order
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Plot each month
    for ax, month in zip(axes, months, strict=True):
        if month in data:
            ax.plot(data[month])
            ax.set_title(month)
    
    # Save output
    save_plot(fig, output_dir / "monthly_profile", dpi=300)
    
    return fig, axes
```

### Step 2.3: Implement Task 2

Add tests to `tests/test_analysis.py`:

```python
import pytest
import numpy as np
from pathlib import Path
from scienceplots_toolkit.analysis import create_monthly_profile

class TestCreateMonthlyProfile:
    """Tests for create_monthly_profile() function."""
    
    def test_create_monthly_profile_valid_data(self, tmp_path):
        """Test with valid 12-month data."""
        # Arrange
        data = {
            month: np.random.randn(24)
            for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        }
        
        # Act
        fig, axes = create_monthly_profile(data, output_dir=tmp_path)
        
        # Assert
        assert fig is not None
        assert len(axes) == 12
        assert (tmp_path / "monthly_profile.png").exists()
        assert (tmp_path / "monthly_profile.pdf").exists()
    
    def test_create_monthly_profile_invalid_count(self, tmp_path):
        """Test with invalid number of months."""
        # Arrange
        data = {"Jan": np.random.randn(24)}  # Only 1 month
        
        # Act & Assert
        with pytest.raises(ValueError, match="Expected 12 months"):
            create_monthly_profile(data, output_dir=tmp_path)
    
    def test_create_monthly_profile_empty_data(self, tmp_path):
        """Test with empty data dictionary."""
        # Arrange
        data = {}
        
        # Act & Assert
        with pytest.raises(ValueError, match="Expected 12 months"):
            create_monthly_profile(data, output_dir=tmp_path)
```

### Step 2.4: Implement Task 3

Update documentation:

```markdown
<!-- CHANGELOG.md -->

## [Unreleased]

### Added

- `create_monthly_profile()` function for 4×3 monthly grid plots
```

### Step 2.5: Run Local Validation

Validate your work before marking complete:

```bash
# Type check
uv run ty check src/analysis.py

# Lint
uv run ruff check src/analysis.py

# Test
uv run pytest tests/test_analysis.py::TestCreateMonthlyProfile -v

# Coverage
uv run pytest tests/test_analysis.py --cov=scienceplots_toolkit.analysis --cov-report=term-missing
```

---

## Phase 3: VALIDATE

**Goal**: Prove the implementation is correct and complete.

### Step 3.1: Verify Acceptance Criteria

Go through each acceptance criteria:

```markdown
## Task 1 Acceptance Criteria

- [x] Function has complete type hints
  - Evidence: `def create_monthly_profile(data: dict[str, np.ndarray], ...) -> tuple[Figure, list[Axes]]:`
- [x] Function has Google-style docstring
  - Evidence: Docstring with Args, Returns, Example sections
- [x] Grid has 4 rows × 3 columns
  - Evidence: `generate_profile_grid(n_rows=4, n_cols=3)`
- [x] Each subplot shows one month
  - Evidence: Loop over months, `ax.plot(data[month])`
- [x] Month labels are Jan, Feb, ..., Dec
  - Evidence: `months = ["Jan", "Feb", ...]`
- [x] Output saved to PNG and PDF
  - Evidence: `save_plot(fig, output_dir / "monthly_profile", dpi=300)`

## Task 2 Acceptance Criteria

- [x] Test class follows naming convention
  - Evidence: `class TestCreateMonthlyProfile:`
- [x] Test normal case with sample data
  - Evidence: `test_create_monthly_profile_valid_data()`
- [x] Test edge cases (empty, invalid)
  - Evidence: `test_create_monthly_profile_invalid_count()`, `test_create_monthly_profile_empty_data()`
- [x] Test output files created
  - Evidence: `assert (tmp_path / "monthly_profile.png").exists()`
- [x] 100% code coverage for new function
  - Evidence: `pytest --cov` shows 100%

## Task 3 Acceptance Criteria

- [x] Docstring has working example
  - Evidence: Example section in docstring
- [x] CHANGELOG.md entry added
  - Evidence: Entry in CHANGELOG.md
```

### Step 3.2: Run Full Validation Suite

Run comprehensive validation:

```bash
# Full test suite
uv run pytest tests/ -v

# Type check entire project
uv run ty check .

# Lint entire project
uv run ruff check . --fix

# Repository standards
uv run python tools/agent/validate_standards.py

# Pre-commit hooks
uv run pre-commit run --all-files
```

### Step 3.3: Document Evidence

Create validation report:

```markdown
## Validation Results

### Tests

```bash
$ uv run pytest tests/ -v
============================= test session starts ==============================
collected 15 items
tests/test_analysis.py::TestCreateMonthlyProfile::test_valid_data PASSED
tests/test_analysis.py::TestCreateMonthlyProfile::test_invalid_count PASSED
tests/test_analysis.py::TestCreateMonthlyProfile::test_empty_data PASSED
============================== 3 passed in 2.34s ===============================
```

### Type Check

```bash
$ uv run ty check .
✅ All checks passed!
```

### Lint

```bash
$ uv run ruff check .
All checks passed!
```

### Standards Validation

```bash
$ uv run python tools/agent/validate_standards.py
✅ Repository standards validation successful!
```

### Pre-Commit

```bash
$ uv run pre-commit run --all-files
markdownlint-rs (check only).........................Passed
ruff (lint+fix)......................................Passed
ruff format..........................................Passed
ty type check........................................Passed
validate-standards...................................Passed
pytest...............................................Passed
```

**Conclusion**: All validation gates passed. Implementation is complete.
```

### Step 3.4: Update Plan Status

Mark plan as complete:

```markdown
<!-- Update plan document -->

## Status: COMPLETED ✅

**Completed At**: 2026-05-12 14:30
**Total Time**: 4 hours
**Validation**: All gates passed

### Reality Checker

- [x] All tests pass (3/3)
- [x] Zero type errors
- [x] Zero lint errors
- [x] Repository standards validated
- [x] No pre-existing issues introduced
```

### Step 3.5: Capture Learnings

Write session note:

```markdown
---
date: 2026-05-12
task: "Add monthly profile function"
agent: "Sisyphus"
changelog: true
---

# Session: Monthly Profile Implementation

## Summary

Added `create_monthly_profile()` function for generating 4×3 monthly load profile grids.

## Findings

- `generate_profile_grid()` works perfectly for this use case
- Month validation important (must be exactly 12)
- Output files saved to configurable directory

## Decisions

- Use strict mode for zip (prevents silent errors)
- Validate input data count upfront
- Return figure and axes for further customization

## Code Quality

- 100% test coverage
- Zero type errors
- Zero lint errors
- Follows all project standards

## Changelog Entry

Added `create_monthly_profile()` function.
```

---

## Reality Checker (For Surgical Tasks)

For surgical tasks (single file, no deps, obvious), skip the full plan but use Reality Checker:

```markdown
## Reality Checker

**Task**: Fix typo in docstring

- [x] Change is minimal (1 line)
- [x] No dependencies affected
- [x] No API changes
- [x] Obvious correctness (typo fix)
- [x] Verified with `uv run ruff check .`
- [x] No tests needed (no behavior change)

**Status**: COMPLETE ✅
```

---

## Templates

### Plan Template

Use `docs/templates/PLAN.md` as base.

### Session Note Template

```markdown
---
date: YYYY-MM-DD
task: "Task description"
agent: "Agent name"
changelog: true|false
---

# Session: [Task Name]

## Summary

[Brief summary]

## Findings

- [Finding 1]
- [Finding 2]

## Decisions

- [Decision 1]
- [Decision 2]

## Validation

- [ ] Tests pass
- [ ] Type check passes
- [ ] Lint passes
- [ ] Standards validated
```

---

## Related Documentation

- **[PLAN Template](templates/PLAN.md)**: Plan document template
- **[SPEC Template](templates/SPEC.md)**: Specification template
- **[AGENTS.md](AGENTS.md)**: Root-level mandates
- **[INTENT_CLASSIFICATION.md](INTENT_CLASSIFICATION.md)**: Intent classification guide
