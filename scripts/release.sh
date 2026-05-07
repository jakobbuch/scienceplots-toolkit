#!/usr/bin/env bash
#
# release.sh - Publish scienceplots-toolkit release
#
# This script:
# 1. Validates the release is ready
# 2. Builds distribution packages
# 3. Mirrors to GitHub (if configured)
# 4. Uploads to PyPI (TestPyPI or Production)
#
# Usage:
#   ./scripts/release.sh --help
#   ./scripts/release.sh --test          # Upload to TestPyPI
#   ./scripts/release.sh --production    # Upload to PyPI
#   ./scripts/release.sh --skip-github   # Skip GitHub mirror
#
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_NAME="scienceplots-toolkit"
GITHUB_REMOTE="github"
# TUWIEN_REMOTE="origin"  # Reserved for future use
PYPI_TEST="testpypi"
PYPI_PROD="pypi"

# Flags
SKIP_GITHUB=false
SKIP_PYPI=false
TEST_PYPI=false
DRY_RUN=false

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

die() {
    log_error "$1"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_PYPI=true
            shift
            ;;
        --production)
            TEST_PYPI=false
            shift
            ;;
        --skip-github)
            SKIP_GITHUB=true
            shift
            ;;
        --skip-pypi)
            SKIP_PYPI=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --test          Upload to TestPyPI (default)"
            echo "  --production    Upload to PyPI production"
            echo "  --skip-github   Skip GitHub mirror push"
            echo "  --skip-pypi     Skip PyPI upload"
            echo "  --dry-run       Show what would be done without executing"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            die "Unknown option: $1"
            ;;
    esac
done

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo ""
echo "========================================"
echo "  ${REPO_NAME} Release Script"
echo "========================================"
echo ""

# Step 1: Pre-flight checks
log_info "Running pre-flight checks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    die "Not in a git repository"
fi

# Check if working tree is clean
if [[ -n $(git status --porcelain) ]]; then
    die "Working tree is not clean. Commit or stash changes first."
fi

# Check if we have a version tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [[ -z "$LATEST_TAG" ]]; then
    die "No version tag found. Create a tag first: git tag -a v0.1.0 -m 'Release message'"
fi

log_success "Git repository is clean"
log_success "Latest tag: $LATEST_TAG"

# Check for required tools
for cmd in uv twine; do
    if ! command -v "$cmd" &> /dev/null; then
        die "Required command not found: $cmd"
    fi
done

log_success "Required tools available (uv, twine)"

# Check PyPI credentials if not skipping PyPI
if [[ "$SKIP_PYPI" == "false" ]]; then
    if [[ -z "${TWINE_USERNAME:-}" ]] && [[ ! -f ~/.pypirc ]]; then
        die "PyPI credentials not set. Set TWINE_USERNAME and TWINE_PASSWORD environment variables, or create ~/.pypirc"
    fi
    log_success "PyPI credentials configured"
fi

# Step 2: Build distribution
echo ""
log_info "Building distribution packages..."

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would run: uv build"
else
    # Clean previous builds
    rm -rf dist/ build/ -- *.egg-info/
    
    # Build
    if ! uv build; then
        die "Build failed"
    fi
fi

# Verify build artifacts
if [[ "$DRY_RUN" != "true" ]]; then
    if ! ls dist/*.tar.gz > /dev/null 2>&1 || ! ls dist/*.whl > /dev/null 2>&1; then
        die "Build did not produce expected artifacts"
    fi
    log_success "Distribution packages built successfully"
    ls -lh dist/
fi

# Step 3: Check package metadata
echo ""
log_info "Checking package metadata..."

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] Would run: twine check dist/*"
else
    if ! uv run twine check dist/*; then
        die "Package metadata check failed"
    fi
    log_success "Package metadata is valid"
fi

# Step 4: Mirror to GitHub (optional)
if [[ "$SKIP_GITHUB" == "true" ]]; then
    echo ""
    log_warning "Skipping GitHub mirror (as requested)"
else
    echo ""
    log_info "Mirroring to GitHub..."
    
    # Check if github remote exists
    if ! git remote | grep -q "^${GITHUB_REMOTE}$"; then
        log_warning "GitHub remote '$GITHUB_REMOTE' not configured"
        echo "To add GitHub remote, run:"
        echo "  git remote add $GITHUB_REMOTE git@github.com:jakobbuch/$REPO_NAME.git"
        echo ""
        read -p "Continue without GitHub mirror? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            die "Aborted by user"
        fi
        SKIP_GITHUB=true
    else
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "[DRY RUN] Would push to GitHub:"
            echo "  git push $GITHUB_REMOTE master"
            echo "  git push $GITHUB_REMOTE $LATEST_TAG"
        else
            log_info "Pushing master branch to GitHub..."
            if ! git push "$GITHUB_REMOTE" master; then
                die "Failed to push to GitHub"
            fi
            log_success "Master branch pushed"
            
            log_info "Pushing tag $LATEST_TAG to GitHub..."
            if ! git push "$GITHUB_REMOTE" "$LATEST_TAG"; then
                die "Failed to push tag to GitHub"
            fi
            log_success "Tag pushed to GitHub"
            
            echo ""
            log_success "GitHub mirror updated!"
            echo "  https://github.com/jakobbuch/$REPO_NAME"
        fi
    fi
fi

# Step 5: Upload to PyPI (optional)
if [[ "$SKIP_PYPI" == "true" ]]; then
    echo ""
    log_warning "Skipping PyPI upload (as requested)"
else
    echo ""
    if [[ "$TEST_PYPI" == "true" ]]; then
        log_info "Uploading to TestPyPI..."
        PYPI_REPO="$PYPI_TEST"
        PYPI_URL="https://test.pypi.org/project/$REPO_NAME"
    else
        log_info "Uploading to PyPI production..."
        PYPI_REPO="$PYPI_PROD"
        PYPI_URL="https://pypi.org/project/$REPO_NAME"
    fi
    
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Would run:"
        echo "  uv run twine upload --repository $PYPI_REPO dist/*"
    else
        log_info "Uploading to $PYPI_REPO..."
        if ! uv run twine upload --repository "$PYPI_REPO" dist/*; then
            die "Upload to $PYPI_REPO failed"
        fi
        
        log_success "Upload successful!"
        echo ""
        log_info "Verify your package at:"
        echo "  $PYPI_URL"
        echo ""
        log_info "Test installation with:"
        if [[ "$TEST_PYPI" == "true" ]]; then
            echo "  uv run pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple $REPO_NAME"
        else
            echo "  uv run pip install $REPO_NAME"
        fi
    fi
fi

# Summary
echo ""
echo "========================================"
echo "  Release Summary"
echo "========================================"
echo ""
log_success "Release $LATEST_TAG prepared successfully!"
echo ""
echo "Artifacts:"
if [[ "$DRY_RUN" != "true" ]]; then
    ls -lh dist/
fi
echo ""

if [[ "$SKIP_GITHUB" != "true" && "$DRY_RUN" != "true" ]]; then
    log_success "GitHub: https://github.com/jakobbuch/$REPO_NAME"
fi

if [[ "$SKIP_PYPI" != "true" && "$DRY_RUN" != "true" ]]; then
    if [[ "$TEST_PYPI" == "true" ]]; then
        log_success "TestPyPI: https://test.pypi.org/project/$REPO_NAME"
    else
        log_success "PyPI: https://pypi.org/project/$REPO_NAME"
    fi
fi

echo ""
log_info "Next steps:"
if [[ "$TEST_PYPI" == "true" && "$SKIP_PYPI" != "true" ]]; then
    echo "1. Test installation from TestPyPI (see command above)"
    echo "2. Verify package functionality"
    echo "3. Run this script with --production to upload to PyPI"
elif [[ "$SKIP_PYPI" == "true" ]]; then
    echo "1. Upload to PyPI manually or run this script without --skip-pypi"
else
    echo "1. Verify package on PyPI"
    echo "2. Test installation"
    echo "3. Announce release!"
fi

echo ""
log_success "Done!"
echo ""
