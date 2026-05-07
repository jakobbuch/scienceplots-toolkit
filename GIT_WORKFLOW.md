# Git Workflow Guide

## Overview

This repository uses a **dual-remote, dual-branch workflow** to maintain:

- **Full development history** on TU Wien Phabricator (internal)
- **Clean release history** on GitHub (public)

This approach separates internal development from public releases while keeping both remotes synchronized for published packages.

---

## Remote Configuration

```bash
# Two remotes configured:
origin    ssh://vcs@phabricator.ict.tuwien.ac.at/source/Scienceplots_with_Python_for_Latex.git
github    git@github.com:jakobbuch/scienceplots-toolkit.git
```bash

| Remote | Purpose | Access |
|--------|---------|--------|
| `origin` (Phabricator)   | Full development history, internal collaboration | TU Wien VCS          | (Phabricator) | Full development history, internal collaboration | TU Wien VCS |
| `github` (GitHub)       | Clean release-only history, public distribution  | Public                 | (GitHub) | Clean release-only history, public distribution | Public |

---

## Branch Structure

### `master` Branch (Development)

- **Tracks**: `origin/master` (Phabricator)
- **Purpose**: Day-to-day development, feature work, bug fixes
- **History**: Complete development history with all commits
- **Push target**: Phabricator only

### `main` Branch (Publication)

- **Tracks**: `github/main` (GitHub)
- **Purpose**: Publication-ready commits, clean release history
- **History**: Curated, minimal commits for releases
- **Push target**: GitHub only

---

## Why This Workflow?

### Problem

- Phabricator doesn't allow history rewrites (force push rejected)
- GitHub releases benefit from clean, curated history
- Package on PyPI should have corresponding clean git tags

### Solution

Maintain two parallel branches:

1. **`master`** on Phabricator: Full development history (never rewritten)
2. **`main`** on GitHub: Clean release history (can be force-pushed)

### Benefits

- ✅ Phabricator retains complete development audit trail
- ✅ GitHub shows clean, user-friendly release history
- ✅ PyPI releases map to clean git tags
- ✅ No conflicts between internal and public workflows
- ✅ VS Code shows correct tracking status (no "publish branch" warnings)

---

## Daily Development Workflow

### Working on Features

```bash
# Always develop on master
git checkout master

# Make changes, commit, push to Phabricator
git add .
git commit -m "feat: add new feature"
git push origin master
```bash

### Syncing with Phabricator

```bash
# Pull latest changes from Phabricator
git checkout master
git pull origin master
```bash

---

## Release Workflow

### Step 1: Prepare Release Branch

```bash
# Switch to main branch
git checkout main

# Option A: Reset to specific commit from master
git log master --oneline  # Find the release commit
git reset --hard <commit-hash>

# Option B: Cherry-pick specific commits
git cherry-pick <commit-1>
git cherry-pick <commit-2>
```bash

### Step 2: Create Release Tag

```bash
# Create annotated tag with release notes
git tag -a v0.1.1 -m "v0.1.1 - Initial release with fixed save_plot

Changelog:
- Fixed save_plot() to handle string output_dir parameter
- Added comprehensive TestPyPI test script
- Updated PyPI badge in README"
```bash

### Step 3: Push to GitHub

```bash
# Push main branch and tags to GitHub
git push github release --force --tags
```bash

### Step 4: Build and Upload to PyPI

```bash
# Ensure you're on main branch
git checkout main

# Build distribution
uv build

# Upload to TestPyPI first (optional but recommended)
export TWINE_PASSWORD=$(cat /run/user/1000/agenix/pypi-test-token)
uv run twine upload --repository testpypi dist/*

# Verify on TestPyPI, then upload to production
export TWINE_PASSWORD=$(cat /run/user/1000/agenix/pypi-token)
uv run twine upload --repository pypi dist/*
```bash

### Step 5: Create GitHub Release

1. Go to <https://github.com/jakobbuch/scienceplots-toolkit/releases/new>
2. Select tag: `v0.1.1`
3. Click "Generate release notes"
4. Publish release

### Step 6: Return to Development

```bash
git checkout master
```bash

---

## Branch Management

### View All Branches and Tracking

```bash
git branch -vv
```bash

Expected output:

```bash
* master  0bfa237 [origin/master] chore: fix markdown duplicate heading
  release e7f1259 [github/main] docs: update PyPI badge URL
```bash

### Switch Between Branches in VS Code

1. Click branch name in bottom-left status bar
2. Select `master` or `main` from dropdown
3. VS Code will switch context automatically

### Update Release Branch from Master

```bash
# When master has new commits to include in next release
git checkout main
git reset --hard master  # Or specific commit
# Then tag and push as above
```bash

---

## Common Scenarios

### Scenario 1: Fix Bug in Development

```bash
# Fix bug on master
git checkout master
git add .
git commit -m "fix: resolve issue with X"
git push origin master

# Later, include in release
git checkout main
git cherry-pick <commit-hash>
git tag -a v0.1.2 -m "v0.1.2 - Bugfix release"
git push github release --force --tags
```bash

### Scenario 2: Hotfix for Released Version

```bash
# Create hotfix directly on main branch
git checkout main
# Make fix
git commit -m "fix: critical hotfix for Y"
git tag -a v0.1.3 -m "v0.1.3 - Hotfix"
git push github release --force --tags

# Later merge back to master
git checkout master
git cherry-pick <hotfix-commit>
git push origin master
```bash

### Scenario 3: Major Release with Multiple Features

```bash
# On master, develop multiple features
git checkout master
# ... multiple commits over time ...

# When ready for release
git checkout main
git reset --hard master  # Include all recent work
git tag -a v1.0.0 -m "v1.0.0 - Major release with features A, B, C"
git push github release --force --tags
```bash

---

## Git Commands Reference

### Remote Operations

```bash
# View remotes
git remote -v

# Fetch from both remotes
git fetch --all

# Push to specific remote
git push origin master      # Phabricator
git push github release     # GitHub
```bash

### Branch Operations

```bash
# List branches with tracking info
git branch -vv

# Create new main branch
git checkout -b release

# Set upstream tracking
git branch --set-upstream-to=github/main release

# Switch branches
git checkout master
git checkout main
```bash

### Tag Operations

```bash
# List tags
git tag -l

# Create annotated tag
git tag -a v1.0.0 -m "Release message"

# Push tags to specific remote
git push github --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push github :refs/tags/v1.0.0
```bash

---

## Troubleshooting

### VS Code Shows "Publish Branch"

**Cause**: Branch has no upstream tracking set.

**Fix**:

```bash
git branch --set-upstream-to=origin/master master   # For master
git branch --set-upstream-to=github/main release  # For release
```bash

### Force Push Rejected by Phabricator

**Expected behavior**: Phabricator rejects history rewrites.

**Solution**: Only force push to GitHub, never to Phabricator.

```bash
# ✅ OK
git push github release --force

# ❌ Will fail
git push origin master --force
```bash

### Accidentally Pushed to Wrong Remote

**Fix**:

```bash
# If you pushed main branch to Phabricator by mistake
git push origin :release  # Delete from Phabricator

# If you pushed master to GitHub by mistake
git push github :master   # Delete from GitHub
```bash

### Diverged Branch Warning

**Cause**: Local branch has different history than remote.

**For master** (Phabricator - don't rewrite):

```bash
git fetch origin
git reset --hard origin/master  # Align with Phabricator
```bash

**For release** (GitHub - can rewrite):

```bash
# Rebuild clean history, then force push
git reset --hard <desired-commit>
git push github release --force
```bash

---

## Best Practices

### ✅ Do

- Develop on `master`, push to Phabricator
- Create releases on `main` branch, push to GitHub
- Test on TestPyPI before production releases
- Use annotated tags (`-a`) with meaningful messages
- Keep `main` branch minimal (only release-ready commits)

### ❌ Don't

- Force push to Phabricator (`origin`)
- Push `master` to GitHub
- Push `main` to Phabricator
- Create lightweight tags (use `-a` for annotated)
- Forget to build (`uv build`) before uploading to PyPI

---

## Release Checklist

Before publishing a release:

- [ ] All tests pass (`uv run pytest`)
- [ ] Linting clean (`uv run ruff check .`)
- [ ] Type checking passes (`uv run ty check .`)
- [ ] README updated with correct version
- [ ] CHANGELOG.md updated (if maintained)
- [ ] Release branch created/updated
- [ ] Annotated tag created with release notes
- [ ] Uploaded to TestPyPI and verified
- [ ] Uploaded to production PyPI
- [ ] GitHub release page created
- [ ] Tag pushed to GitHub

---

## Quick Reference Card

```bash
# Daily development
git checkout master
# ... work ...
git push origin master

# Create release
git checkout main
git reset --hard master          # Or cherry-pick
git tag -a vX.Y.Z -m "Release"
git push github release --force --tags
uv build
uv run twine upload dist/*

# Switch branches in VS Code
# Click branch name (bottom-left) → select branch
```bash

---

## See Also

- [RELEASE.md](RELEASE.md) - Detailed release procedures
- [PYPI_SETUP_WITH_AGENIX.md](PYPI_SETUP_WITH_AGENIX.md) - PyPI token management
- [QUICK_START.md](QUICK_START.md) - Fast-track publication guide
