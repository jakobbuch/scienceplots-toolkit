# Quiet greeting
set -g fish_greeting ""

# Helpful environment / safety defaults
set -gx PIP_DISABLE_PIP_VERSION_CHECK 1
set -gx UV_LINK_MODE copy
set -gx LESS '-R'

# Useful aliases
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias py='python'
alias pip='python -m pip'

# Shorter prompt (use builtin fish prompt if available)
# (leave default fish prompt unless user customises)

# Optional: auto-activate project .venv if a fish activation script is present
# This only runs for non-root users to avoid creating/changing root-owned host files unexpectedly.
if test -f .venv/bin/activate.fish -a (id -u) -ne 0
    # shellcheck disable=SC1091
    source .venv/bin/activate.fish
    echo "Activated project .venv"
end
