# Agent Tooling

This directory contains scripts and utilities designed to be executed by AI agents to enhance their context, automate tasks, or validate work.

## validate_standards.py

Automated validator that enforces repository structure and standards compliance.

### Usage (validate_standards.py)

```bash
uv run python tools/agent/validate_standards.py
```

### Validation Checks (validate_standards.py)

**Mandatory Files** (errors if missing):

- `AGENTS.md` — Root agent instruction document
- `README.md` — Project overview
- `CHANGELOG.md` — Record of structural changes
- `CONTRIBUTING.md` — Shared standards and check suite
- `pyproject.toml` — Project configuration
- `.pre-commit-config.yaml` — Pre-commit hook configuration

**Mandatory Directories** (errors if missing):

- `src/scienceplots_toolkit/` — Core package
- `examples/` — Example scripts
- `tests/` — Test suite
- `docs/` — Technical documentation
- `.agents/skills/` — Agent skills
- `output/` — Generated plots

**Content Validation** (errors if violated):

- `AGENTS.md` must contain `## Core Mandates` or `## Core Principles` section
- `AGENTS.md` should reference the scienceplots-viz skill
- `CHANGELOG.md` must contain a 'Changelog' header
- Skills directory must contain SKILL.md files

**Skills Validation** (warnings if violated):

- Missing scienceplots-viz skill triggers error
- No SKILL.md files found triggers warning

**Pre-commit Validation** (warnings if violated):

- Recommended hooks: ruff, pre-commit-hooks

### Exit Codes (validate_standards.py)

- `0` — Repository is compliant
- `1` — Validation errors found (check stderr for details)

### Integration

This validator is integrated into the pre-commit pipeline and runs automatically before each commit.

## validate_skill.py

Structural validator for SKILL.md files. Validates frontmatter, layout sections, markdown links, rule IDs, and identity sections.

### Usage (validate_skill.py)

```bash
# Validate a specific skill file
uv run python tools/agent/validate_skill.py --path .agents/skills/scienceplots-viz/SKILL.md

# Validate all skills in a directory
uv run python tools/agent/validate_skill.py --dir .agents/skills/

# Check if a proposed name collides with reserved names
uv run python tools/agent/validate_skill.py --check-name "my-skill"

# Verbose output
uv run python tools/agent/validate_skill.py --dir .agents/skills/ --verbose
```

### Validation Checks (validate_skill.py)

**Structural**:
- YAML frontmatter (name, description fields)
- Layout sections (When to Use, Core, Example, Related, Quality)
- Markdown links (all relative links resolve)
- Rule IDs (unique `<!-- rule:XXX -->` markers)
- Identity section (present and correct)

**Name Collision**:
- Reserved names: playwright, dev-browser, git-master, review-work, ai-slop-remover, frontend-ui-ux
- Namespace prefixes: system/, user/, project/
- Name already exists in skills directory

### Name Collision Examples

**Reserved name check**:

```bash
uv run python tools/agent/validate_skill.py --check-name "playwright"
# ERROR: Reserved name: 'playwright' is a built-in skill name.
```

**Namespace prefix check**:

```bash
uv run python tools/agent/validate_skill.py --check-name "system/git"
# ERROR: Namespace prefix rejected: starts with reserved namespace 'system/'
```

**Valid name**:

```bash
uv run python tools/agent/validate_skill.py --check-name "my-custom-skill"
# Name 'my-custom-skill' is valid.
```

### Exit Codes (validate_skill.py)

- `0` — Skill (or all skills) is compliant
- `1` — Validation errors found

## eval_skill.py

Quality evaluator for SKILL.md files. Uses checklist-based scoring to assess skill completeness.

### Usage (eval_skill.py)

```bash
# Evaluate a specific skill file
uv run python tools/agent/eval_skill.py --path .agents/skills/scienceplots-viz/SKILL.md

# Evaluate all skills in a directory
uv run python tools/agent/eval_skill.py --dir .agents/skills/

# Evaluate with custom threshold (default 70%)
uv run python tools/agent/eval_skill.py --dir .agents/skills/ --threshold 90

# Verbose output
uv run python tools/agent/eval_skill.py --dir .agents/skills/ --verbose
```

### Evaluation Checklist

10 criteria evaluated:

1. ✅ YAML frontmatter with name and description
2. ✅ Has 'When to Use' section or equivalent
3. ✅ Has usage code examples
4. ✅ All relative links resolve
5. ✅ Rule IDs present in mandate sections
6. ✅ No TODO markers or placeholder text
7. ✅ Has identity/mandate section
8. ✅ Has references/related resources section
9. ✅ Has quality checklist or verification section
10. ✅ Has complete working example

### Scoring

Score = (Pass count) / (Pass + Fail count) × 100

Default threshold is 70%. Customize with `--threshold`.

### Exit Codes (eval_skill.py)

- `0` — Skill passes threshold
- `1` — Skill fails threshold

## How to Add a Tool

1. **Script**: Place your script in `tools/agent/`
2. **Documentation**: Register it in this README
3. **Skills**: Add its usage to `.agents/skills/` so agents can discover it
4. **Testing**: Add tests in `tests/` if applicable
5. **Validation**: Update `validate_standards.py` if it adds new requirements

## Integration with Workflows

These tools are designed to be used:

- **Pre-commit**: `validate_standards.py` runs before each commit
- **CI/CD**: All validators should run in CI pipeline
- **Agent Workflows**: Agents use these tools to validate their work
- **Manual Review**: Humans can run validators to check compliance

## Related Documentation

- **[AGENTS.md](../AGENTS.md)**: Root-level agent mandates
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Development workflow
- **[.agents/skills/](../.agents/skills/)**: Agent skills directory
- **[docs/templates/](../docs/templates/)**: Templates for plans and specs
