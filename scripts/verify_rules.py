#!/usr/bin/env python3
"""
Semgrep Custom Rule Suite Validator
Recursively validates YAML syntax, Semgrep schema fields, regex compilations, and language targets.
"""

import os
import sys
import yaml
import re

REQUIRED_RULE_FIELDS = {"id", "message", "severity", "languages"}
VALID_SEVERITIES = {"INFO", "WARNING", "ERROR"}

def validate_rule_file(filepath):
    print(f"[*] Validating rule file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"  [FAIL] YAML Syntax error in {filepath}: {e}", file=sys.stderr)
            return False

    if not isinstance(data, dict) or "rules" not in data:
        print(f"  [FAIL] Missing root 'rules' key in {filepath}", file=sys.stderr)
        return False

    rules = data.get("rules", [])
    if not isinstance(rules, list) or len(rules) == 0:
        print(f"  [FAIL] 'rules' must be a non-empty list in {filepath}", file=sys.stderr)
        return False

    for idx, r in enumerate(rules):
        rule_id = r.get("id", f"index-{idx}")
        missing = REQUIRED_RULE_FIELDS - set(r.keys())
        if missing:
            print(f"  [FAIL] Rule '{rule_id}' missing required fields: {missing}", file=sys.stderr)
            return False

        sev = r.get("severity", "").upper()
        if sev not in VALID_SEVERITIES:
            print(f"  [FAIL] Rule '{rule_id}' has invalid severity '{sev}'", file=sys.stderr)
            return False

        # Validate regex if pattern-regex present
        patterns = r.get("patterns", [])
        for p in patterns:
            if isinstance(p, dict) and "pattern-regex" in p:
                reg = p["pattern-regex"]
                try:
                    re.compile(reg)
                except re.error as e:
                    print(f"  [FAIL] Invalid regex in '{rule_id}': {e}", file=sys.stderr)
                    return False

        print(f"  [PASS] Rule '{rule_id}' ({sev}) [{', '.join(r.get('languages', []))}]")
    return True

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rules"))
    success = True
    rule_count = 0
    file_count = 0

    for r, _, files in os.walk(root):
        for f in files:
            if f.endswith(".yml") or f.endswith(".yaml"):
                file_count += 1
                fp = os.path.join(r, f)
                if not validate_rule_file(fp):
                    success = False

    print("==================================================")
    print(f"Validated {file_count} Semgrep rule files across rules/")
    if not success:
        print("[FAILED] One or more Semgrep rules failed schema validation.", file=sys.stderr)
        sys.exit(1)
    print("[SUCCESS] All custom Semgrep rules conform to production schema.")
    sys.exit(0)

if __name__ == "__main__":
    main()
