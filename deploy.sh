#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/opt/ScrumPraxisProjekt"
WEB_ROOT="/var/www/scrumpraxis"
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

find "$WEB_ROOT" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

if [[ -d dist ]]; then
  cp -a dist/. "$WEB_ROOT"/
elif [[ -d public ]]; then
  cp -a public/. "$WEB_ROOT"/
elif [[ -f index.html ]]; then
  cp -a index.html "$WEB_ROOT"/
else
  cat > "$WEB_ROOT/index.html" <<'HTML'
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ScrumPraxisProjekt</title>
  <style>
    body { margin: 0; min-height: 100vh; display: grid; place-items: center; font-family: system-ui, sans-serif; background: #f6f7f9; color: #1f2937; }
    main { text-align: center; padding: 2rem; }
    h1 { margin: 0 0 .5rem; font-size: clamp(2rem, 5vw, 4rem); }
    p { margin: 0; color: #4b5563; }
  </style>
</head>
<body>
  <main>
    <h1>ScrumPraxisProjekt</h1>
    <p>Deployment ist eingerichtet.</p>
  </main>
</body>
</html>
HTML
fi

sudo /usr/sbin/nginx -t
sudo /usr/bin/systemctl reload nginx
