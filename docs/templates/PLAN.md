---
name: "Plan: [Task Name]"
description: "[Brief description of the implementation strategy]"
---

# Plan: [Task Name]

## Intent Classification

Before creating a plan, classify your task:

- **Surgical**: No plan required (single file, no deps, obvious correctness)
  - Examples: typos, comments, logging, minor refactors
  - MUST verify with Reality Checker after completion

- **Standard**: Plan required (2-5 files, minor API changes)
  - Examples: new internal functions, test additions, feature enhancements
  - Create this plan document

- **Complex**: Spec + Plan required (6+ files, public API changes, architectural changes)
  - Examples: new modules, breaking changes, major refactors
  - Create SPEC.md first, then this plan

See `docs/INTENT_CLASSIFICATION.md` for full criteria.

---

## Overview

[Summary of the technical approach - 2-3 sentences describing what you're building and why.]

## Assumptions

**Purpose**: Document what you assume to be true about the system, environment, and constraints. These are beliefs you're not testing but must hold for your plan to succeed.

**Example**:

- Repository structure is stable; no major reorganization planned
- Python 3.12+ tooling (uv, ruff, ty) is correctly configured
- Existing test coverage is adequate for validation
- No breaking changes to core APIs expected

## Tradeoffs

**Purpose**: Surface design decisions explicitly. Every approach has costs; name them so future readers understand why you chose this path.

**Example**:

- **Scope**: Focused on [specific goal] only; excludes [out of scope items]
  - _Rationale_: Keeps work bounded and maintainable
- **Automation-first**: Relies on tool-based verification rather than manual review
  - _Rationale_: Ensures reproducible, objective compliance checks
- **Incremental updates**: Enhanced existing patterns rather than rewriting
  - _Rationale_: Preserves institutional knowledge while improving clarity

## Rule Compliance

[List relevant Rule IDs from AGENTS.md or PYTHON_STANDARDS.md that this plan addresses.]

- <!-- rule:XYZ -->: [Brief rationale]

---

## Sub-Task 1: [Module/Component Name]

**Goal**: [One sentence describing the goal of this sub-task.]

**Implementation Steps**:

1. [Step 1 - specific action]
2. [Step 2 - specific action]
3. [Step N - as needed]

**Acceptance Criteria**:

- [ ] [Specific, testable condition 1 - not just "run tool"]
- [ ] [Specific, testable condition 2 - what does success look like?]
- [ ] [Observable outcome that proves completion]

**Validation**:

- [ ] `uv run ty check` (zero type errors)
- [ ] `uv run ruff check` (zero lint errors)
- [ ] `uv run pytest tests/[test_file].py` (all tests pass)
- [ ] `uv run python tools/agent/validate_standards.py` (repository validated)

---

## Sub-Task 2: [Module/Component Name]

**Goal**: [One sentence describing the goal of this sub-task.]

**Implementation Steps**:

1. [Step 1 - specific action]
2. [Step 2 - specific action]

**Acceptance Criteria**:

- [ ] [Specific, testable condition 1]
- [ ] [Specific, testable condition 2]

**Validation**:

- [ ] `uv run ty check`
- [ ] `uv run ruff check`
- [ ] `uv run pytest tests/[test_file].py`

---

[Add more sub-tasks as needed...]

---

## Final Verification (Reality Checker)

Before marking this plan complete, verify:

- [ ] All tests pass (100% coverage for new logic)
- [ ] Zero linting/type errors on changed files
- [ ] Repository standards validated
- [ ] No pre-existing issues introduced
- [ ] Documentation updated if needed

**Cleanup**: _Note to Agent: Keep `PLAN.md` as an active-plan pointer and update it when the active plan changes. Do not delete this template._

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial plan | [Agent/Human] |
| | | |
