# Coordination Artifacts

Harness-agnostic artifact structure for multi-agent coordination.

## Overview

Coordination artifacts are file-based structures that enable multiple AI agents to work in parallel without conflicts. They are designed to be:

- **Harness-Agnostic**: Work across Opencode, Cursor, Cline, Claude Code
- **Session-Isolated**: Each agent maintains their own namespace
- **Collision-Free**: Deterministic naming prevents conflicts
- **Verifiable**: Clear status tracking and handoff points

---

## Directory Structure

```
[project-root]/
├── .sisyphus/                    # Opencode sessions (default)
│   └── ses_[id]/
│       ├── plans/
│       │   └── T-[uuid]-[task].md
│       └── notes/
│           └── [date]-[slug].md
│
├── .cursor/                      # Cursor sessions
│   └── ses_[id]/
│       ├── plans/
│       └── sessions/
│
├── .cline/                       # Cline sessions
│   └── ses_[id]/
│       ├── plans/
│       └── sessions/
│
├── .claude/                      # Claude Code sessions
│   └── ses_[id]/
│       └── plans/
│
├── wiki/                         # Harness-agnostic knowledge
│   ├── sessions/                 # Session findings
│   ├── decisions/                # Architectural decisions
│   └── research/                 # Background research
│
└── docs/                         # Permanent documentation
    └── coordination/             # Coordination templates
```

---

## Artifact Types

### 1. Plans

**Purpose**: Document implementation strategy before coding

**Location**: `[harness-dir]/ses_[id]/plans/T-[uuid]-[task].md`

**Naming Convention**:
- `T-` prefix (Task)
- UUID (8 chars from task ID)
- Task slug (kebab-case)

**Examples**:
```
.sisyphus/ses_abc123/plans/T-8c6ab1b2-auth-refactor.md
.cursor/ses_def456/plans/T-78aa6c9d-api-layer.md
.cline/ses_ghi789/plans/T-ec10d7e8-tests.md
```

**Template**: Use `docs/templates/PLAN.md`

**Lifecycle**:
- Created: Before implementation starts
- Updated: When plan changes
- Archived: After task completion (move to `.sisyphus/archive/`)

---

### 2. Session Notes

**Purpose**: Capture findings, decisions, and handoffs during work

**Location**: `[harness-dir]/ses_[id]/notes/[date]-[slug].md`

**Naming Convention**:
- ISO date: `YYYY-MM-DD`
- Slug: kebab-case description

**Examples**:
```
.sisyphus/ses_abc123/notes/2026-05-12-auth-handoff.md
.cursor/ses_def456/notes/2026-05-12-api-decisions.md
```

**Alternative**: Use `wiki/sessions/` for harness-agnostic notes

**Template**:
```markdown
---
date: YYYY-MM-DD
task: "Task description"
agent: "Agent name"
changelog: false
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

## Handoffs

**To**: [Agent/Task]
**What**: [What they need to know]

## Open Questions

- [Question 1]
```

**Lifecycle**:
- Created: During implementation
- Synthesized: Promoted to `wiki/` or `docs/` if valuable
- Archived: After task completion

---

### 3. Decisions (ADRs)

**Purpose**: Document architectural decisions with rationale

**Location**: `wiki/decisions/ADR-[number]-[slug].md`

**Naming Convention**:
- `ADR-` prefix (Architecture Decision Record)
- Sequential number (001, 002, ...)
- Slug: kebab-case description

**Examples**:
```
wiki/decisions/ADR-001-auth-architecture.md
wiki/decisions/ADR-002-database-choice.md
```

**Template**:
```markdown
# ADR-[number]: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

[Problem statement and background]

## Decision

[What we decided and why]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

## Implementation

[How to implement this decision]

## References

- [Related docs]
- [Related ADRs]
```

**Lifecycle**:
- Created: When architectural decision made
- Updated: If decision evolves
- Deprecated: If superseded by new decision
- Permanent: Never deleted (historical record)

---

### 4. Status Files (Optional)

**Purpose**: Track task progress for synchronization

**Location**: `[harness-dir]/ses_[id]/status.json`

**Example**:
```json
{
  "task_id": "T-8c6ab1b2",
  "status": "in_progress",
  "started_at": "2026-05-12T10:30:00Z",
  "updated_at": "2026-05-12T11:15:00Z",
  "agent": "Sisyphus",
  "files_modified": [
    "src/auth/core.py",
    "src/auth/models.py"
  ],
  "next_step": "Waiting for API layer to complete"
}
```

**Status Values**:
- `pending` - Task queued, not started
- `in_progress` - Actively working
- `blocked` - Waiting on dependency
- `completed` - Work done, validation pending
- `validated` - All checks passed

**Lifecycle**:
- Created: When task starts
- Updated: On status changes
- Deleted: After task validated

---

## Naming Conventions

### Session IDs

Format: `ses_[random-12-chars]`

Examples:
```
ses_abc123def456
ses_789ghi012jkl
ses_mno345pqr678
```

**Generation**: Use harness-provided session ID (don't invent your own)

### Task IDs

Format: `T-[uuid-8-chars]`

Examples:
```
T-8c6ab1b2
T-78aa6c9d
T-ec10d7e8
```

**Generation**: First 8 chars of UUID v4

### Slugs

Format: kebab-case, max 5 words

Examples:
```
auth-refactor
api-layer
tests-integration
```

**Rules**:
- Lowercase only
- Hyphens between words
- No special characters
- Max 40 characters

---

## File Ownership

### Exclusive Ownership

One agent owns a file at a time:

```
File: src/auth/core.py
Owner: Agent 1 (Sisyphus)
Lock: .locks/src_auth_core.py.lock (optional)
```

### Shared Files

Multiple agents may need to edit:

**Strategy 1: Sequential**
```
Agent 1: Edit src/__init__.py (imports)
→ Complete and commit
Agent 2: Edit src/__init__.py (exports)
→ Complete and commit
```

**Strategy 2: Sections**
```
Agent 1: Edit src/auth/core.py (lines 1-100)
Agent 2: Edit src/auth/core.py (lines 101-200)
→ Merge manually after both complete
```

### Lock Files (Optional)

For critical files, use simple locks:

```bash
# Create lock
echo "Agent 1 - ses_abc123" > .locks/src_auth_core.py.lock

# Remove lock
rm .locks/src_auth_core.py.lock
```

**Lock File Format**:
```
[agent-name] - [session-id]
[started-at]
[expected-duration]
```

---

## Synchronization

### File-Based Sync

Use file timestamps to detect completion:

```python
from pathlib import Path
import time

def wait_for_completion(plan_file: Path, timeout: int = 3600):
    """Wait for plan to be marked complete."""
    start = time.time()
    while time.time() - start < timeout:
        content = plan_file.read_text()
        if "status: completed" in content:
            return True
        time.sleep(5)
    raise TimeoutError("Task did not complete in time")
```

### Status Polling

Check status files periodically:

```python
import json

def check_status(session_id: str) -> str:
    """Check task status."""
    status_file = Path(f".sisyphus/{session_id}/status.json")
    if not status_file.exists():
        return "unknown"
    data = json.loads(status_file.read_text())
    return data.get("status", "unknown")
```

### Handoff Signals

Use wiki entries for async handoffs:

```markdown
<!-- wiki/sessions/2026-05-12-handoff-core-to-api.md -->

## Handoff: Core → API

**From**: Agent 1 (ses_abc123)
**To**: Agent 2 (ses_def456)
**Time**: 2026-05-12 11:30

Core logic complete. API should expose:
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

Schema defined in `src/auth/schemas.py`

Ready for API layer implementation.
```

---

## Validation

### Pre-Integration Checklist

Before merging parallel work:

- [ ] All plans marked `completed`
- [ ] All session notes written
- [ ] No lock files remaining
- [ ] All agents validated their own work

### Integration Validation

After merging:

```bash
# Run full validation suite
uv run ruff check .
uv run ty check .
uv run pytest tests/ -v
uv run python tools/agent/validate_standards.py
uv run pre-commit run --all-files
```

### Post-Integration Checklist

After validation:

- [ ] All tests pass
- [ ] Zero type errors
- [ ] Zero lint errors
- [ ] Repository standards validated
- [ ] No merge conflicts or duplicate code
- [ ] CHANGELOG.md updated (if applicable)

---

## Archive Strategy

### When to Archive

- Task completed and validated
- Session older than 7 days
- Plan superseded by new approach

### How to Archive

```bash
# Move to archive
mv .sisyphus/ses_abc123 .sisyphus/archive/ses_abc123

# Or compress
tar -czf .sisyphus/archive/ses_abc123.tar.gz .sisyphus/ses_abc123/
rm -rf .sisyphus/ses_abc123/
```

### What to Keep

**Permanent** (never archive):
- `wiki/decisions/` - Architectural decisions
- `docs/` - Permanent documentation
- `CHANGELOG.md` - Version history

**Temporary** (archive after 7 days):
- `.sisyphus/ses_*/` - Session data
- `.cursor/ses_*/` - Session data
- `.cline/ses_*/` - Session data
- `.claude/ses_*/` - Session data

**Synthesized** (promote before archiving):
- `wiki/sessions/` - Move valuable findings to `docs/`
- Session notes with decisions → `wiki/decisions/`

---

## Examples

### Example 1: Simple Parallel Work

Two agents working on independent modules:

```
Agent 1: src/module_a/
Agent 2: src/module_b/

Artifacts:
.sisyphus/ses_abc123/plans/T-11111111-module-a.md
.sisyphus/ses_def456/plans/T-22222222-module-b.md
wiki/sessions/2026-05-12-module-a.md
wiki/sessions/2026-05-12-module-b.md
```

### Example 2: Sequential Handoff

Agent 1 completes core, Agent 2 builds API:

```
Agent 1: Core logic (days 1-2)
Agent 2: API layer (days 3-4)

Artifacts:
.sisyphus/ses_abc123/plans/T-core.md
.sisyphus/ses_def456/plans/T-api.md
wiki/sessions/2026-05-12-handoff-core-to-api.md
wiki/decisions/ADR-001-core-architecture.md
```

### Example 3: Three-Agent Parallel Work

Complex refactor with 3 parallel agents:

```
Agent 1: Core logic
Agent 2: API layer
Agent 3: Tests

Artifacts:
.sisyphus/ses_abc/plans/T-core.md
.cursor/ses_def/plans/T-api.md
.cline/ses_ghi/plans/T-tests.md
wiki/sessions/2026-05-12-core.md
wiki/sessions/2026-05-12-api.md
wiki/sessions/2026-05-12-tests.md
wiki/decisions/ADR-001-refactor-approach.md
```

---

## Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)**: 5-step coordination protocol
- **[TEMPLATES.md](../templates/)**: Plan, spec, and skill templates
- **[AGENTS.md](../AGENTS.md)**: Root-level mandates
- **[GIT_WORKFLOW.md](../GIT_WORKFLOW.md)**: Git operations for merged work
