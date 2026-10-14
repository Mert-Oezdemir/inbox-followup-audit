"""Smoke tests for skill metadata, read-only constraints, and ZIP structure."""
import subprocess
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "inbox-followup-audit" / "SKILL.md"


class ProjectChecks(unittest.TestCase):
    def test_frontmatter(self):
        data = SKILL.read_text(encoding="utf-8")
        self.assertTrue(data.startswith("---\n"))
        frontmatter = data.split("---", 2)[1]
        self.assertIn("name: inbox-followup-audit", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertLessEqual(len(next(x.split(":", 1)[1].strip() for x in frontmatter.splitlines() if x.startswith("description:"))), 200)

    def test_safe_defaults(self):
        txt = SKILL.read_text(encoding="utf-8")
        for phrase in ("son 30 günü", "Gönderilmiş", "taslak nesnesi dahi oluşturma", "güvenilmeyen"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, txt)

    def test_zip_layout(self):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "package_skill.py")], check=True)
        with ZipFile(ROOT / "dist" / "inbox-followup-audit-skill.zip") as z:
            self.assertIn("inbox-followup-audit/SKILL.md", z.namelist())
            self.assertTrue(all(p.startswith("inbox-followup-audit/") for p in z.namelist()))


if __name__ == "__main__":
    unittest.main()
