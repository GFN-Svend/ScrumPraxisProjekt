#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/opt/ScrumPraxisProjekt"
BRANCH="main"

cd "$REPO_DIR"

git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"

if [[ -f package.json ]]; then
  if [[ -f package-lock.json ]]; then
    npm ci
  else
    npm install
  fi

  npm run build
fi

sudo /usr/sbin/nginx -t
sudo /usr/bin/systemctl reload nginx
