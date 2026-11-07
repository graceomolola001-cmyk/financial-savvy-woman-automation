#!/usr/bin/env python3
"""Scan public n8n workflow templates for obvious private data. Review manually too."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = sorted((root / "workflows").glob("*.json"))
patterns = {
    "email address": r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    "Google OAuth client domain": r"apps\.googleusercontent\.com",
    "private n8n instance": r"https?://[\w.-]+\.hostingersite\.com",
    "spreadsheet ID": r"\b1[A-Za-z0-9_-]{30,}\b",
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "10-digit account-number-like value": r"(?<!\d)\d{10}(?!\d)",
}
sensitive_keys = {"credentials", "webhookId", "pinData", "staticData", "executionData", "shared"}
issues = []
def visit(x, where):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in sensitive_keys:
                issues.append(f"{where}: forbidden field {k}")
            visit(v, where + "." + k)
    elif isinstance(x, list):
        for i, value in enumerate(x):
            visit(value, where + f"[{i}]")
    elif isinstance(x, str):
        for name, pattern in patterns.items():
            if re.search(pattern, x, re.I):
                issues.append(f"{where}: potential {name}")

for path in files:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
            issues.append(f"{path}: not an n8n workflow export")
        else:
            visit(data, str(path.relative_to(root)))
    except (OSError, ValueError) as exc:
        issues.append(f"{path}: {exc.__class__.__name__}")
if not files:
    issues.append("No workflow templates found")
if issues:
    print("\n".join("BLOCKED: " + item for item in issues))
    sys.exit(1)
print(f"PASS: {len(files)} sanitized templates scanned for common sensitive content")
