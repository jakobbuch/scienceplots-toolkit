# PyPI Publication with devenv + agenix

## Overview

This project uses **devenv + agenix** to securely manage PyPI credentials. Tokens are stored as encrypted secrets and automatically loaded when needed.

## Secrets Configuration

The following secrets should be configured in your agenix setup:

- `pypi-token` - Production PyPI API token
- `pypi-test-token` - TestPyPI API token

These are exposed at:

- `/run/user/1000/agenix/pypi-token`
- `/run/user/1000/agenix/pypi-test-token`

## Quick Start

### 1. Enter devenv shell

```bash
devenv shell
```

This decrypts and exposes your secrets.

### 2. Verify tokens are loaded

```bash
# Option A: Use the helper script
source scripts/load-pypi-tokens.sh

# Option B: Check manually
cat /run/user/1000/agenix/pypi-test-token | head -c 20
# Should show: pypi-AgEN...
```

### 3. Publish to TestPyPI

```bash
# Tokens are auto-loaded by the release script
./scripts/release.sh --test
```

### 4. Publish to Production PyPI

```bash
# After verifying TestPyPI works
./scripts/release.sh --production
```

## How It Works

The `release.sh` script automatically:

1. Checks for agenix secrets at `/run/user/1000/agenix/`
2. Loads the appropriate token based on `--test` or `--production` flag
3. Sets `TWINE_USERNAME` and `TWINE_PASSWORD` environment variables
4. Proceeds with upload

No manual token management needed!

## Manual Token Loading (Optional)

If you need tokens outside the release script:

```bash
# Source the helper script
source scripts/load-pypi-tokens.sh

# Or manually export
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD=$(cat /run/user/1000/agenix/pypi-test-token)
```

## Troubleshooting

### "PyPI credentials not set"

Make sure you're in the devenv shell:

```bash
devenv shell
```

Verify secrets exist:

```bash
ls -la /run/user/1000/agenix/pypi*
```

### "Permission denied"

Check that agenix has decrypted the secrets:

```bash
# Should show the token (first 20 chars)
cat /run/user/1000/agenix/pypi-test-token | head -c 20
```

If files don't exist, your agenix secrets might not be configured correctly in your devenv.nix or Home Manager configuration.

### "Invalid token"

Verify the token is correct:

```bash
# Check token length (should be ~100+ characters)
cat /run/user/1000/agenix/pypi-test-token | wc -c
```

If too short, the secret might not be properly encrypted/decrypted.

## Security Notes

- ✅ Tokens are **never** committed to git
- ✅ Tokens are **encrypted** at rest by agenix
- ✅ Tokens are **only accessible** in your user session
- ✅ Tokens are **automatically rotated** when you update secrets

## Creating New Tokens

If you need to create new PyPI tokens:

1. **PyPI**: <https://pypi.org/manage/account/token/>
2. **TestPyPI**: <https://test.pypi.org/manage/account/token/>

Then update your agenix secrets (method depends on your setup).

## Example Session

```bash
# Enter devenv shell (secrets decrypted)
$ devenv shell

# Run release to TestPyPI (tokens auto-loaded)
(devenv) $ ./scripts/release.sh --test
ℹ️  Running pre-flight checks...
✓ Loaded TestPyPI token from agenix
✓ Git repository is clean
✓ Latest tag: v0.1.0
✓ Required tools available (uv, twine)
✓ PyPI credentials configured
ℹ️  Building distribution packages...
✓ Distribution packages built successfully
ℹ️  Uploading to testpypi...
✓ Upload successful!
```

---

**That's it!** Your PyPI credentials are securely managed by agenix. Just run the release script! 🎉
