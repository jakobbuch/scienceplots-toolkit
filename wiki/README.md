# Wiki Directory

This directory serves as the knowledge base for the SciencePlots Toolkit project. It captures session findings, architectural decisions, and research notes.

## Purpose

The wiki is the **transition layer** between "Act/Validate" and "Done". When new technical findings or architectural decisions are discovered during implementation, they are captured here first before being promoted to permanent documentation.

## Structure

```
wiki/
├── sessions/          # Session-specific findings and notes
├── decisions/         # Architectural decisions and rationale
├── research/          # Background research and analysis
└── README.md          # This file
```

### `sessions/`

Session-specific notes from AI agent work sessions:

- **Naming**: `YYYY-MM-DD-[task-slug].md`
- **Content**: What was done, what was learned, open questions
- **Lifecycle**: Temporary - synthesized into docs or decisions

**Example**:
```markdown
---
date: 2026-05-12
task: "Add validation infrastructure"
agent: "Sisyphus"
changelog: false
---

# Session: Add Validation Infrastructure

## Summary

Created tools/agent/ validation scripts for automated repository standards checking.

## Findings

- validate_standards.py checks mandatory files and directories
- validate_skill.py validates SKILL.md structure
- eval_skill.py scores skill quality (10-criteria checklist)

## Decisions

- Use exit code 0 for success, 1 for failure
- Support --verbose flag for detailed output
- Integrate with pre-commit hooks

## Open Questions

- Should we add more validation rules?
- What threshold for eval_skill.py?
```

### `decisions/`

Architectural decisions with rationale:

- **Naming**: `ADR-[number]-[decision-slug].md` (Architecture Decision Record)
- **Content**: Context, decision, consequences, status
- **Lifecycle**: Permanent - referenced in docs

**Example**:
```markdown
# ADR-001: Use pathlib.Path for All Path Operations

## Status

Accepted

## Context

The codebase needs consistent path handling that works across platforms and from any execution directory.

## Decision

ALWAYS use `pathlib.Path` for all path operations. NEVER use `os.chdir()` or string concatenation.

## Consequences

### Positive
- Scripts work from any directory
- Cross-platform compatibility
- Cleaner, more readable code

### Negative
- Requires Python 3.4+ (already satisfied)

## Implementation

- Update all existing scripts to use Path
- Add to AGENTS.md mandates
- Enforce via validate_standards.py
```

### `research/`

Background research and analysis:

- **Naming**: `[topic]-research.md`
- **Content**: Market research, competitive analysis, technical deep-dives
- **Lifecycle**: Reference material

**Example**:
```markdown
# Matplotlib Style Libraries Research

## Overview

Analysis of existing Matplotlib style libraries and best practices.

## Libraries Analyzed

1. **SciencePlots**
   - Styles: science, ieee, no-latex
   - Focus: Publication-quality scientific plots
   - License: MIT

2. **seaborn**
   - Built on matplotlib
   - Statistical plotting focus
   - License: BSD

## Best Practices

- Use constrained_layout instead of tight_layout
- Override color cycles for consistency
- Support both LaTeX and mathtext rendering

## Recommendations

- Build on top of SciencePlots (already done)
- Add cmap library for qualitative colormaps
- Implement PreambleManager for LaTeX configuration
```

## Workflow

### Capture (During Implementation)

1. **Create session note** in `sessions/`
2. **Document findings** as you work
3. **Tag with `changelog: true`** if structural change

### Synthesize (After Completion)

1. **Review session notes** for important findings
2. **Promote to `docs/`** if permanent documentation needed
3. **Create decision record** in `decisions/` for architectural choices
4. **Update `CHANGELOG.md`** from changelog-tagged entries

### Maintenance

- **Archive old sessions**: Move to `archive/` after synthesis
- **Keep decisions current**: Update status as decisions evolve
- **Link related docs**: Cross-reference between wiki and docs

## YAML Frontmatter

All wiki entries use YAML frontmatter:

```yaml
---
date: YYYY-MM-DD
task: "Task description"
agent: "Agent name"
changelog: true|false  # Should this be in CHANGELOG.md?
tags: [tag1, tag2]     # Optional tags for organization
---
```

## Changelog Synthesis

Entries tagged with `changelog: true` are candidates for `CHANGELOG.md`:

```yaml
---
changelog: true
---
```

These entries should be synthesized into the changelog under:
- **Added**: New features, tools, documentation
- **Changed**: Modified behavior, APIs, standards
- **Removed**: Deprecated features, removed code

## Related Documentation

- **[CHANGELOG.md](../CHANGELOG.md)**: Auto-synthesized from wiki entries
- **[docs/](../docs/)**: Permanent documentation (promoted from wiki)
- **[AGENTS.md](../AGENTS.md)**: Agent mandates including wiki-first knowledge capture
