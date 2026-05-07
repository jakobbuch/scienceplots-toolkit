# Publication Plan: scienceplots-toolkit v0.1.0

This document outlines the complete workflow for publishing scienceplots-toolkit to PyPI.

---

## Pre-Publication Checklist

### 1. Package Structure Verification

- [x] **src/ layout** - Package uses proper isolation
- [x] **MIT License** - Included with SciencePlots attribution
- [x] **pyproject.toml** - PEP 621 compliant with all metadata
- [x] **README.md** - Comprehensive documentation
- [x] **Examples** - Working examples with updated imports
- [x] **Clean API** - `__init__.py` exports with `__all__`

### 2. Metadata Verification

- [x] Package name: `scienceplots-toolkit`
- [x] Version: Dynamic (via `hatch-vcs` from git tags)
- [x] Python requirement: `>=3.13`
- [x] License: `MIT`
- [x] Authors: Jakob Buchmeier <jakob.buchmeier@tuwien.ac.at>
- [x] Classifiers: Development Status, Intended Audience, Topics, Python versions
- [x] URLs: Homepage, Bug Tracker, Source, Changelog

### 3. Dependencies

**Runtime:**

- `cmap>=0.6.2`
- `matplotlib>=3.10.7`
- `scienceplots>=2.1.1`

**Development:**

- `ruff>=0.4`
- `ty`
- `pre-commit>=4.3.0`
- `pytest>=8`
- `pytest-cov>=4`
- `numpy>=1.24`

### 4. Build System

- [x] Build backend: `hatchling`
- [x] Version source: `hatch-vcs` (git tags)
- [x] Package discovery: `src/scienceplots_toolkit`

---

## Publication Workflow

### Phase 1: Final Verification (Local)

#### Step 1.1: Clean Working Directory

```bash
# Remove build artifacts
rm -rf dist/ build/ *.egg-info/
rm -rf __pycache__/ .pytest_cache/
rm -rf null/

# Verify clean state
git status
```

#### Step 1.2: Update .gitignore

```bash
# Ensure null/ is in .gitignore (already done)
# Ensure dist/ is in .gitignore (already done)
```

#### Step 1.3: Run Final Tests

```bash
# In devenv shell
devenv shell

# Lint and format
uv run ruff check src/ examples/
uv run ruff format src/ examples/
uv run ty check src/

# Run examples to verify functionality
uv run python examples/example_basic.py
uv run python examples/example_energy.py

# Verify output
ls -lh output/
```

#### Step 1.4: Build Package

```bash
# Build source distribution and wheel
uv build

# Verify build artifacts
ls -lh dist/
# Should have:
# - scienceplots_toolkit-*.tar.gz (source distribution)
# - scienceplots_toolkit-*-py3-none-any.whl (wheel)

# Check package contents
unzip -l dist/*.whl | head -20
tar -tzf dist/*.tar.gz | head -20
```

#### Step 1.5: Verify Package Metadata

```bash
# Check metadata
uv run python -m pip install dist/*.whl --dry-run

# Or use twine to check
uv add --dev twine
uv run twine check dist/*
```

#### Step 1.6: Test Installation

```bash
# Create a fresh virtual environment
uv venv .test-env
source .test-env/bin/activate

# Install from wheel
pip install dist/scienceplots_toolkit-*.whl

# Test imports
python -c "
from scienceplots_toolkit import (
    configure_matplotlib_style,
    save_plot,
    generate_profile_grid,
    plot_profile_with_quantiles,
)
print('All imports successful!')
print(f'Version: {__import__(\"scienceplots_toolkit\").__version__}')
"

# Cleanup
deactivate
rm -rf .test-env
```

---

### Phase 2: GitHub Preparation

#### Step 2.1: Commit Final Changes

```bash
# Add cleanup changes
git add .gitignore
git commit -m "chore: add null/ to gitignore and cleanup build artifacts"
```

#### Step 2.2: Push to GitHub

```bash
# Push all commits
git push origin master

# Verify on GitHub
# Visit: https://github.com/jakobbuch/scienceplots-toolkit
```

#### Step 2.3: Create Release Tag

```bash
# Create annotated tag for v0.1.0
git tag -a v0.1.0 -m "Initial release

First public release of scienceplots-toolkit with:
- Publication-quality Matplotlib styling
- LaTeX typesetting support
- 24h profile utilities
- Quantile shading
- Multi-panel grid generation"

# Push tag
git push origin v0.1.0

# Verify tag
git tag -l
git show v0.1.0
```

#### Step 2.4: Create GitHub Release (Optional but Recommended)

```bash
# Using GitHub CLI
gh release create v0.1.0 \
  --title "scienceplots-toolkit v0.1.0" \
  --notes "Initial release of scienceplots-toolkit

## Features
- Pre-configured SciencePlots styles
- LaTeX typesetting for mathematical expressions
- 24-hour time axis utilities
- Statistical annotations
- Quantile shading for uncertainty visualization
- Multi-panel grid generation

## Installation
\`\`\`bash
pip install scienceplots-toolkit
\`\`\`

## Quick Start
\`\`\`python
from scienceplots_toolkit import configure_matplotlib_style, save_plot
configure_matplotlib_style(use_latex=True)
# ... create your plots ...
save_plot(fig, 'my_plot')
\`\`\`

## Acknowledgments
Built upon the excellent SciencePlots library by John Garrett." \
  --verify-tag

# Or create manually at:
# https://github.com/jakobbuch/scienceplots-toolkit/releases/new
```

---

### Phase 3: PyPI Publication

#### Step 3.1: PyPI Account Setup (First Time Only)

```bash
# Create accounts if you don't have them
# 1. PyPI: https://pypi.org/account/register/
# 2. TestPyPI: https://test.pypi.org/account/register/

# Install twine (if not already installed)
uv add --dev twine

# Generate API token from PyPI
# Visit: https://pypi.org/manage/account/token/
# Create API token with scope: "Entire account"

# Store credentials (use __token__ as username)
uv run twine upload --repository testpypi dist/*
# When prompted:
# Username: __token__
# Password: <your-pypi-token>
```

#### Step 3.2: Test Upload to TestPyPI

```bash
# Always test on TestPyPI first!
uv run twine upload --repository testpypi dist/*

# Verify on TestPyPI
# Visit: https://test.pypi.org/project/scienceplots-toolkit/

# Test installation from TestPyPI
uv run pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  scienceplots-toolkit
```

#### Step 3.3: Upload to PyPI

```bash
# Once TestPyPI verification passes, upload to real PyPI
uv run twine upload dist/*

# Or using uv directly
uv publish

# Verify on PyPI
# Visit: https://pypi.org/project/scienceplots-toolkit/
```

#### Step 3.4: Verify PyPI Installation

```bash
# Fresh installation test
uv run pip install scienceplots-toolkit

# Test in Python
python -c "
import scienceplots_toolkit
print(f'Version: {scienceplots_toolkit.__version__}')
print(f'Author: {scienceplots_toolkit.__author__}')
print(f'Available: {scienceplots_toolkit.__all__}')
"
```

---

### Phase 4: Post-Publication

#### Step 4.1: Update Documentation

- [ ] Add PyPI badge to README.md
- [ ] Add installation instructions via pip
- [ ] Update CHANGELOG.md with release notes
- [ ] Pin documentation version if using ReadTheDocs

#### Step 4.2: Announce Release

- [ ] Share on relevant mailing lists
- [ ] Post on Twitter/LinkedIn
- [ ] Share in Python/Scientific computing communities
- [ ] Update personal website/CV

#### Step 4.3: Monitor

- [ ] Watch for issues on GitHub
- [ ] Monitor PyPI downloads (<https://pepy.tech/project/scienceplots-toolkit>)
- [ ] Check for user feedback

---

## 🔧 Troubleshooting

### Issue: Build Fails

```bash
# Clean everything
rm -rf dist/ build/ *.egg-info/ __pycache__/
uv cache clean

# Rebuild
uv build

# Check for errors in output
```

### Issue: Version Not Updating

```bash
# Ensure git tag is annotated
git tag -a v0.1.0 -m "Release message"

# Verify tag
git describe --tags

# Rebuild
uv build
```

### Issue: Twine Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Or use environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-<your-token>

# Retry upload
uv run twine upload dist/*
```

### Issue: Package Name Already Taken

```bash
# Check availability
uv run pip search scienceplots-toolkit  # (deprecated but still works sometimes)

# Or visit PyPI directly
# https://pypi.org/search/?q=scienceplots-toolkit

# If taken, choose alternative:
# - scienceplots-toolkit
# - scienceplots-utils
# - scienceplots-extra
```

---

## Version Management

### Current Setup

- **Dynamic versioning** via `hatch-vcs`
- Version derived from git tags
- Format: `0.1.0`, `0.1.1`, `1.0.0`, etc.

### Creating New Versions

```bash
# For bug fixes (0.1.0 -> 0.1.1)
git tag -a v0.1.1 -m "Bug fix release"

# For new features (0.1.0 -> 0.2.0)
git tag -a v0.2.0 -m "New features release"

# For major changes (0.1.0 -> 1.0.0)
git tag -a v1.0.0 -m "Major release"

# Push tag
git push origin v0.1.1
```

### Version Number Guidelines

- **MAJOR.MINOR.PATCH** (Semantic Versioning)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

---

## 📝 Maintenance Checklist

### After Each Release

- [ ] Update CHANGELOG.md
- [ ] Create GitHub release notes
- [ ] Tag release on GitHub
- [ ] Upload to PyPI
- [ ] Verify installation
- [ ] Update documentation

### Ongoing Maintenance

- [ ] Monitor GitHub issues
- [ ] Review pull requests
- [ ] Update dependencies
- [ ] Check Python version compatibility
- [ ] Respond to user feedback

---

## Quick Reference Commands

```bash
# Build package
uv build

# Check package
uv run twine check dist/*

# Test upload
uv run twine upload --repository testpypi dist/*

# Production upload
uv run twine upload dist/*
# or
uv publish

# Create release tag
git tag -a v0.1.0 -m "Release message"
git push origin v0.1.0

# Install from PyPI
pip install scienceplots-toolkit

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple scienceplots-toolkit
```

---

## 📚 Resources

- [PyPA Packaging Guide](https://packaging.python.org/)
- [PyPI Upload Documentation](https://pypi.org/help/#file-name-reuse)
- [Semantic Versioning](https://semver.org/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [PEP 639 - License Expression](https://peps.python.org/pep-0639/)
- [hatch-vcs Documentation](https://github.com/ofek/hatch-vcs)

---

**Last Updated**: May 7, 2026  
**Package**: scienceplots-toolkit v0.1.0  
**Maintainer**: Jakob Buchmeier <jakob.buchmeier@tuwien.ac.at>
