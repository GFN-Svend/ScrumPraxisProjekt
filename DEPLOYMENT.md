# Deployment

This repository deploys automatically to `/opt/ScrumPraxisProjekt` when changes are pushed to `main`.

The Flask app is served at:

```text
https://scrum.zvendson.com
```

## GitHub Actions secrets

Create these repository secrets in GitHub:

- `SSH_HOST`: server IP address or DNS name
- `SSH_USER`: `scrumpraxis`
- `SSH_KEY`: private key from `/root/.ssh/github-actions-scrum-praxis-projekt`

Show the private key on the server with:

```bash
cat /root/.ssh/github-actions-scrum-praxis-projekt
```

GitHub path:

```text
Repository -> Settings -> Secrets and variables -> Actions -> New repository secret
```

## Server behavior

The deploy script:

1. Fetches `origin/main`.
2. Resets `/opt/ScrumPraxisProjekt` to `origin/main`.
3. Runs `npm ci` or `npm install` and `npm run build` when `package.json` exists.
4. Installs Python dependencies from `requirements.txt` into `.venv`.
5. Restarts `scrumpraxis.service`.
6. Tests and reloads nginx.

The existing nginx site is not changed by this repository setup.

The Linux deploy user is `scrumpraxis`. It owns `/opt/ScrumPraxisProjekt` and may only run these commands through passwordless sudo:

```bash
/usr/sbin/nginx -t
/usr/bin/systemctl reload nginx
/usr/bin/systemctl restart scrumpraxis.service
```

## Nginx

The active server block is `/etc/nginx/sites-available/scrumpraxis` and proxies to the Gunicorn socket at `/run/scrumpraxis/gunicorn.sock`.

For a static HTML site:

```nginx
server {
    listen 80;
    server_name example.com;

    root /opt/ScrumPraxisProjekt;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

For a Vite/React build:

```nginx
server {
    listen 80;
    server_name example.com;

    root /opt/ScrumPraxisProjekt/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```
