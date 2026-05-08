# Release Guide

This document describes the release workflow for scienceplots-toolkit.

## Repository Structure

- **Primary Repository**: TU Wien Phabricator (full development history)
- **Public GitHub**: Clean release history (single commit per release)
- **Distribution**: PyPI (package installation)

### History Strategy

This project uses a **dual-history approach**:

- **TU Wien Phabricator** (`origin`): Retains complete development history with all commits
- **GitHub** (`github`): Shows only clean release commits (single commit per version)

**Why?**

- Academic transparency: Full history preserved at TU Wien
- Professional appearance: GitHub shows polished releases
- Easy maintenance: Simple workflow, no complex branching

## Quick Start

### First-Time Setup

1. **Create GitHub Repository**
   - Visit: <https://github.com/new>
   - Name: `scienceplots-toolkit`
   - Visibility: Public
   - **Do NOT** initialize with README/.gitignore/license

2. **Add GitHub Remote**

   ```bash
   git remote add github git@github.com:jakobbuch/scienceplots-toolkit.git
   ```

3. **Configure PyPI Credentials**

   ```bash
   # Create API token at: https://pypi.org/manage/account/token/
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
   ```

### Release Workflow

#### Step 1: Prepare Release

```bash
# Ensure all changes are committed
git status

# Run tests
uv run pytest tests/ -v

# Run linting
uv run ruff check .
uv run ty check .

# Create annotated tag
git tag -a v0.1.0 -m "Release message"
```

#### Step 2: Run Release Script (TestPyPI)

```bash
# Test on TestPyPI first (RECOMMENDED)
./scripts/release.sh --test

# This will:
# ✓ Build distribution packages
# ✓ Push clean history to GitHub (if remote configured)
# ✓ Upload to TestPyPI

#### Step 3: Verify TestPyPI Release

```bash
# Test installation from TestPyPI
uv run pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  scienceplots-toolkit

# Verify it works
uv run python -c "
from scienceplots_toolkit import configure_matplotlib_style
print('✓ Installation successful!')
"
```

#### Step 4: Release to Production PyPI

```bash
# Upload to PyPI production
./scripts/release.sh --production

# Verify on PyPI
# Visit: https://pypi.org/project/scienceplots-toolkit/
```

---

## Scripts

### `scripts/release.sh`

Main release automation script.

**Usage:**

```bash
./scripts/release.sh [OPTIONS]
```

**Options:**

- `--test` - Upload to TestPyPI (default, recommended first)
- `--production` - Upload to PyPI production
- `--skip-github` - Skip GitHub push
- `--skip-pypi` - Skip PyPI upload (build only)
- `--dry-run` - Show what would be done without executing
- `--help` - Show help message

**What it does**:

1. ✅ Validates release is ready (clean git, has tag)
2. ✅ Builds distribution packages (`.tar.gz` and `.whl`)
3. ✅ Checks package metadata with `twine check`
4. ✅ Pushes clean history to GitHub (master + tag)
5. ✅ Uploads to PyPI (TestPyPI or Production)

**Note**: The script pushes your **clean release branch** to GitHub, not the full
development history. TU Wien Phabricator retains all commits.
**Example workflows:**

```bash
# Test everything first
./scripts/release.sh --test

# Production release (after TestPyPI verification)
./scripts/release.sh --production

# Build only, no upload
./scripts/release.sh --skip-pypi

# Upload to PyPI without GitHub mirror
./scripts/release.sh --production --skip-github

# Dry run to see what would happen
./scripts/release.sh --dry-run
```

### `scripts/mirror-to-github.sh`

Simple script to mirror to GitHub only (no PyPI upload).

**Usage:**

```bash
./scripts/mirror-to-github.sh
```

**What it does:**

- Pushes `master` branch to GitHub
- Pushes latest tag to GitHub

**When to use:**

- You want to update GitHub mirror without PyPI upload
- Manual release workflow
- Debugging mirror issues

---

## Manual Release Steps

If you prefer not to use the scripts, here are the manual commands:

### 1. Build Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build
uv build

# Verify
ls -lh dist/
# Should have:
# - scienceplots_toolkit-0.1.0.tar.gz
# - scienceplots_toolkit-0.1.0-py3-none-any.whl
```

### 2. Check Package

```bash
uv run twine check dist/*
```

### 3. Mirror to GitHub

```bash
git push github master
git push github v0.1.0
```

### 4. Upload to TestPyPI

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TESTPYPI_TOKEN

uv run twine upload --repository testpypi dist/*
```

### 5. Upload to PyPI

```bash
export TWINE_PASSWORD=pypi-YOUR_PRODUCTION_TOKEN

uv run twine upload dist/*
```

---

## PyPI Token Setup

### TestPyPI Verification

1. Create account: <https://test.pypi.org/account/register/>
2. Create token: <https://test.pypi.org/manage/account/token/>
3. Set environment variable:

   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YOUR_TESTPYPI_TOKEN
   ```

### PyPI Production

1. Create account: <https://pypi.org/account/register/>
2. Create token: <https://pypi.org/manage/account/token/>
3. Set environment variable:

   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YOUR_PRODUCTION_TOKEN
   ```

### Alternative: `.pypirc` File

Create `~/.pypirc`:

```ini
[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN
```

Then you don't need to set environment variables.

---

## Version Management

### Semantic Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a New Version

```bash
# For bug fixes (0.1.0 -> 0.1.1)
git tag -a v0.1.1 -m "Bug fix release"

# For new features (0.1.0 -> 0.2.0)
git tag -a v0.2.0 -m "New features release"

# For major changes (0.1.0 -> 1.0.0)
git tag -a v1.0.0 -m "Major release"

# Push tag
git push origin v0.1.1
git push github v0.1.1
```

### Version Source

Version is automatically determined from git tags using `hatch-vcs`.

To check current version:

```bash
git describe --tags
# or
uv run python -c "import scienceplots_toolkit; print(scienceplots_toolkit.__version__)"
```

---

## Future Releases

For next releases (v0.2.0, v1.0.0, etc.):

   ```bash
   git checkout --orphan release-v0.2.0
   git reset
   git add -A
   git commit -m "release: v0.2.0"
   git tag -a v0.2.0 -m "Version 0.2.0"
   ./scripts/release.sh --production
   ```

## GitHub Releases

After pushing to GitHub, create a release page:

### Option 1: GitHub CLI

```bash
gh release create v0.1.0 \
  --title "scienceplots-toolkit v0.1.0" \
  --notes-file CHANGELOG.md \
  --verify-tag
```

### Option 2: GitHub Web Interface

1. Visit: <https://github.com/jakobbuch/scienceplots-toolkit/releases/new>
2. Select tag: `v0.1.0`
3. Title: `scienceplots-toolkit v0.1.0`
4. Copy release notes from `CHANGELOG.md`
5. Click "Publish release"

---

## Troubleshooting

### Build Fails

```bash
# Clean everything
rm -rf dist/ build/ *.egg-info/
uv cache clean

# Rebuild
uv build
```

### Tag Not Found

```bash
# List tags
git tag -l

# Create tag if missing
git tag -a v0.1.0 -m "Release message"
```

### PyPI Upload Fails

```bash
# Check credentials
echo $TWINE_USERNAME  # Should be __token__

# Verify .pypirc if using file
cat ~/.pypirc

# Check token is valid
# Try creating a new token at PyPI
```

### GitHub Push Fails

```bash
# Verify remote
git remote -v

# Check SSH key
ssh -T git@github.com

# Re-add remote if needed
git remote set-url github git@github.com:jakobbuch/scienceplots-toolkit.git
```

---

## Checklist

### Before Release

- [ ] All tests passing: `uv run pytest tests/ -v`
- [ ] Linting clean: `uv run ruff check .`
- [ ] Type checking clean: `uv run ty check .`
- [ ] CHANGELOG.md updated
- [ ] Git working tree clean
- [ ] Version tag created

### Post-Release

- [ ] Upload to PyPI successful
- [ ] Package visible on PyPI
- [ ] Installation from PyPI works
- [ ] Basic functionality tested

### Production PyPI

- [ ] TestPyPI verification complete
- [ ] Upload to PyPI successful
- [ ] Package visible on PyPI
- [ ] Installation from PyPI works
- [ ] GitHub release page created
- [ ] Announcement sent (if applicable)

---

## Resources

- [PyPA Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [twine documentation](https://twine.readthedocs.io/)
- [hatch-vcs documentation](https://github.com/ofek/hatch-vcs)

---

**Last Updated**: 2026-05-07  
**Maintainer**: Jakob Buchmeier <jakob.buchmeier@tuwien.ac.at>
