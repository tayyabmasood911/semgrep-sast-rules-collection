# Security Policy

## Supported Versions

Only rules maintained on the `main` branch are actively updated to align with the latest Semgrep core specifications.

| Version | Supported          |
|:--------|:------------------:|
| main    | :white_check_mark: |
| < main  | :x:                |

## Reporting a Vulnerability or Rule Bypass

If you discover a false-negative evasion, rule syntax vulnerability, or secret leakage issue within this repository:

1. **Do not submit a public issue** documenting the evasion technique.
2. Email maintainer **Tayyab Masood** directly at **tayyabmasood911@gmail.com** with the subject `[SEMGREP SECURITY] Rule Evasion / Defect Report`.
3. Provide the rule identifier, proof of concept code, and observed vs expected AST matching behavior.

### Remediation Process
All verified evasion vulnerabilities or syntax defects will receive a triaged fix within 72 hours and be incorporated into the regression testing matrix.
