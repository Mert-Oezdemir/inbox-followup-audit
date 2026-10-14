#!/usr/bin/env python3
"""Basic public-repository hygiene checks, not a substitute for code review."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_SUFFIX = {".mbox", ".eml", ".pst", ".ost", ".pem", ".key", ".p12", ".pfx"}
BLOCKED_NAMES = {".env", "credentials.json", "token.json", "secrets.json"}
SECRETS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
}


def public_files():
    """Prefer the actual staged/tracked files in git when available."""
    out = subprocess.run(
        ["git", "ls-files", "-c", "-o", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if out.returncode == 0:
        return [ROOT / path for path in out.stdout.splitlines()]
    return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "dist" not in p.parts]


def main() -> None:
    issues = []
    for path in public_files():
        if not path.is_file():
            continue
        if path.suffix.lower() in BLOCKED_SUFFIX or path.name in BLOCKED_NAMES:
            issues.append(f"Yasak dosya: {path.relative_to(ROOT)}")
            continue
        if path.is_symlink():
            issues.append(f"Sembolik bağlantı: {path.relative_to(ROOT)}")
            continue
        try:
            txt = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in SECRETS.items():
            if pattern.search(txt):
                issues.append(f"Muhtemel {label}: {path.relative_to(ROOT)}")
    if issues:
        raise SystemExit("\n".join(issues))
    print("Temel gizli bilgi ve dosya kontrolleri geçti.")


if __name__ == "__main__":
    main()
