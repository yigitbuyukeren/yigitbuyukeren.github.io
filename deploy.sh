#!/usr/bin/env bash
# Siteyi VPS'e gönderir (Caddy /var/www/yigitbuyukeren altından sunar).
# VPS dağıtımı GitHub Pages'ten ayrı, açık istek gerektiren bir işlemdir.
set -euo pipefail
cd "$(dirname "$0")"

DEPLOY_USER="${DEPLOY_USER:-root}"
DEPLOY_HOST="${DEPLOY_HOST:-}"
DEPLOY_PATH="${DEPLOY_PATH:-/var/www/yigitbuyukeren}"

if [ -z "$DEPLOY_HOST" ]; then
  echo "Hata: DEPLOY_HOST tanımlı değil. Örnek: DEPLOY_HOST=example.com ./deploy.sh" >&2
  exit 1
fi

rsync -az --delete --exclude .git --exclude .github --exclude _gh --exclude .DS_Store --exclude CNAME --exclude .nojekyll --exclude deploy.sh --exclude tools --exclude README.md --exclude .claude --exclude CLAUDE.md --exclude AGENTS.md ./ "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "chown -R caddy:caddy \"${DEPLOY_PATH}\""
echo "Yayında: https://yigitbuyukeren.com"
