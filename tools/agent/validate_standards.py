#!/usr/bin/env python3
"""Automated Standards Validator for SciencePlots Toolkit.

This script verifies if the repository adheres to the required structure and
mandates for AI agent collaboration.
"""

import argparse
import sys
from pathlib import Path


class ValidationResult:
    """Container for validation results."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        """Record an error."""
        self.errors.append(message)

    def warning(self, message: str) -> None:
        """Record a warning."""
        self.warnings.append(message)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0


def validate_mandatory_files(root: Path, result: ValidationResult) -> None:
    """Validate mandatory root-level files exist."""
    mandatory_files = [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "pyproject.toml",
        ".pre-commit-config.yaml",
    ]

    for filename in mandatory_files:
        if not (root / filename).exists():
            result.error(f"Mandatory file missing: {filename}")


def validate_mandatory_directories(root: Path, result: ValidationResult) -> None:
    """Validate mandatory directories exist."""
    mandatory_dirs = [
        "src/scienceplots_toolkit",
        "examples",
        "tests",
        "docs",
        ".agents/skills",
        "output",
    ]

    for dirname in mandatory_dirs:
        if not (root / dirname).exists():
            result.error(f"Mandatory directory missing: {dirname}")


def validate_mandatory_docs(root: Path, result: ValidationResult) -> None:
    """Validate mandatory documentation files exist."""
    mandatory_docs = [
        "docs/ARCHITECTURE.md",
        "docs/PYTHON_STANDARDS.md",
        "src/scienceplots_toolkit/AGENTS.md",
    ]

    for docpath in mandatory_docs:
        if not (root / docpath).exists():
            result.error(f"Mandatory documentation missing: {docpath}")


def validate_agents_md(root: Path, result: ValidationResult) -> None:
    """Validate AGENTS.md contains required sections."""
    agents_path = root / "AGENTS.md"
    if not agents_path.exists():
        return  # Already caught by mandatory files check

    content = agents_path.read_text()

    if "## Core Mandates" not in content and "## Core Principles" not in content:
        result.error(
            "AGENTS.md must contain '## Core Mandates' or '## Core Principles' section"
        )

    if (
        "scienceplots-viz" not in content
        and ".agents/skills/scienceplots-viz" not in content
    ):
        result.warning("AGENTS.md should reference the scienceplots-viz skill")


def validate_changelog(root: Path, result: ValidationResult) -> None:
    """Validate CHANGELOG.md structure."""
    changelog_path = root / "CHANGELOG.md"
    if not changelog_path.exists():
        return  # Already caught by mandatory files check

    content = changelog_path.read_text()

    if (
        "# Changelog" not in content
        and "## Changelog" not in content
        and "## [" not in content
    ):
        result.error("CHANGELOG.md must contain a 'Changelog' header")


def validate_skills_directory(root: Path, result: ValidationResult) -> None:
    """Validate skills directory structure."""
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.exists():
        return  # Already caught by mandatory directories check

    skill_files = list(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        result.warning("No SKILL.md files found in .agents/skills/")

    # Check for scienceplots-viz skill
    scienceplots_skill = skills_dir / "scienceplots-viz" / "SKILL.md"
    if not scienceplots_skill.exists():
        result.error(
            "Missing scienceplots-viz skill: .agents/skills/scienceplots-viz/SKILL.md"
        )


def validate_precommit_hooks(root: Path, result: ValidationResult) -> None:
    """Validate pre-commit configuration exists and has required hooks."""
    precommit_path = root / ".pre-commit-config.yaml"
    if not precommit_path.exists():
        return  # Already caught by mandatory files check

    content = precommit_path.read_text()

    required_hooks = ["ruff", "pre-commit-hooks"]
    for hook in required_hooks:
        if hook not in content:
            result.warning(f"Recommended pre-commit hook missing: {hook}")


def validate() -> None:
    """Validate the repository against scienceplots standards."""
    root = Path(".")
    result = ValidationResult()

    # Run all validations
    validate_mandatory_files(root, result)
    validate_mandatory_directories(root, result)
    validate_mandatory_docs(root, result)
    validate_agents_md(root, result)
    validate_changelog(root, result)
    validate_skills_directory(root, result)
    validate_precommit_hooks(root, result)

    # Output results
    if result.warnings:
        print("--- WARNINGS ---")
        for warning in result.warnings:
            print(f"WARN: {warning}")
        print()

    if result.errors:
        print("--- ERRORS ---")
        for error in result.errors:
            print(f"ERR: {error}")
        print()
        print("Validation FAILED. Fix the errors above.")
        sys.exit(1)
    else:
        print("✅ Repository standards validation successful!")
        sys.exit(0)


def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Automated Standards Validator for SciencePlots Toolkit.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation progress",
    )
    args = parser.parse_args()

    if args.verbose:
        print("Starting repository validation...")

    validate()


if __name__ == "__main__":
    main()
