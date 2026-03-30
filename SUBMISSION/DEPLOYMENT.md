# Deployment Guide

This repository does not currently ship Dockerfiles, Compose manifests, or CI/CD assets. The workable deployment path is manual backend deployment plus a built static frontend.

## Constraints

- API version is `/api/v1`
- Frontend API base URL is injected at build time through `VITE_API_BASE_URL`
- No authentication, secret management, or user access control layer is implemented

## Backend Deployment

```bash
cd /opt/ai4mh/backend
python3 -m venv .venv312
source .venv312/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Recommended environment overrides:

```bash
export AI4MH_SQLITE_PATH=/var/lib/ai4mh/ai4mh.db
export AI4MH_ALLOWED_ORIGINS='["https://ai4mh.example.com"]'
```

Run with Gunicorn + Uvicorn worker:

```bash
source .venv312/bin/activate
python -m pip install gunicorn
gunicorn main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 2 \
  --bind 127.0.0.1:8000
```

`backend/main.py` is a compatibility wrapper that re-exports `app.main:app`, so `main:app` remains valid from the `backend/` working directory.

## Frontend Deployment

Build with the production API URL:

```bash
cd /opt/ai4mh/frontend
npm install
VITE_API_BASE_URL=https://ai4mh.example.com/api/v1 npm run build
```

Serve `frontend/dist/` with Nginx or any static file server.

## Nginx Example

```nginx
server {
    listen 443 ssl http2;
    server_name ai4mh.example.com;

    root /opt/ai4mh/frontend/dist;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri /index.html;
    }
}
```

## Systemd Example

Backend service:

```ini
[Unit]
Description=AI4MH API
After=network.target

[Service]
User=ai4mh
WorkingDirectory=/opt/ai4mh/backend
Environment=AI4MH_SQLITE_PATH=/var/lib/ai4mh/ai4mh.db
Environment=AI4MH_ALLOWED_ORIGINS=["https://ai4mh.example.com"]
ExecStart=/opt/ai4mh/backend/.venv312/bin/gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --workers 2 --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Post-Deploy Validation

```bash
curl -s https://ai4mh.example.com/api/v1/posts?limit=3 | jq '.total'
curl -s https://ai4mh.example.com/api/v1/scores | jq '.scores | length'
```

## Operational Gaps

- No auth/authz layer
- No structured metrics endpoint
- No container assets in repo
- No migration system beyond SQLite table bootstrap in `SQLiteStore`
