import os
import unittest
import yaml

class TestSemgrepRulesSuite(unittest.TestCase):
    def setUp(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_core_files_exist(self):
        required = [
            "README.md",
            "Makefile",
            "SECURITY.md",
            ".gitattributes",
            "docs/architecture.svg",
            "scripts/verify_rules.py",
            "scripts/healthcheck.sh",
            "rules/terraform/terraform-s3-public-access.yml",
            "rules/terraform/terraform-security-group-ingress-anywhere.yml",
            "rules/terraform/terraform-iam-wildcard-actions.yml",
            "rules/docker/docker-root-user.yml",
            "rules/docker/docker-latest-tag.yml",
            "rules/docker/docker-sensitive-mount.yml",
            "rules/python/python-sql-injection.yml",
            "rules/python/python-command-injection.yml",
            "rules/python/python-insecure-deserialization.yml",
            "rules/go/go-sql-injection.yml",
            "rules/go/go-command-injection.yml",
            "rules/go/go-weak-crypto.yml",
            "rules/secrets/ci-secrets-leak.yml",
            "rules/secrets/jwt-hardcoded-secret.yml"
        ]
        for f in required:
            p = os.path.join(self.root, f)
            self.assertTrue(os.path.exists(p), f"Required rule file '{f}' must be present")

    def test_rules_validation_runner(self):
        rule_dir = os.path.join(self.root, "rules")
        for r, _, files in os.walk(rule_dir):
            for f in files:
                if f.endswith(".yml") or f.endswith(".yaml"):
                    fp = os.path.join(r, f)
                    with open(fp, "r", encoding="utf-8") as handle:
                        content = yaml.safe_load(handle)
                    self.assertIn("rules", content)
                    for rule in content["rules"]:
                        self.assertIn("id", rule)
                        self.assertIn("message", rule)
                        self.assertIn("severity", rule)
                        self.assertIn("languages", rule)

    def test_gitattributes_content(self):
        path = os.path.join(self.root, ".gitattributes")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("*.yaml linguist-detectable=true", content)
        self.assertIn("Makefile linguist-vendored=true", content)

if __name__ == "__main__":
    unittest.main()
