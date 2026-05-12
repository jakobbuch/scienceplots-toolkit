# Multi-Agent Coordination Quickstart

5-step protocol for parallel execution with multiple AI agents.

## Quick Start

### Step 1: Decompose Work

Break your task into independent units that can be worked on in parallel:

```markdown
Task: Refactor authentication module

Unit 1: Core logic (`src/auth/core.py`)
Unit 2: API layer (`src/auth/api.py`)
Unit 3: Tests (`tests/auth/`)
Unit 4: Documentation (`docs/auth.md`)
```

**Rules:**
- Each unit must be independently testable
- No overlapping file modifications
- Clear handoff points defined

### Step 2: Assign Agents

Assign each unit to a separate agent session:

```
Agent 1 (Sisyphus): Unit 1 - Core logic
Agent 2 (Cursor): Unit 2 - API layer
Agent 3 (Claude): Unit 3 - Tests
Agent 4 (Opencode): Unit 4 - Documentation
```

### Step 3: Set Boundaries

Define clear file ownership to prevent conflicts:

```markdown
## File Boundaries

- Agent 1: `src/auth/core.py`, `src/auth/models.py`
- Agent 2: `src/auth/routes.py`, `src/auth/schemas.py`
- Agent 3: `tests/auth/test_core.py`, `tests/auth/test_api.py`
- Agent 4: `docs/auth.md`, `CHANGELOG.md`

## Shared Files (Coordinate!)

- `src/auth/__init__.py` - Agent 1 writes, others review
- `pyproject.toml` - Agent 2 updates deps, Agent 1 reviews
```

### Step 4: Execute in Parallel

Each agent works independently following the PAV cycle:

```bash
# Each agent runs in their own session
Agent 1: Plan → Act → Validate (core logic)
Agent 2: Plan → Act → Validate (API layer)
Agent 3: Plan → Act → Validate (tests)
Agent 4: Plan → Act → Validate (docs)
```

**Coordination Artifacts:**

- Plans stored in `.sisyphus/ses_[id]/plans/`
- Session notes in `wiki/sessions/`
- Status tracked via file timestamps

### Step 5: Integrate & Validate

Final agent integrates all changes and runs comprehensive validation:

```bash
# Integration checklist
- [ ] All files merged without conflicts
- [ ] No duplicate imports or definitions
- [ ] Consistent style across modules

# Validation
uv run ruff check .
uv run ty check .
uv run pytest tests/ -v
uv run python tools/agent/validate_standards.py
uv run pre-commit run --all-files
```

---

## Coordination Patterns

### Pattern 1: Module-Based Decomposition

Best for large refactors:

```
Agent 1: Module A (src/module_a/)
Agent 2: Module B (src/module_b/)
Agent 3: Integration (src/__init__.py, tests/)
```

### Pattern 2: Layer-Based Decomposition

Best for full-stack features:

```
Agent 1: Backend logic (src/backend/)
Agent 2: API layer (src/api/)
Agent 3: Frontend (src/frontend/)
Agent 4: Tests (tests/)
```

### Pattern 3: Test-Driven Decomposition

Best for complex features:

```
Agent 1: Write tests first (tests/)
Agent 2: Implement core logic (src/core.py)
Agent 3: Implement API (src/api.py)
Agent 4: Documentation (docs/)
```

---

## Artifact Structure

### Plans

```
.sisyphus/ses_[id]/plans/
├── T-[uuid]-core-refactor.md
├── T-[uuid]-api-layer.md
└── T-[uuid]-tests.md
```

### Session Notes

```
wiki/sessions/
├── 2026-05-12-core-refactor.md
├── 2026-05-12-api-layer.md
└── 2026-05-12-tests.md
```

### Decisions

```
wiki/decisions/
└── ADR-001-auth-architecture.md
```

---

## Conflict Prevention

### File Locks (Optional)

For critical files, use simple lock files:

```bash
# Create lock
echo "Agent 1 working" > .locks/src_auth_core.py.lock

# Remove when done
rm .locks/src_auth_core.py.lock
```

### Communication Protocol

Use wiki entries for async communication:

```markdown
<!-- wiki/sessions/2026-05-12-handoff.md -->

## Handoff: Core → API

**From**: Agent 1
**To**: Agent 2

Core logic complete. API should expose:
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

Schema defined in `src/auth/schemas.py`
```

---

## Validation Gates

### Gate 1: Individual Agent Validation

Each agent validates their own work:

```bash
# Each agent runs before marking unit complete
uv run ruff check src/their_module/
uv run ty check src/their_module/
uv run pytest tests/their_module/ -v
```

### Gate 2: Integration Validation

Final agent validates merged work:

```bash
# Full repository validation
uv run ruff check .
uv run ty check .
uv run pytest tests/ -v
uv run python tools/agent/validate_standards.py
```

### Gate 3: Pre-Commit Validation

Final pre-commit hook check:

```bash
uv run pre-commit run --all-files
```

---

## Harness-Specific Coordination

### Opencode (Default)

```bash
# Session isolation
.sisyphus/ses_[id]/

# Plans
.sisyphus/ses_[id]/plans/T-[uuid].md

# Notes
.sisyphus/ses_[id]/notes/
```

### Cursor

```bash
# Session isolation
.cursor/ses_[id]/

# Plans
.cursor/ses_[id]/plans/
```

### Cline

```bash
# Session isolation
.cline/ses_[id]/

# Plans
.cline/ses_[id]/plans/
```

### Claude Code

```bash
# Session isolation
.claude/ses_[id]/

# Plans via CLAUDE.md context
```

---

## Example: Auth Refactor

### Scenario

Refactor authentication module with 3 parallel agents.

### Decomposition

```
Agent 1 (Opencode): Core Logic
- `src/auth/core.py`
- `src/auth/models.py`
- `src/auth/security.py`

Agent 2 (Cursor): API Layer
- `src/auth/routes.py`
- `src/auth/schemas.py`
- Update `pyproject.toml` deps

Agent 3 (Claude): Testing
- `tests/auth/test_core.py`
- `tests/auth/test_api.py`
- `tests/auth/test_security.py`
```

### Execution Timeline

```
T+0:00  - All agents start (parallel)
T+0:30  - Agent 1 completes core logic
T+0:45  - Agent 2 completes API layer
T+1:00  - Agent 3 completes tests
T+1:15  - Agent 1 integrates all changes
T+1:30  - Final validation complete
T+1:45  - PR created
```

### Coordination Artifacts

```
.sisyphus/ses_abc123/plans/T-core.md
.sisyphus/ses_def456/plans/T-api.md
.sisyphus/ses_ghi789/plans/T-tests.md

wiki/sessions/2026-05-12-auth-core.md
wiki/sessions/2026-05-12-auth-api.md
wiki/sessions/2026-05-12-auth-tests.md

wiki/decisions/ADR-001-auth-architecture.md
```

---

## Troubleshooting

### Conflict: Two Agents Edit Same File

**Solution:**
1. Pause one agent
2. Let first agent complete
3. Merge changes manually
4. Resume second agent with updated context

### Conflict: Circular Dependencies

**Solution:**
1. Define clear dependency order upfront
2. Agent 1 creates interfaces
3. Agent 2 implements against interfaces
4. Agent 1 fills in implementations

### Conflict: Inconsistent Style

**Solution:**
1. Run `ruff format .` on merged code
2. Add style guide to `docs/PYTHON_STANDARDS.md`
3. Agents reference standards before coding

---

## Related Documentation

- **[AGENTS.md](../AGENTS.md)**: Root-level mandates
- **[PAV_CYCLE.md](PAV_CYCLE.md)**: Plan → Act → Validate workflow
- **[ARTIFACTS.md](ARTIFACTS.md)**: Coordination artifact structure
- **[GIT_WORKFLOW.md](../GIT_WORKFLOW.md)**: Git operations for merged work
