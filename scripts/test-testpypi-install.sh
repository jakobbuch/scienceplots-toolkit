#!/usr/bin/env bash
#
# test-testpypi-install.sh - Test installation from TestPyPI
#
# This script:
# 1. Creates a temporary virtual environment
# 2. Installs scienceplots-toolkit from TestPyPI
# 3. Runs basic functionality tests
# 4. Cleans up the test environment
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

die() {
    log_error "$1"
    exit 1
}

echo ""
echo "========================================"
echo "  TestPyPI Installation Test"
echo "========================================"
echo ""

# Create temporary directory
TEST_DIR=$(mktemp -d)
log_info "Created test directory: $TEST_DIR"

# Cleanup function
cleanup() {
    log_info "Cleaning up test directory..."
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Create virtual environment
log_info "Creating virtual environment..."
cd "$TEST_DIR"
uv venv .test-venv
source .test-venv/bin/activate

# Install from TestPyPI
log_info "Installing scienceplots-toolkit from TestPyPI..."
log_info "Using: --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple"

uv pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    scienceplots-toolkit || die "Installation failed!"

log_success "Package installed successfully!"

# Get installed version
VERSION=$(uv pip show scienceplots-toolkit | grep "Version:" | cut -d' ' -f2)
log_info "Installed version: $VERSION"

# Run tests
echo ""
log_info "Running functionality tests..."
echo ""

# Test 1: Import main module
log_info "Test 1: Importing main module..."
uv run python -c "
import scienceplots_toolkit
print(f'  Package: {scienceplots_toolkit.__name__}')
print(f'  Version: {scienceplots_toolkit.__version__}')
print(f'  Author: {scienceplots_toolkit.__author__}')
" || die "Failed to import main module"
log_success "Main module imports correctly"

# Test 2: Import style configuration
log_info "Test 2: Importing style configuration..."
uv run python -c "
from scienceplots_toolkit import configure_matplotlib_style, qual_cmap, DEFAULT_QUAL_CMAP_NAME
print(f'  Default colormap: {DEFAULT_QUAL_CMAP_NAME}')
cmap = qual_cmap()
print(f'  Colormap loaded: {cmap}')
" || die "Failed to import style configuration"
log_success "Style configuration imports correctly"

# Test 3: Import utilities
log_info "Test 3: Importing utilities..."
uv run python -c "
from scienceplots_toolkit.utils import save_plot, configure_24h_axis, add_stats_box, OUTPUT_DIR
print(f'  Output directory: {OUTPUT_DIR}')
print(f'  Functions available: save_plot, configure_24h_axis, add_stats_box')
" || die "Failed to import utilities"
log_success "Utilities import correctly"

# Test 4: Import analysis tools
log_info "Test 4: Importing analysis tools..."
uv run python -c "
from scienceplots_toolkit import plot_profile_with_quantiles, generate_profile_grid
print(f'  Functions available: plot_profile_with_quantiles, generate_profile_grid')
" || die "Failed to import analysis tools"
log_success "Analysis tools import correctly"

# Test 5: Create a simple plot
log_info "Test 5: Creating a simple plot..."
uv run python << 'PYTHON'
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from scienceplots_toolkit import configure_matplotlib_style, save_plot

# Configure style
configure_matplotlib_style(use_latex=False)

# Create simple plot
fig, ax = plt.subplots()
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
ax.plot(x, y, label='Test line')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_title('Test Plot')
ax.legend()

# Save to temp file
import tempfile
import os
with tempfile.TemporaryDirectory() as tmpdir:
    save_plot(fig, 'test_plot', output_dir=os.path.join(tmpdir, 'output'))
    print(f'  Plot saved successfully')

plt.close(fig)
PYTHON
log_success "Simple plot created successfully"

# Test 6: Test 24h axis configuration
log_info "Test 6: Testing 24h axis configuration..."
uv run python << 'PYTHON'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scienceplots_toolkit.utils import configure_24h_axis

fig, ax = plt.subplots()
configure_24h_axis(ax)

xticks = list(ax.get_xticks())
xlim = ax.get_xlim()

assert xticks == [0, 4, 8, 12, 16, 20, 24], f"Expected [0,4,8,12,16,20,24], got {xticks}"
assert xlim == (0, 24), f"Expected (0, 24), got {xlim}"

print(f'  X-ticks: {xticks}')
print(f'  X-limits: {xlim}')
print(f'  24h axis configured correctly')

plt.close(fig)
PYTHON
log_success "24h axis configuration works"

# Test 7: Test stats box
log_info "Test 7: Testing stats box annotation..."
uv run python << 'PYTHON'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scienceplots_toolkit.utils import add_stats_box

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
add_stats_box(ax, avg=5.2, peak=12.3, unit=r"\text{kW}")

# Check that text was added
assert len(ax.texts) == 1, f"Expected 1 text object, got {len(ax.texts)}"
text = ax.texts[0].get_text()
assert "Avg" in text, "Stats box should contain 'Avg'"
assert "Peak" in text, "Stats box should contain 'Peak'"
assert "5.2" in text, "Stats box should contain average value"
assert "12.3" in text, "Stats box should contain peak value"

print(f'  Stats box text: {text[:50]}...')
print(f'  Stats box annotation works correctly')

plt.close(fig)
PYTHON
log_success "Stats box annotation works"

# Test 8: Test profile grid generation
log_info "Test 8: Testing profile grid generation..."
uv run python << 'PYTHON'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scienceplots_toolkit import generate_profile_grid

# Test 2x2 grid
fig, axes = generate_profile_grid(n_rows=2, n_cols=2)
assert len(axes) == 4, f"Expected 4 axes, got {len(axes)}"
assert fig.get_figwidth() == 16, f"Expected width 16, got {fig.get_figwidth()}"
assert fig.get_figheight() == 10, f"Expected height 10, got {fig.get_figheight()}"

print(f'  Grid size: 2x2 (4 axes)')
print(f'  Figure size: {fig.get_figwidth()}x{fig.get_figheight()}')
print(f'  Profile grid generation works correctly')

plt.close(fig)
PYTHON
log_success "Profile grid generation works"

# Test 9: Test quantile plotting
log_info "Test 9: Testing quantile profile plotting..."
uv run python << 'PYTHON'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scienceplots_toolkit import plot_profile_with_quantiles

fig, ax = plt.subplots()
x = np.linspace(0, 24, 24)
mean = np.sin(x) + 5
q10 = mean * 0.9
q90 = mean * 1.1

plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Test Profile", color="C0")

# Check that line and fill were added
assert len(ax.lines) == 1, f"Expected 1 line, got {len(ax.lines)}"
assert len(ax.collections) == 1, f"Expected 1 fill, got {len(ax.collections)}"

line = ax.lines[0]
assert line.get_label() == "Test Profile", f"Expected label 'Test Profile', got '{line.get_label()}'"
assert line.get_linewidth() == 2.5, f"Expected linewidth 2.5, got {line.get_linewidth()}"

print(f'  Line label: {line.get_label()}')
print(f'  Line width: {line.get_linewidth()}')
print(f'  Fill alpha: {ax.collections[0].get_alpha()}')
print(f'  Quantile profile plotting works correctly')

plt.close(fig)
PYTHON
log_success "Quantile profile plotting works"

# All tests passed
echo ""
echo "========================================"
log_success "ALL TESTS PASSED!"
echo "========================================"
echo ""
log_info "Package version: $VERSION"
log_info "Test directory: $TEST_DIR (will be cleaned up)"
echo ""
echo "The package from TestPyPI is working correctly!"
echo ""
echo "Next steps:"
echo "1. Verify on TestPyPI: https://test.pypi.org/project/scienceplots-toolkit/"
echo "2. Upload to production PyPI: uv run twine upload --repository pypi --non-interactive dist/*"
echo ""
