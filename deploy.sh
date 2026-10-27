#!/usr/bin/env bash
# Siteyi VPS'e gönderir (Caddy /var/www/yigitbuyukeren altından sunar).
set -euo pipefail
cd "$(dirname "$0")"
rsync -az --delete --exclude .git --exclude .github --exclude _gh --exclude .DS_Store --exclude CNAME --exclude .nojekyll --exclude deploy.sh --exclude tools --exclude README.md ./ root@82.153.241.6:/var/www/yigitbuyukeren/
ssh root@82.153.241.6 'chown -R caddy:caddy /var/www/yigitbuyukeren'
echo "Yayında: https://yigitbuyukeren.com"
