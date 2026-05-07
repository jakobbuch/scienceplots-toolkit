# AI Agent Mandates

As an AI agent in this repository, you MUST follow these core mandates at all
costs. This project requires high precision in data handling and professional
scientific visualization.

## Core Mandates

- **Path Handling**: ALWAYS use `pathlib.Path` for all path operations. Scripts
  MUST work from any execution directory. NEVER use `os.chdir()`,
  `sys.path.insert()`, or string concatenation for paths.
- **Plotting Excellence**: Adhere strictly to the Matplotlib Object-Oriented
  API and the project's custom styling. Professional LaTeX typesetting is
  mandatory for all labels.
- **Reliability**: All findings MUST be reproducible via permanent, executable
  scripts.

## Task-Specific Instructions

**Mandatory Reading**: When working on tasks involving the areas below, you
MUST read the corresponding instruction file to ensure compliance.

- **Coding & Style**: [.agents/instructions/coding-standards.instructions.md](.agents/instructions/coding-standards.instructions.md)
  (Load for `**/*.py`)
- **Workflow & Git**: [.agents/instructions/workflow.instructions.md](.agents/instructions/workflow.instructions.md)
  (Load for all tasks)
- **Documentation**: [.agents/instructions/documentation.instructions.md](.agents/instructions/documentation.instructions.md)
  (Load for `**/*.{py,md}`)
- **Plotting**: [.agents/instructions/plotting.instructions.md](.agents/instructions/plotting.instructions.md)
  (Load for `**/*.py`)
- **Data Handling**: [.agents/instructions/data-handling.instructions.md](.agents/instructions/data-handling.instructions.md)
  (Load for `**/*.py`)

## AI Agent Customization

This repository is designed to be tool-agnostic, supporting GitHub Copilot,
Claude Code, Gemini CLI, etc.

- **Skills**: Actively use project-specific skills like
  [SciencePlots Visualization](.agents/skills/scienceplots-viz.md).

## Project Context

Refer to these files for foundational information:

- [README.md](README.md): Project overview and usage.
- [src/scienceplots_toolkit/](src/scienceplots_toolkit/): Main package source code.
  - `style.py`: Matplotlib style configuration.
  - `utils.py`: Common plotting helpers.
  - `analysis.py`: Advanced analysis tools.
- [examples/](examples/): Example scripts demonstrating package usage.
- [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md): PyPI publication workflow.
- [CHANGELOG.md](CHANGELOG.md): Version history and changes.
