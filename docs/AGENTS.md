# AGENTS.md — Documentation Engineering (`docs/`)

This directory is the central knowledge base. Documentation must be engineered with the same rigour as code.

## Global Mandates

<!-- rule:D-001 -->

- **Inherit Root Mandates**: All instructions in the [Root AGENTS.md](../AGENTS.md) apply here.

## Documentation Structure & Flow

<!-- rule:D-002 -->

- **Follow Progressive Disclosure**: concept → capabilities → examples → config → edge cases
  - Helps readers build mental models incrementally
  - Reduces cognitive load
  - Start with high-level concepts, drill down to details

<!-- rule:D-003 -->

- **Structure Examples: Context → Code → Details**
  - Never show code without preceding context
  - Readers understand purpose before seeing implementation
  - Example structure:
    ```markdown
    ### When to Use

    [Context: when this pattern applies]

    ### Example

    ```python
    [Code example]
    ```

### Details

[Explanation of parameters, options, etc.]
    ```

<!-- rule:D-004 -->

- **Focus on User Tasks & Public APIs**
  - Task-oriented guides help users accomplish goals faster
  - Defer internal implementation details to docstrings
  - Show what, not how (unless it's a "how-to" guide)

## High-Signal Content

<!-- rule:D-005 -->

- **Demonstrate Realistic Use Cases**
  - Avoid toy scenarios or debugging snippets
  - Well-crafted examples show actual value
  - Prevent cargo-culting (copying without understanding)

<!-- rule:D-006 -->

- **Show Recommended Approach First**
  - Introduce alternatives only after best practice
  - Prevents users from adopting legacy or suboptimal patterns
  - Example:
    ```markdown
    ### Recommended: Using configure_matplotlib_style()

    [Best practice example]

    ### Alternative: Manual Configuration

    [Alternative approach - only if needed]
    ```

<!-- rule:D-007 -->

- **Remove "Working as Expected" Noise**
  - Focus only on limitations, deviations, or integration concerns
  - Reduces cognitive load
  - Prevents documentation staleness

## Formatting & Linking

<!-- rule:D-008 -->

- **Link All Concepts to Reference Pages**
  - Use anchor fragments (`#section`) for precision
  - Improves discoverability
  - Reduces navigation friction
  - Example: `[configure_matplotlib_style](ARCHITECTURE.md#style-configuration)`

<!-- rule:D-009 -->

- **Use MkDocs Admonitions for Callouts**
  ```markdown
  !!! note "Title"
      This is a note admonition.

  !!! warning "Warning Title"
      This is a warning admonition.

  !!! tip "Pro Tip"
      This is a tip admonition.
  ```
  - Ensures consistent rendering
  - Prevents TOC clutter

<!-- rule:D-010 -->

- **Use Reference-Style Links for API Elements**
  - Enables interactive features like hover docs in MkDocs
  - Example: `[ElementName][path.ElementName]`

## Documentation Types

### Conceptual Guides

Explain concepts, architecture, and design decisions:

- **Purpose**: Help readers understand the "why"
- **Structure**: Problem → Solution → Tradeoffs
- **Examples**: `ARCHITECTURE.md`, `PHILOSOPHY.md`

### How-To Guides

Task-oriented instructions:

- **Purpose**: Help readers accomplish specific goals
- **Structure**: Prerequisites → Steps → Verification
- **Examples**: `GIT_WORKFLOW.md`, `PAV_CYCLE.md`

### API Reference

Technical API documentation:

- **Purpose**: Document public interfaces
- **Structure**: Function signature → Description → Parameters → Returns → Examples
- **Location**: Docstrings in source code, auto-generated

### Templates

Reusable templates for agent workflows:

- **Purpose**: Standardize agent outputs
- **Structure**: Placeholder fields with instructions
- **Examples**: `templates/PLAN.md`, `templates/SPEC.md`

## Documentation Maintenance

<!-- rule:D-011 -->

- **Update Documentation with Code**
  - Documentation changes are part of the PR
  - Don't merge code without updating docs
  - Test examples in documentation

<!-- rule:D-012 -->

- **Version Documentation**
  - Note version-specific behavior
  - Use deprecation warnings for old patterns
  - Example:
    ```markdown
    !!! warning "Deprecated in v2.0"
        This pattern is deprecated. Use [new pattern](new-pattern.md) instead.
    ```

<!-- rule:D-013 -->

- **Link Related Documentation**
  - Always provide "See Also" or "Related" sections
  - Help readers navigate to related concepts
  - Example:
    ```markdown
    ## Related Documentation

    - [Architecture](ARCHITECTURE.md)
    - [API Design](API_DESIGN.md)
    - [Python Standards](PYTHON_STANDARDS.md)
    ```

## Validation

Before committing documentation changes:

```bash
# Check markdown linting
uv run mdlint check docs/

# Check links (if tool available)
uv run mkdocs serve  # Preview locally

# Validate standards
uv run python tools/agent/validate_standards.py
```

## Writing Standards

<!-- rule:D-014 -->

- **Use Active Voice**: "The function returns" not "A value is returned"
- **Be Concise**: Remove unnecessary words
- **Use Consistent Terminology**: Don't use "function", "method", "routine" interchangeably
- **Spell Check**: Use American English spelling
- **Code Formatting**: Use backticks for inline code, fenced blocks for multi-line

## Documentation Templates

Use templates in `templates/` directory:

- **[PLAN.md](templates/PLAN.md)**: Implementation plans
- **[SPEC.md](templates/SPEC.md)**: Feature specifications
- **[SKILL.md](templates/SKILL.md)**: Agent skill documentation

## Related Documentation

- **[Root AGENTS.md](../AGENTS.md)**: Global mandates
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture
- **[PYTHON_STANDARDS.md](PYTHON_STANDARDS.md)**: Python coding standards
- **[API_DESIGN.md](API_DESIGN.md)**: API design principles

## Gotchas

- **Don't Write Walls of Text**: Use headings, lists, code blocks
- **Don't Assume Knowledge**: Link to prerequisite concepts
- **Don't Skip Examples**: Every feature needs at least one example
- **Don't Use Jargon Without Definition**: Define technical terms on first use
- **Don't Forget Mobile**: Documentation should be readable on all devices
