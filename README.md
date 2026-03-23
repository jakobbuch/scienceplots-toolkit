# SciencePlots + LaTeX example

This example shows how to generate plots using the SciencePlots Matplotlib styles
with LaTeX rendering. By default, LaTeX rendering is done using the Matplotlib
interpreter, meaning it can run with just python installed provided in the
pyproject.toml for uv or requirements.txt for pip. For more advanced LaTeX
rendering for publications, you can run the scripts inside a provided Docker
container and write the results to an `output` directory.

## Project layout

- `example.py`: Generates standard scientific plots (line, scatter, heatmap,
  annotated profiles) using the custom style.
- `example_energy.py`: Generates energy-specific plots (24h load profiles,
  seasonal grids) demonstrating advanced features like quantile shading and
  statistical annotation boxes.
- `MatplotlibStyle.py`: Custom Matplotlib stylesheet and configuration.
- `plotting_utils.py`: Standardized utilities for saving plots, configuring
  24h time axes, and adding statistical annotations.
- `profile_analysis.py`: Specialized functions for time-series visualization,
  including quantile shading and grid generation.
- `.agents/`: Modular AI agent instructions and skills for tool-agnostic
  development (Copilot, Claude, Gemini, etc.).
- `Dockerfile`: Image that includes LaTeX, fonts, and an isolated venv with
  `uv`.
- `entrypoint.sh`: Runs `uv sync` (if requirements exist) and drops you into a
  fish shell.

## AI Agent Workflow

This repository uses a tool-agnostic agent workflow to ensure high-quality
code and consistent scientific visualization across different AI assistants
(GitHub Copilot, Claude Code, Gemini CLI, etc.).

- **Mandates**: Core project rules are defined in `AGENTS.md`.
- **Instructions**: Specific guidelines for coding, plotting, and data handling
  reside in `.agents/instructions/`.
- **Skills**: High-level task workflows (e.g., creating a new visualization)
  are defined in `.agents/skills/`.

AI agents are expected to read these files to align with the project's
standards.

## Plotting Standards

This project follows several core plotting standards:

1. **Object-Oriented API**: Always use `fig, ax = plt.subplots()` instead of
   `plt.plot()`.
2. **24-Hour Time Axes**: Use `plotting_utils.configure_24h_axis(ax)` to
   standardize horizontal axes for daily profiles (0-24h, 4h ticks).
3. **Statistical Annotations**: Use `plotting_utils.add_stats_box(ax, ...)` to
   display Average and Peak values in a consistent, readable format.
4. **No Figure-Level Titles in Grids**: In multi-panel plots, use individual
   subplot titles or a shared figure-level legend instead of `suptitle()`.
5. **LaTeX for Units**: Always use LaTeX math mode for units (e.g.,
   `r"Power (kW)"` or `r"Energy (kWh)"`) to ensure professional typesetting.
6. **Quantile Shading**: Use `profile_analysis.plot_profile_with_quantiles` for
   visualizing uncertainty (e.g., 10th-90th percentiles).

## Local Usage

You can run the scripts locally if you have `uv` installed.

```bash
# Install dependencies locally
uv sync

# Run the standard example
uv run example.py

# Run the energy-specific example
uv run example_energy.py

# Run with LaTeX (requires local LaTeX installation)
uv run example.py --latex
```

All scripts output to the `output` directory.

## Container Usage

### How the image behaves

- The container installs the `uv` tool. When you mount your project into the
  container at `/app`, uv will create and use a project-local virtual
  environment at `/app/.venv`.
- On startup the entry point:
  - If `pyproject.toml` is present, compiles it to `requirements.txt` (for
    reproducible pins).
  - If `requirements.txt` is present, runs `uv sync --link-mode=copy` to
    create the `.venv`.
  - Finally drops you into a fish login shell for interactive development.

### Build & Run

1. Build the image, first build will take a while as it downloads latex:

   ```bash
   docker build -t scienceplots .
   ```

2. Run the container; mount your project to `/app` (choose the command for your
   shell):

   - Linux/macOS/Git Bash:

     ```bash
     docker run -it --rm -v "$PWD":/app scienceplots
     ```

   - PowerShell:

     ```powershell
     docker run -it --rm -v "${PWD}:/app" scienceplots
     ```

   - cmd.exe:

     ```cmd
     docker run -it --rm -v "%cd%":/app scienceplots
     ```

3. This enters you into a shell, here you can run the scripts with:

   ```bash
   # Run non-LaTeX examples
   uv run example.py

   # Run with LaTeX enabled (pass through args to the script)
   uv run example.py -- --latex
   ```

4. Develop you own scripts, install packages with `uv add <package>`, and they
   will be installed into the project-local venv at `.venv`.

## uv commands (add, sync, remove)

- `uv add <package>`
  - Installs a package into the project-local virtual env (.venv) and records
    it for the project environment. Example:

    ```bash
    uv add numpy
    ```

- `uv sync [--link-mode=copy]`
  - Ensures the project venv matches the pinned requirements (creates .venv if
    missing). The container entry point uses:

    ```bash
    uv sync --link-mode=copy
    ```

- `uv remove <package>`
  - Removes a package from the project venv. Example:

    ```bash
    uv remove numpy
    ```

## Developer tooling: ruff, ty

- A basic ruff config has been added to the project root.
- To install tooling into the project venv using uv:

  ```bash
  # install tooling into the project venv using uv
  uv add ruff ty
  ```

### Quick commands

- Format & lint with ruff:

  ```bash
  uv run ruff format .
  uv run ruff check .
  ```

- Run ty type checks:

  ```bash
  uv run ty check .
  ```

## Notes

- If you maintain dependencies in `pyproject.toml` and want pinned requirements
  for `uv`, you can generate `requirements.txt` locally with:

  ```bash
  uv pip compile pyproject.toml -o requirements.txt
  ```

- The entry point will perform the compile step automatically when
  `pyproject.toml` exists; otherwise it will proceed if `requirements.txt` is
  present.

## Usage in other projects

You can copy `MatplotlibStyle.py` to your project to use the standardized
plotting style. Additionally, you can include the `AGENTS.md` and `.agents/`
folder in your project root to provide context-aware coding guidelines for AI
agents (GitHub Copilot, Claude Code, Gemini CLI, etc.). This ensures that
generated code follows the project's style, path handling, and plotting
standards.

## Contact

Maintained by Jakob Buchmeier ([jakob.buchmeier@tuwien.ac.at](mailto:jakob.buchmeier@tuwien.ac.at))
