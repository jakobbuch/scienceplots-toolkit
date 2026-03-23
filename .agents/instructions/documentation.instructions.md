---
description: "Documentation standards and Markdown formatting rules."
applyTo: "**/*.{py,md}"
---

# Documentation Standards

Follow these rules for all documentation and comments in this repository.

## Python Documentation

- Write docstrings and comments in British English (e.g., 'analyse' instead of
  'analyze')
- Write error messages and print output in English
- Use Google-style docstrings:

  ```python
  def example(param1: str, param2: int) -> bool:
      """Brief description of function.

      Args:
          param1: Description of param1.
          param2: Description of param2.

      Returns:
          Description of return value.
      """
  ```

## Markdown Rules

- Markdown must pass `markdownlint` rules with strict adherence:
  - **Line length**: Maximum 80 characters (MD013). Wrap text to fit.
  - **Spacing**: Always surround headings, lists, and code blocks with blank
    lines (MD022, MD031, MD032).
  - **Lists**: Use consistent indentation.
