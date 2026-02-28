#!/usr/bin/env bash
set -euo pipefail

# Helper script: create branches and run validation commands for v5 migration.
# This script is intentionally conservative and does not auto-move files.

echo "== NECHTO v5 migration helper =="

echo "[1/3] Suggested branch sequence"
printf '%s\n' \
  "pr1/docs-rails-root-cleanup" \
  "pr2/v5-skeleton-and-moves" \
  "pr3/split-modules-levels" \
  "pr4/api-surface-cleanup" \
  "pr5/docs-glossary-adr"

echo "[2/3] Validation commands"
printf '%s\n' \
  'python -m pip install -e ".[dev]"' \
  'nechto --version' \
  'nechto selftest' \
  'python examples/00_smoke.py' \
  'python -m pytest -q'

echo "[3/3] Example branch bootstrap"
printf '%s\n' \
  'git checkout main' \
  'git pull --ff-only' \
  'git checkout -b pr1/docs-rails-root-cleanup'
