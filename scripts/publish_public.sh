#!/usr/bin/env bash
# Publish this original project into a NEW public GitHub repository.
# Requires gh CLI authenticated with permission to create repositories.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_NAME="${1:-inbox-followup-audit}"

if [[ ! "$REPO_NAME" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "Depo adı sadece harf, rakam, nokta, tire veya alt çizgi içerebilir." >&2
  exit 1
fi
command -v gh >/dev/null || { echo "GitHub CLI gerekli: https://cli.github.com/" >&2; exit 1; }
command -v git >/dev/null || { echo "git gerekli." >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Önce: gh auth login" >&2; exit 1; }
cd "$ROOT"

if [[ ! -d .git ]]; then
  git init -b main
  if ! git config user.name >/dev/null; then
    git config user.name "Inbox Follow-up Audit contributors"
  fi
  if ! git config user.email >/dev/null; then
    git config user.email "contributors@users.noreply.github.com"
  fi
  git add .
  git commit -m "Initial release: privacy-first inbox follow-up audit skill"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Yayınlamadan önce çalışma ağacındaki değişiklikleri kontrol edip commit et." >&2
  exit 1
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo "origin zaten tanımlı; mevcut bir uzak depoyu yanlışlıkla değiştirmemek için durduruldu." >&2
  exit 1
fi

OWNER="$(gh api user --jq .login)"
TARGET="$OWNER/$REPO_NAME"
if gh repo view "$TARGET" >/dev/null 2>&1; then
  echo "Bu isimde zaten bir depo var: $TARGET. Var olan depoya müdahale edilmedi." >&2
  exit 1
fi

echo "GitHub'da herkese açık yeni depo oluşturuluyor: $TARGET"
gh repo create "$TARGET" --public --source="$ROOT" --remote=origin --push --description "Privacy-first, read-only inbox follow-up audit Agent Skill (TR)"
echo "Yayınlandı: https://github.com/$TARGET"
