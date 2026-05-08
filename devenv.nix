{ inputs, ... }:
{
  imports = [
    inputs.templates.devenvModules.python
    inputs.templates.devenvModules.latex
    inputs.templates.devenvModules.nix
    inputs.templates.devenvModules.markdown
    inputs.devenv-nix-environments.devenvModules.local-hooks
  ];

  # PyPI tokens decrypted by agenix (Home Manager)
  enterShell = ''
    export PYPI_TOKEN_FILE="/run/user/1000/agenix/pypi-token"
    export PYPI_TEST_TOKEN_FILE="/run/user/1000/agenix/pypi-test-token"
  '';

  # Pre-commit hooks: pytest for testing, pytest-visual for visual regression
  git-hooks.hooks = {
    pytest = {
      enable = true;
      name = "pytest";
      entry = "uv run pytest tests/ -v";
      language = "system";
      pass_filenames = false;
      stages = ["commit"];
    };
    pytest-visual = {
      enable = true;
      name = "pytest-visual";
      entry = "uv run pytest tests/test_visual_baselines.py -v";
      language = "system";
      pass_filenames = false;
      stages = ["pre-push"];
    };
  };
}
