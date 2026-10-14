#!/usr/bin/env python3
"""Build a portable ZIP with one top-level Agent Skill folder."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "inbox-followup-audit"
OUT = ROOT / "dist" / "inbox-followup-audit-skill.zip"


def main() -> None:
    if not (SKILL_DIR / "SKILL.md").is_file():
        raise SystemExit("Beceri dosyası bulunamadı.")
    files = sorted(p for p in SKILL_DIR.rglob("*") if p.is_file())
    if not files:
        raise SystemExit("Beceri boş.")
    forbidden = {".env", "token.json", "credentials.json"}
    if any(p.name in forbidden or p.is_symlink() for p in files):
        raise SystemExit("Paketlenemeyen gizli dosya veya sembolik bağlantı saptandı.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, f"{SKILL_DIR.name}/{path.relative_to(SKILL_DIR).as_posix()}")
    print(f"Oluşturuldu: {OUT}")


if __name__ == "__main__":
    main()
