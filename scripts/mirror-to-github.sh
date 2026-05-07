#!/usr/bin/env bash
#
# mirror-to-github.sh - Push clean release to GitHub
#
# Pushes current master branch and latest tag to GitHub remote.
# This is designed for the "clean history" workflow where:
#   - TU Wien Phabricator: Full development history
#   - GitHub: Clean single-commit release
#
# Usage:
#   ./scripts/mirror-to-github.sh
#
# Note: Ensure you're on the clean release branch before running!
set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
# RED='\033[0;31m'  # Reserved for future use
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

die() {
    log_error "$1"
    exit 1
}

GITHUB_REMOTE="github"
REPO_NAME="scienceplots-toolkit"

echo ""
echo "========================================"
echo "  Mirror to GitHub"
echo "========================================"
echo ""

# Check if github remote exists
if ! git remote | grep -q "^${GITHUB_REMOTE}$"; then
    log_warning "GitHub remote '$GITHUB_REMOTE' not configured"
    echo ""
    echo "To add GitHub remote, run:"
    echo "  git remote add $GITHUB_REMOTE git@github.com:jakobbuch/$REPO_NAME.git"
    echo ""
    echo "Then create the repository on GitHub:"
    echo "  https://github.com/new"
    echo ""
    exit 1
fi

# Get latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [[ -z "$LATEST_TAG" ]]; then
    die "No version tag found. Create a tag first."
fi

log_info "Latest tag: $LATEST_TAG"
echo ""

# Push master branch
log_info "Pushing master branch to GitHub..."
if git push "$GITHUB_REMOTE" master; then
    log_success "Master branch pushed"
else
    die "Failed to push master branch"
fi

# Push latest tag
log_info "Pushing tag $LATEST_TAG to GitHub..."
if git push "$GITHUB_REMOTE" "$LATEST_TAG"; then
    log_success "Tag pushed"
else
    die "Failed to push tag"
fi

echo ""
log_success "GitHub release published!"
echo ""
echo "View on GitHub:"
echo "  Repository: https://github.com/jakobbuch/$REPO_NAME"
echo "  Release:    https://github.com/jakobbuch/$REPO_NAME/releases/tag/$LATEST_TAG"
echo ""
echo "Note: GitHub shows clean history (1 commit)."
echo "      TU Wien Phabricator retains full development history."
echo ""
