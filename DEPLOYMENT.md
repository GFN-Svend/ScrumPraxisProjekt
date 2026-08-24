# Deployment

This repository deploys automatically to `/opt/ScrumPraxisProjekt` when changes are pushed to `main`.

The website is served at:

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
4. Publishes the website to `/var/www/scrumpraxis`.
5. Tests and reloads nginx.

Publishing source priority:

1. `dist/` when a build produced it.
2. `public/` when it exists.
3. Root `index.html` when it exists.
4. A small placeholder page when no website files exist yet.

The existing nginx site is not changed by this repository setup.

The Linux deploy user is `scrumpraxis`. It owns `/opt/ScrumPraxisProjekt` and may only run these commands through passwordless sudo:

```bash
/usr/sbin/nginx -t
/usr/bin/systemctl reload nginx
```

## Nginx

Add a separate nginx server block for this project once the domain or subdomain is known.
The active server block is `/etc/nginx/sites-available/scrumpraxis` and serves `/var/www/scrumpraxis`.

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
