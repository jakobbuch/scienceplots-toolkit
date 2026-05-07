#!/usr/bin/env bash
#
# load-pypi-tokens.sh - Load PyPI tokens from agenix secrets
#
# Usage:
#   source scripts/load-pypi-tokens.sh
#   # or
#   . scripts/load-pypi-tokens.sh
#
# Then run:
#   ./scripts/release.sh --test
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if agenix secrets exist
if [[ -f "/run/user/1000/agenix/pypi-token" ]]; then
    export TWINE_USERNAME="__token__"
    export TWINE_PASSWORD=""; TWINE_PASSWORD=$(cat /run/user/1000/agenix/pypi-token)
    log_success "Production PyPI token loaded"
else
    log_warning "Production PyPI token not found at /run/user/1000/agenix/pypi-token"
fi

if [[ -f "/run/user/1000/agenix/pypi-test-token" ]]; then
    export TWINE_USERNAME="__token__"
    export TWINE_PASSWORD=""; TWINE_PASSWORD=$(cat /run/user/1000/agenix/pypi-test-token)
    log_success "TestPyPI token loaded"
else
    log_warning "TestPyPI token not found at /run/user/1000/agenix/pypi-test-token"
fi

# Verify tokens are loaded
if [[ -n "${TWINE_PASSWORD:-}" ]]; then
    echo ""
    log_success "PyPI credentials ready!"
    echo "  TWINE_USERNAME: ${TWINE_USERNAME}"
    echo "  TWINE_PASSWORD: ${TWINE_PASSWORD:0:10}... (${#TWINE_PASSWORD} chars)"
else
    echo ""
    log_error "No PyPI tokens loaded!"
    echo ""
    echo "Make sure you're in the devenv shell:"
    echo "  devenv shell"
    echo ""
    echo "Or check that agenix has decrypted the secrets."
    return 1
fi
