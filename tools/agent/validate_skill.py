#!/usr/bin/env python3
"""Structural Validator for SKILL.md Files.

This script validates that skill files follow the required structure and
format for AI agent skills.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    """Result of validating a single skill file."""

    file: Path
    passed: bool
    errors: list[str]
    warnings: list[str]


# Reserved skill names that cannot be used
RESERVED_NAMES = {
    "playwright",
    "dev-browser",
    "git-master",
    "review-work",
    "ai-slop-remover",
    "frontend-ui-ux",
}

# Reserved namespace prefixes
RESERVED_PREFIXES = {"system/", "user/", "project/"}


def validate_yaml_frontmatter(content: str, filepath: Path) -> list[str]:
    """Validate YAML frontmatter structure."""
    errors = []

    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter start (---)")
        return errors

    # Find end of frontmatter
    end_match = re.search(r"\n---\n", content)
    if not end_match:
        errors.append("Missing YAML frontmatter end (---)")
        return errors

    frontmatter = content[4 : end_match.start()]

    # Check for required fields
    if "name:" not in frontmatter:
        errors.append("Missing 'name:' field in YAML frontmatter")

    if "description:" not in frontmatter:
        errors.append("Missing 'description:' field in YAML frontmatter")

    return errors


def validate_layout_sections(content: str, filepath: Path) -> list[str]:
    """Validate that skill has required layout sections."""
    errors = []

    # Check for at least one major section
    required_sections = [
        "## When to Use",
        "## Core",
        "## Example",
        "## Related",
        "## Quality",
    ]

    has_section = any(section in content for section in required_sections)
    if not has_section:
        errors.append(
            "Missing required sections. Skill should have at least one of: "
            "'## When to Use', '## Core', '## Example', '## Related', or '## Quality'"
        )

    return errors


def validate_markdown_links(content: str, filepath: Path) -> list[str]:
    """Validate that relative markdown links resolve."""
    errors = []
    skill_dir = filepath.parent

    # Find all relative markdown links
    link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(link_pattern, content)

    for link_text, link_url in matches:
        # Skip absolute URLs and anchors
        if link_url.startswith(("http://", "https://", "#")):
            continue

        # Check if link resolves
        link_path = skill_dir / link_url.split("#")[0]
        if not link_path.exists():
            errors.append(f"Broken link: [{link_text}]({link_url})")

    return errors


def validate_rule_ids(content: str, filepath: Path) -> tuple[list[str], list[str]]:
    """Validate rule ID markers are present and unique."""
    errors = []
    warnings = []

    # Find all rule IDs
    rule_pattern = r"<!--\s*rule:[A-Z]-\d+\s*-->"
    rule_ids = re.findall(rule_pattern, content)

    if not rule_ids:
        warnings.append("No rule IDs found (<!-- rule:XXX -->)")
        return errors, warnings

    # Check for duplicates
    seen = set()
    duplicates = set()
    for rule_id in rule_ids:
        if rule_id in seen:
            duplicates.add(rule_id)
        seen.add(rule_id)

    if duplicates:
        errors.append(f"Duplicate rule IDs: {', '.join(duplicates)}")

    return errors, warnings


def validate_identity_section(content: str, filepath: Path) -> list[str]:
    """Validate that skill has identity/mandate section."""
    warnings = []

    # Check for identity indicators
    identity_patterns = [
        "## When to Use",
        "## Core Mandates",
        "## Core Principles",
        "MUST",
        "ALWAYS",
        "NEVER",
    ]

    has_identity = any(pattern in content for pattern in identity_patterns)
    if not has_identity:
        warnings.append(
            "Skill may be missing identity/mandate section. "
            "Consider adding '## When to Use' or '## Core Mandates'"
        )

    return warnings


def check_name_collision(name: str, skills_dir: Path) -> list[str]:
    """Check if a proposed skill name collides with reserved names."""
    errors = []

    # Check reserved names
    if name in RESERVED_NAMES:
        reserved_list = ", ".join(sorted(RESERVED_NAMES))
        errors.append(
            f"Reserved name: '{name}' is a built-in skill name. "
            f"Reserved names: {reserved_list}"
        )

    # Check reserved prefixes
    for prefix in RESERVED_PREFIXES:
        if name.startswith(prefix):
            errors.append(
                f"Namespace prefix rejected: '{name}' starts with reserved "
                f"namespace '{prefix}'"
            )

    # Check if name already exists
    skill_dir = skills_dir / name
    if skill_dir.exists() and skill_dir.is_dir():
        errors.append(
            f"Name already exists: directory '{name}' already exists in '{skills_dir}'"
        )

    return errors


def validate_skill_file(filepath: Path, skills_dir: Path) -> ValidationResult:
    """Validate a single SKILL.md file."""
    errors = []
    warnings = []

    if not filepath.exists():
        return ValidationResult(
            file=filepath,
            passed=False,
            errors=[f"File does not exist: {filepath}"],
            warnings=[],
        )

    content = filepath.read_text()

    # Run all validations
    errors.extend(validate_yaml_frontmatter(content, filepath))
    errors.extend(validate_layout_sections(content, filepath))
    errors.extend(validate_markdown_links(content, filepath))

    rule_errors, rule_warnings = validate_rule_ids(content, filepath)
    errors.extend(rule_errors)
    warnings.extend(rule_warnings)

    warnings.extend(validate_identity_section(content, filepath))

    # Check name collision from filename
    skill_name = filepath.parent.name
    name_errors = check_name_collision(skill_name, skills_dir)
    errors.extend(name_errors)

    passed = len(errors) == 0

    return ValidationResult(
        file=filepath,
        passed=passed,
        errors=errors,
        warnings=warnings,
    )


def validate_all_skills(skills_dir: Path) -> list[ValidationResult]:
    """Validate all SKILL.md files in a directory."""
    results = []

    if not skills_dir.exists():
        return [
            ValidationResult(
                file=skills_dir,
                passed=False,
                errors=[f"Skills directory does not exist: {skills_dir}"],
                warnings=[],
            )
        ]

    skill_files = list(skills_dir.glob("*/SKILL.md"))

    for skill_file in skill_files:
        result = validate_skill_file(skill_file, skills_dir)
        results.append(result)

    return results


def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Structural Validator for SKILL.md Files.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="Validate a specific SKILL.md file",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Validate all SKILL.md files in a directory",
    )
    parser.add_argument(
        "--check-name",
        metavar="NAME",
        help="Check if a proposed skill name collides with reserved names",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation progress",
    )

    args = parser.parse_args()

    # Determine validation mode
    if args.check_name:
        # Name collision check
        skills_dir = Path(".agents/skills")
        errors = check_name_collision(args.check_name, skills_dir)
        if errors:
            for error in errors:
                print(f"ERR: {error}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Name '{args.check_name}' is valid.")
            sys.exit(0)

    elif args.path:
        # Single file validation
        result = validate_skill_file(args.path, args.path.parent)
        print_validation_result(result, args.verbose)
        sys.exit(0 if result.passed else 1)

    elif args.dir:
        # Directory validation
        results = validate_all_skills(args.dir)
        all_passed = all(r.passed for r in results)

        for result in results:
            print_validation_result(result, args.verbose)

        sys.exit(0 if all_passed else 1)

    else:
        # Default: validate .agents/skills/
        skills_dir = Path(".agents/skills")
        results = validate_all_skills(skills_dir)
        all_passed = all(r.passed for r in results)

        for result in results:
            print_validation_result(result, args.verbose)

        sys.exit(0 if all_passed else 1)


def print_validation_result(result: ValidationResult, verbose: bool) -> None:
    """Print validation results in a formatted way."""
    status = "✅ PASS" if result.passed else "❌ FAIL"
    print(f"\n{status}: {result.file}")

    if result.errors:
        print("  Errors:")
        for error in result.errors:
            print(f"    - {error}")

    if result.warnings:
        print("  Warnings:")
        for warning in result.warnings:
            print(f"    - {warning}")

    if verbose and result.passed and not result.warnings:
        print("  No issues found.")


if __name__ == "__main__":
    main()
