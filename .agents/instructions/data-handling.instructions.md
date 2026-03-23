---
description: "Standards for data processing and timezone handling."
applyTo: "**/*.py"
---

# Data Handling Standards

Follow these rules for all data processing in this repository.

## Data Loading

- Do not implement custom CSV parsing for standard data files if a loader
  is available.
- If loading time series data, ensure consistent timezone handling (prefer
  UTC or a single local timezone throughout).

## Script Creation

- When creating a new script:
  - Add a brief description to `README.md`.
  - Ensure it follows the "Plotting" and "Path Handling" guidelines.
