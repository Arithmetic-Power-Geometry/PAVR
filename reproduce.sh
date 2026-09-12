#!/usr/bin/env bash
set -euo pipefail
pytest -q
python scripts/run_all.py
