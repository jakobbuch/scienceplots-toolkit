{ inputs, config, ... }:
{
  imports = [
    inputs.templates.devenvModules.python
    inputs.templates.devenvModules.latex
    inputs.templates.devenvModules.nix
    inputs.templates.devenvModules.markdown
    inputs.templates.devenvModules.git-hooks
    inputs.templates.devenvModules.nix-hooks
    inputs.templates.devenvModules.python-hooks
    inputs.templates.devenvModules.markdown-hooks
  ];

  # PyPI tokens decrypted by agenix (Home Manager)
  enterShell = ''
    export PYPI_TOKEN_FILE="/run/user/1000/agenix/pypi-token"
    export PYPI_TEST_TOKEN_FILE="/run/user/1000/agenix/pypi-test-token"
  '';
}
