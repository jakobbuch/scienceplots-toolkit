---
name: [Skill Name]
description: [Expert guidance for using specific tools, frameworks, or workflows]
type: [tool | role]  # tool-focused (Layout 1) or role-focused (Layout 2)


# [Skill Name]

<!--
SKILL.md Template

Two layouts available:
- Layout 1 (Tool-Focused): Expert guidance for specific tools (e.g., ruff, uv, ty)
- Layout 2 (Role-Focused): Persona-based identity with mission and workflow

Choose the layout that matches your skill's purpose.
- -->

## When to Use This Skill

**Always use this skill when:**

- [Specific trigger condition 1]
- [Specific trigger condition 2]
- [Specific trigger condition 3]

**Do NOT use this skill when:**

- [Condition when NOT to use]
- [Alternative skill or approach to use instead]

---

## Core Mandates

<!-- rule:SK-001 -->

**[Mandate 1 - e.g., ALWAYS run tool before committing]**

[Explanation and rationale for this mandate.]

```bash
# ✅ CORRECT
[command or code example showing correct usage]

# ❌ WRONG
[command or code example showing incorrect usage]
```

<!-- rule:SK-002 -->

**[Mandate 2 - e.g., NEVER suppress warnings]**

[Explanation and rationale for this mandate.]

```bash
# ✅ CORRECT
[correct example]

# ❌ WRONG
[incorrect example]
```

<!-- rule:SK-003 -->

**[Mandate 3 - e.g., ALWAYS verify with tests]**

[Explanation and rationale for this mandate.]

---

## Usage Examples

### Basic Usage

[Simple, common use case example.]

```bash
# Example command or code
[command or code]
```

### Advanced Usage

[More complex or specialized use case.]

```bash
# Advanced example
[command or code]
```

### Configuration

[How to configure or customize the tool/workflow.]

```toml
# Example configuration (pyproject.toml, config file, etc.)
[configuration]
```

---

## Tool Documentation

For detailed API specifications and options, read:

- **Official Docs**: [URL to official documentation]
- **Configuration**: [path/to/config/file]
- **Examples**: [path/to/examples]

---

## Quality Checklist

Before considering a task complete:

- [ ] [Checklist item 1 - specific, verifiable]
- [ ] [Checklist item 2 - specific, verifiable]
- [ ] [Checklist item 3 - specific, verifiable]
- [ ] [Checklist item 4 - specific, verifiable]

---

## Related Skills

- **[Skill Name]**: [Brief description of related skill]
- **[Another Skill]**: [Brief description]

## Related Documentation

- **[Document Name]**: [path/to/document.md] - [What it covers]
- **[Another Document]**: [path/to/another.md] - [What it covers]

---

## Parallel Execution & Statelessness

This skill is **stateless and parallel-safe**:

- **No Session State**: Does not maintain any session-specific state
- **Idempotent Operations**: Can be safely repeated
- **Parallel-Safe**: Multiple agents can use simultaneously
- **Harness-Agnostic**: Works across all agent harnesses

### Coordination for Parallel Work

When multiple agents use this skill:

1. **Clear Boundaries**: Each agent works on independent tasks
2. **Shared Standards**: All agents follow documented patterns
3. **No Conflicts**: Avoid file collisions
4. **Verification**: Validate after merging work

---

<!--
=== ALTERNATIVE: LAYOUT 2 (ROLE-FOCUSED) ===

Use Layout 2 for persona-based skills (e.g., git-master, python, reviewer).
Uncomment and use the structure below instead of Layout 1 above.

---

## Identity

You are **[Role Name]**, a [brief description of role/persona].

- **Mission**: [One sentence describing your core mission]

- **Expertise**: [List of areas of expertise]

## When to Activate

Activate this skill when:

- [Trigger condition 1]
- [Trigger condition 2]

## Workflow

### 1. [Phase Name]

[Description of this phase.]

- **Actions**:

1. [Action 1]
2. [Action 2]

### 2. [Next Phase]

[Description of next phase.]

## Mandates

- **ALWAYS**: [Mandate 1]
- **NEVER**: [Mandate 2]
- **MUST**: [Mandate 3]

## Examples

[Example interactions or workflows]
[Example interactions or workflows]
