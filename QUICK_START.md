# Quick Start: Publish to GitHub & PyPI

## Current State

✅ **Clean history created** - Single commit ready for GitHub  
✅ **Tag v0.1.0 created** - Release tag ready  
✅ **Tests passing** - 36/36 tests  
✅ **Package builds** - Ready for PyPI  

---

## Step 1: Create GitHub Repository

1. Visit: <https://github.com/new>
2. **Repository name:** `scienceplots-toolkit`
3. **Description:** "Publication-quality Matplotlib plotting utilities with SciencePlots styles and LaTeX typesetting"
4. **Visibility:** Public ✓
5. **DO NOT** check:
   - ❌ "Add a README file"
   - ❌ "Add .gitignore"
   - ❌ "Choose a license"
6. Click **"Create repository"**

---

## Step 2: Add GitHub Remote & Push

```bash
cd /home/jakobb/Documents/syncthing/Arbeit/ToolsGeneral/Scienceplots_with_Python_for_Latex

# Add GitHub remote
git remote add github git@github.com:jakobbuch/scienceplots-toolkit.git

# Verify remotes
git remote -v
# Should show:
# origin    ssh://vcs@phabricator.ict.tuwien.ac.at/... (TU Wien)
# github    git@github.com:jakobbuch/scienceplots-toolkit.git (GitHub)

# Push to GitHub (clean history: 1 commit + tag)
git push github master
git push github v0.1.0

# Verify on GitHub
# Visit: https://github.com/jakobbuch/scienceplots-toolkit
```

**What gets pushed:**

- ✅ 1 clean commit: "Initial release: scienceplots-toolkit v0.1.0"
- ✅ 1 tag: v0.1.0
- ❌ NOT the 18 development commits (those stay on TU Wien)

---

## Step 3: Set Up PyPI Credentials

### TestPyPI (for testing)

1. Create account: <https://test.pypi.org/account/register/>
2. Create token: <https://test.pypi.org/manage/account/token/>
3. Set environment variables:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TESTPYPI_TOKEN
```

### PyPI Production (for real release)

1. Create account: <https://pypi.org/account/register/>
2. Create token: <https://pypi.org/manage/account/token/>
3. Set environment variables:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_PRODUCTION_TOKEN
```

---

## Step 4: Test on TestPyPI (RECOMMENDED)

```bash
# Run release script (TestPyPI)
./scripts/release.sh --test

# This will:
# ✓ Build distribution packages
# ✓ Push to GitHub (if remote configured)
# ✓ Upload to TestPyPI
```

**Verify on TestPyPI:**

- Visit: <https://test.pypi.org/project/scienceplots-toolkit/>
- Test installation:

  ```bash
  uv run pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    scienceplots-toolkit
  
  uv run python -c "from scienceplots_toolkit import configure_matplotlib_style; print('✓ Works!')"
  ```

---

## Step 5: Release to PyPI Production

```bash
# Set production credentials
export TWINE_PASSWORD=pypi-YOUR_PRODUCTION_TOKEN

# Run release script (PyPI production)
./scripts/release.sh --production
```

**Verify on PyPI:**

- Visit: <https://pypi.org/project/scienceplots-toolkit/>
- Test installation:

  ```bash
  uv run pip install scienceplots-toolkit
  ```

---

## Step 6: Create GitHub Release (Optional but Recommended)

```bash
# Using GitHub CLI (if installed)
gh release create v0.1.0 \
  --title "scienceplots-toolkit v0.1.0" \
  --notes "Initial release with comprehensive test suite and release automation" \
  --verify-tag

# Or use web interface:
# Visit: https://github.com/jakobbuch/scienceplots-toolkit/releases/new
# - Select tag: v0.1.0
# - Title: scienceplots-toolkit v0.1.0
# - Copy notes from CHANGELOG.md
# - Click "Publish release"
```

---

## Summary

After completing all steps:

- ✅ **TU Wien Phabricator**: Full development history (18 commits)
- ✅ **GitHub**: Clean release (1 commit + tag)
- ✅ **PyPI**: Package available for installation
- ✅ **Users can install**: `pip install scienceplots-toolkit`

---

## Future Releases

For next releases (v0.2.0, v1.0.0, etc.):

```bash
# 1. Make changes, commit to TU Wien
git add -A && git commit -m "feat: new feature"

# 2. Create clean release branch when ready
git checkout --orphan release-v0.2.0
git reset
git add -A
git commit -m "release: v0.2.0"

# 3. Tag and push
git tag -a v0.2.0 -m "Version 0.2.0"
./scripts/release.sh --production
```

---

**Questions?** See [RELEASE.md](RELEASE.md) for complete documentation.
