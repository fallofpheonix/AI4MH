# Deployment Guide

Production deployment instructions for AI4MH.

## Deployment Overview

This guide covers deploying AI4MH to production environments.

## Prerequisites

- Docker & Docker Compose (recommended)
- Or: Python 3.10+, Node.js 16+
- Server with 4GB+ RAM
- HTTPS certificate (for security)
- Reverse proxy (nginx/Apache)

## Option 1: Docker Deployment (Recommended)

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - AI4MH_ALERT_THRESHOLD=0.80
      - AI4MH_DB_PATH=/data/ai4mh.db
    volumes:
      - ./data:/data
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    depends_on:
      - backend
    restart: always
```

### Launch with Docker Compose

```bash
docker-compose up -d
```

## Option 2: Manual Deployment

### Backend Setup

```bash
# 1. Install Python dependencies
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt

# 2. Configure environment
export AI4MH_ALERT_THRESHOLD=0.80
export AI4MH_DB_PATH=/var/lib/ai4mh/data.db

# 3. Run with production server
pip install gunicorn
gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

### Frontend Build

```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Build for production
npm run build

# 3. Serve with web server
npx serve -s dist -l 3000
```

## Systemd Service Files

### Backend Service

Create `/etc/systemd/system/ai4mh-backend.service`:

```ini
[Unit]
Description=AI4MH Backend
After=network.service

[Service]
Type=notify
User=ai4mh
WorkingDirectory=/opt/ai4mh/backend
ExecStart=/opt/ai4mh/backend/venv/bin/gunicorn main:app --workers 4
Environment="AI4MH_DB_PATH=/var/lib/ai4mh/data.db"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Frontend Service

Create `/etc/systemd/system/ai4mh-frontend.service`:

```ini
[Unit]
Description=AI4MH Frontend
After=network.service

[Service]
Type=simple
User=ai4mh
WorkingDirectory=/opt/ai4mh/frontend
ExecStart=/usr/bin/npx serve -s dist -l 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai4mh-backend.service
sudo systemctl enable ai4mh-frontend.service
sudo systemctl start ai4mh-backend.service
sudo systemctl start ai4mh-frontend.service
```

## Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/ai4mh
upstream backend {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name ai4mh.example.com;

    ssl_certificate /etc/letsencrypt/live/ai4mh.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ai4mh.example.com/privkey.pem;

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }

    # CORS headers
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/ai4mh /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d ai4mh.example.com
```

Certificate renewal (automatic with certbot):
```bash
sudo certbot renew --dry-run
```

## Environment Variables for Production

```bash
# Alert thresholds
export AI4MH_ALERT_THRESHOLD=0.80
export AI4MH_CONFIDENCE_THRESHOLD=0.70

# Scoring weights
export AI4MH_WEIGHT_SENTIMENT=0.40
export AI4MH_WEIGHT_VOLUME=0.35
export AI4MH_WEIGHT_GEO=0.15
export AI4MH_WEIGHT_TREND=0.10

# Data limits
export AI4MH_MAX_POSTS=5000
export AI4MH_MIN_REGION_SAMPLE=20

# Database
export AI4MH_DB_PATH=/var/lib/ai4mh/ai4mh.db

# Security
export AI4MH_WORKERS=4  # CPU cores
```

## Monitoring

### Health Check Endpoint

```bash
curl -s https://ai4mh.example.com/api/posts | jq '.total'
```

### Log Aggregation

Monitor logs:
```bash
# Backend
sudo journalctl -u ai4mh-backend.service -f

# Frontend
sudo journalctl -u ai4mh-frontend.service -f
```

### Prometheus Metrics (Optional)

Install prometheus client:
```bash
pip install prometheus-client
```

Add to `main.py`:
```python
from prometheus_client import Counter, Histogram

request_counter = Counter('requests_total', 'Total requests')
response_time = Histogram('response_time_seconds', 'Response time')
```

## Backup & Recovery

### Database Backup

```bash
# Daily backup
0 2 * * * cp /var/lib/ai4mh/ai4mh.db /var/backups/ai4mh-$(date +\%Y-\%m-\%d).db
```

### Restore from Backup

```bash
cp /var/backups/ai4mh-2024-03-17.db /var/lib/ai4mh/ai4mh.db
sudo systemctl restart ai4mh-backend.service
```

## Scaling

### Horizontal Scaling

Use multiple backend instances with load balancing:

```nginx
upstream backend_cluster {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

location /api {
    proxy_pass http://backend_cluster;
}
```

### Performance Tuning

```python
# backend/main.py
app = FastAPI(
    title="AI4MH API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Gunicorn workers
gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker
```

## Security Considerations

### Input Validation
- All requests validated with Pydantic models
- SQL injection protected (using ORM)
- XSS prevention (by default in React)

### Authentication (Future)
- Add JWT token auth for sensitive endpoints
- Rate limiting to prevent DDoS
- API key management

### Data Protection
- Use HTTPS/TLS (mandatory in production)
- Encrypt sensitive data at rest
- Regular security audits
- Keep dependencies updated

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u ai4mh-backend.service -n 50

# Verify environment variables
printenv | grep AI4MH

# Test manually
cd /opt/ai4mh/backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0
```

### Database Lock

```bash
# Remove lock file
rm -f /var/lib/ai4mh/ai4mh.db-wal
rm -f /var/lib/ai4mh/ai4mh.db-shm

# Restart service
sudo systemctl restart ai4mh-backend.service
```

### Out of Memory

```bash
# Monitor memory usage
top -u ai4mh

# Reduce max posts in memory
export AI4MH_MAX_POSTS=1000
```

## Maintenance

### Regular Tasks

- [ ] Check disk space weekly
- [ ] Review logs for errors
- [ ] Update dependencies monthly
- [ ] Test backups monthly
- [ ] Security audit quarterly

### Update Process

```bash
# New deployment
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && npm install && npm run build
sudo systemctl restart ai4mh-backend.service
sudo systemctl restart ai4mh-frontend.service
```

---

For more information see [SUBMISSION/README.md](SUBMISSION/README.md)
