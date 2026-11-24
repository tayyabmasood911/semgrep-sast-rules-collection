#!/usr/bin/env bash
set -euo pipefail

echo "=== Semgrep SAST Rule Collection Healthcheck ==="
python3 scripts/verify_rules.py

if command -v semgrep &> /dev/null; then
    echo "[OK] Semgrep CLI binary detected: $(semgrep --version)"
    semgrep --validate --config rules/
else
    echo "[INFO] Semgrep CLI not installed in local environment. Schema verified via Python engine."
fi

echo "[OK] Healthcheck complete."
exit 0
