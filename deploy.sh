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

if [[ -f requirements.txt ]]; then
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

sudo /usr/bin/systemctl restart scrumpraxis.service
sudo /usr/sbin/nginx -t
sudo /usr/bin/systemctl reload nginx
