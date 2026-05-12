#!/usr/bin/env python3
"""Quality Evaluator for SKILL.md Files.

This script uses checklist-based scoring to assess skill completeness
and quality.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class EvaluationResult(NamedTuple):
    """Result of evaluating a single skill file."""

    file: Path
    score: float
    passed: bool
    pass_count: int
    fail_count: int
    na_count: int
    details: list[tuple[str, bool, str | None]]


EVALUATION_CHECKLIST = [
    ("YAML frontmatter with name and description", "yaml_frontmatter"),
    ("Has 'When to Use' section or equivalent", "when_to_use"),
    ("Has usage code examples", "code_examples"),
    ("All relative links resolve", "links_resolve"),
    ("Rule IDs present in mandate sections", "rule_ids"),
    ("No TODO markers or placeholder text", "no_todos"),
    ("Has identity/mandate section", "identity"),
    ("Has references/related resources section", "references"),
    ("Has quality checklist or verification section", "quality_checklist"),
    ("Has complete working example", "complete_example"),
]


def check_yaml_frontmatter(content: str) -> tuple[bool, str | None]:
    """Check for YAML frontmatter with required fields."""
    if not content.startswith("---"):
        return False, "Missing YAML frontmatter"

    end_match = re.search(r"\n---\n", content)
    if not end_match:
        return False, "Incomplete YAML frontmatter"

    frontmatter = content[4 : end_match.start()]

    has_name = "name:" in frontmatter
    has_description = "description:" in frontmatter

    if has_name and has_description:
        return True, None
    elif has_name:
        return False, "Missing 'description:' field"
    elif has_description:
        return False, "Missing 'name:' field"
    else:
        return False, "Missing both 'name:' and 'description:' fields"


def check_when_to_use(content: str) -> tuple[bool, str | None]:
    """Check for 'When to Use' section."""
    patterns = [
        "## When to Use",
        "## When to Use This Skill",
        "## Usage",
        "## Triggers",
    ]
    for pattern in patterns:
        if pattern in content:
            return True, None
    return False, "Missing 'When to Use' section"


def check_code_examples(content: str) -> tuple[bool, str | None]:
    """Check for code examples."""
    # Look for code blocks
    code_blocks = re.findall(r"```[\s\S]*?```", content)
    if not code_blocks:
        return False, "No code examples found"

    # Check if at least one code block has substantial content
    for block in code_blocks:
        lines = block.strip().split("\n")
        if len(lines) > 2:  # At least 1 line of actual code
            return True, None

    return False, "Code examples are too minimal"


def check_links_resolve(content: str, filepath: Path) -> tuple[bool, str | None]:
    """Check that relative markdown links resolve."""
    skill_dir = filepath.parent
    link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(link_pattern, content)

    broken_links = []
    for link_text, link_url in matches:
        # Skip absolute URLs and anchors
        if link_url.startswith(("http://", "https://", "#")):
            continue

        # Check if link resolves
        link_path = skill_dir / link_url.split("#")[0]
        if not link_path.exists():
            broken_links.append(link_url)

    if broken_links:
        return False, f"Broken links: {', '.join(broken_links[:3])}"
    return True, None


def check_rule_ids(content: str) -> tuple[bool, str | None]:
    """Check for rule ID markers."""
    rule_pattern = r"<!--\s*rule:[A-Z]-\d+\s*-->"
    rule_ids = re.findall(rule_pattern, content)

    if rule_ids:
        return True, None
    return False, "No rule IDs found (<!-- rule:XXX -->)"


def check_no_todos(content: str) -> tuple[bool, str | None]:
    """Check for TODO markers or placeholder text."""
    todo_patterns = [
        r"\bTODO\b",
        r"\bFIXME\b",
        r"\bXXX\b",
        r"\bPLACEHOLDER\b",
        r"\[.*\.\.\..*\]",  # [something...]
    ]

    for pattern in todo_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False, "Found TODO markers or placeholder text"

    return True, None


def check_identity(content: str) -> tuple[bool, str | None]:
    """Check for identity/mandate section."""
    identity_patterns = [
        "## Core Mandates",
        "## Core Principles",
        "## Identity",
        "## Mission",
    ]

    # Also check for mandate language
    mandate_language = ["MUST", "ALWAYS", "NEVER", "REQUIRED"]
    has_mandate_language = any(lang in content for lang in mandate_language)

    for pattern in identity_patterns:
        if pattern in content:
            return True, None

    if has_mandate_language:
        return True, None

    return False, "Missing identity/mandate section"


def check_references(content: str) -> tuple[bool, str | None]:
    """Check for references/related resources section."""
    patterns = [
        "## Related",
        "## References",
        "## Resources",
        "## See Also",
        "## Documentation",
        "## Bundled Resources",
    ]

    for pattern in patterns:
        if pattern in content:
            return True, None

    return False, "Missing references/resources section"


def check_quality_checklist(content: str) -> tuple[bool, str | None]:
    """Check for quality checklist or verification section."""
    patterns = [
        "## Quality Checklist",
        "## Verification",
        "## Checklist",
        "## Acceptance Criteria",
    ]

    for pattern in patterns:
        if pattern in content:
            return True, None

    return False, "Missing quality checklist section"


def check_complete_example(content: str) -> tuple[bool, str | None]:
    """Check for complete working example."""
    # Look for substantial code blocks
    code_blocks = re.findall(r"```[\s\S]*?```", content)

    for block in code_blocks:
        lines = block.strip().split("\n")
        # Check for a complete example (imports + main logic)
        if len(lines) >= 10:
            has_import = any("import" in line for line in lines)
            # has_main = any(
            if has_import:
                return True, None

    return False, "Missing complete working example"


def evaluate_skill_file(filepath: Path) -> EvaluationResult:
    """Evaluate a single SKILL.md file."""
    if not filepath.exists():
        return EvaluationResult(
            file=filepath,
            score=0.0,
            passed=False,
            pass_count=0,
            fail_count=len(EVALUATION_CHECKLIST),
            na_count=0,
            details=[
                (name, False, "File does not exist") for name, _ in EVALUATION_CHECKLIST
            ],
        )

    content = filepath.read_text()
    details = []
    pass_count = 0
    fail_count = 0
    na_count = 0

    # Run all checks
    checks = [
        ("yaml_frontmatter", check_yaml_frontmatter),
        ("when_to_use", check_when_to_use),
        ("code_examples", check_code_examples),
        ("links_resolve", lambda c: check_links_resolve(c, filepath)),
        ("rule_ids", check_rule_ids),
        ("no_todos", check_no_todos),
        ("identity", check_identity),
        ("references", check_references),
        ("quality_checklist", check_quality_checklist),
        ("complete_example", check_complete_example),
    ]

    for check_name, check_func in checks:
        try:
            passed, message = check_func(content)
            details.append((check_name, passed, message))
            if passed:
                pass_count += 1
            else:
                fail_count += 1
        except Exception as e:
            details.append((check_name, False, f"Error: {e}"))
            fail_count += 1

    # Calculate score (ignore N/A for now)
    total = pass_count + fail_count
    score = (pass_count / total * 100) if total > 0 else 0.0

    return EvaluationResult(
        file=filepath,
        score=score,
        passed=score >= 70.0,  # Default threshold
        pass_count=pass_count,
        fail_count=fail_count,
        na_count=na_count,
        details=details,
    )


def evaluate_all_skills(
    skills_dir: Path, threshold: float = 70.0
) -> list[EvaluationResult]:
    """Evaluate all SKILL.md files in a directory."""
    results = []

    if not skills_dir.exists():
        return [
            EvaluationResult(
                file=skills_dir,
                score=0.0,
                passed=False,
                pass_count=0,
                fail_count=len(EVALUATION_CHECKLIST),
                na_count=0,
                details=[],
            )
        ]

    skill_files = list(skills_dir.glob("*/SKILL.md"))

    for skill_file in skill_files:
        result = evaluate_skill_file(skill_file)
        # Override passed with custom threshold
        result = EvaluationResult(
            file=result.file,
            score=result.score,
            passed=result.score >= threshold,
            pass_count=result.pass_count,
            fail_count=result.fail_count,
            na_count=result.na_count,
            details=result.details,
        )
        results.append(result)

    return results


def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Quality Evaluator for SKILL.md Files.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="Evaluate a specific SKILL.md file",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Evaluate all SKILL.md files in a directory",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=70.0,
        help="Minimum score to pass (default: 70)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed evaluation results",
    )

    args = parser.parse_args()

    # Determine evaluation mode
    if args.path:
        # Single file evaluation
        result = evaluate_skill_file(args.path)
        passed = result.score >= args.threshold
        print_evaluation_result(result, args.verbose, args.threshold)
        sys.exit(0 if passed else 1)

    elif args.dir:
        # Directory evaluation
        results = evaluate_all_skills(args.dir, args.threshold)
        all_passed = all(r.passed for r in results)

        for result in results:
            print_evaluation_result(result, args.verbose, args.threshold)

        # Print summary
        print_summary(results, args.threshold)
        sys.exit(0 if all_passed else 1)

    else:
        # Default: evaluate .agents/skills/
        skills_dir = Path(".agents/skills")
        results = evaluate_all_skills(skills_dir, args.threshold)
        all_passed = all(r.passed for r in results)

        for result in results:
            print_evaluation_result(result, args.verbose, args.threshold)

        # Print summary
        print_summary(results, args.threshold)
        sys.exit(0 if all_passed else 1)


def print_evaluation_result(
    result: EvaluationResult, verbose: bool, threshold: float
) -> None:
    """Print evaluation results in a formatted way."""
    status = "✅ PASS" if result.passed else "❌ FAIL"
    print(f"\n{status}: {result.file}")
    print(f"  Score: {result.score:.1f}% (threshold: {threshold}%)")
    print(f"  Passed: {result.pass_count}, Failed: {result.fail_count}")

    if verbose and result.details:
        print("  Details:")
        for check_name, passed, message in result.details:
            check_status = "✓" if passed else "✗"
            print(f"    {check_status} {check_name}")
            if message and not passed:
                print(f"      → {message}")


def print_summary(results: list[EvaluationResult], threshold: float) -> None:
    """Print summary of all evaluations."""
    if not results:
        return

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    avg_score = sum(r.score for r in results) / total if total > 0 else 0.0

    print(f"\n{'=' * 60}")
    print(f"Summary: {passed}/{total} skills passed")
    print(f"Average score: {avg_score:.1f}%")
    print(f"Threshold: {threshold}%")

    if passed == total:
        print("✅ All skills meet quality threshold!")
    else:
        print(f"⚠️  {total - passed} skill(s) need improvement")


if __name__ == "__main__":
    main()
