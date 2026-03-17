# Verification Guide

Step-by-step verification that your AI4MH installation is working correctly.

## Pre-Verification Checklist

- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Python 3.10+ available
- [ ] Node.js 16+ available
- [ ] Ports 8000 and 5173 available

## Verification Steps

### Step 1: Backend Import Verification (1 minute)

```bash
cd backend
source .venv312/bin/activate
python3 -c "
from main import app
from config import settings
from pipeline.score import score_all_regions
print('✓ Backend imports successfully')
print(f'✓ Python version: {__import__(\"sys\").version}')
print(f'✓ Alert threshold: {settings.alert_threshold}')
"
```

Expected output:
```
✓ Backend imports successfully
✓ Python version: 3.x.x ...
✓ Alert threshold: 0.8
```

### Step 2: Frontend Build Verification (2 minutes)

```bash
cd frontend
npm run build
```

Expected output:
```
✓ [SUCCESS] built in XXms
```

### Step 3: Configuration Verification (1 minute)

```bash
cd backend
source .venv312/bin/activate
python3 -c "
from config import settings
assert settings.alert_threshold > 0
assert settings.confidence_threshold > 0
assert abs(sum(settings.weights.values()) - 1.0) < 0.01
print('✓ Configuration: Alert threshold =', settings.alert_threshold)
print('✓ Configuration: Confidence threshold =', settings.confidence_threshold)
print('✓ Configuration: Scoring weights sum =', sum(settings.weights.values()))
"
```

Expected output:
```
✓ Configuration: Alert threshold = 0.8
✓ Configuration: Confidence threshold = 0.7
✓ Configuration: Scoring weights sum = 1.0
```

### Step 4: Scoring Engine Verification (2 minutes)

```bash
cd backend
source .venv312/bin/activate
python3 -c "
from pipeline.score import _sentiment_intensity, _volume_spike
from models.post import EnrichedPost
import datetime

# Test sentiment signal
posts = [
    EnrichedPost(
                id='1', 
                text='I am very sad',
                sentiment_compound=-0.8,
                region_id='region_1',
                crisis_keywords=0,
                created_at=datetime.datetime.now()
            )
]
score = _sentiment_intensity(posts)
print(f'✓ Sentiment signal: {score:.2f}')

# Test volume signal
posts_batch = posts * 5
vol_signal = _volume_spike(posts_batch, baseline=1)
print(f'✓ Volume signal: {vol_signal:.2f}')
"
```

Expected output:
```
✓ Sentiment signal: 0.80
✓ Volume signal: 0.50
```

### Step 5: Database Verification (1 minute)

```bash
cd backend
source .venv312/bin/activate
python3 -c "
from storage.sqlite import SQLiteStore
store = SQLiteStore(db_path=':memory:')
posts = store.get_posts()
print(f'✓ Database: {len(posts)} posts')
alerts = store.get_alerts()
print(f'✓ Database: {len(alerts)} alerts')
print('✓ Database connection: OK')
"
```

Expected output:
```
✓ Database: 0 posts
✓ Database: 0 alerts
✓ Database connection: OK
```

### Step 6: API Startup Verification (5 minutes)

**Terminal 1: Start Backend**
```bash
cd backend
source .venv312/bin/activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2: Test API**
```bash
# Wait for backend to initialize (30 seconds)
sleep 30

# Test API health
curl -s http://127.0.0.1:8000/api/posts | python3 -m json.tool | head -20
```

Expected output:
```json
{
  "posts": [
    {
      "id": "...",
      "text": "...",
      ...
    }
  ],
  "total": 3
}
```

### Step 7: Frontend Startup Verification (3 minutes)

**Terminal 3: Start Frontend**
```bash
cd frontend
npm run dev
```

Wait for:
```
➜  Local:   http://127.0.0.1:5173/
```

**Terminal 4: Test Frontend**
```bash
curl -s http://localhost:5173 | head -20
```

Expected output: HTML content starting with `<!DOCTYPE html>`

### Step 8: Dashboard Verification (3 minutes)

1. Open browser: http://localhost:5173
2. Look for:
   - [ ] Dashboard loads without errors
   - [ ] "Posts" section visible
   - [ ] "Scores" section visible
   - [ ] "Alerts" section visible
   - [ ] "Logs" section visible

### Step 9: API Endpoint Verification (2 minutes)

```bash
# In Terminal 2 (where you tested /api/posts)

# Test all endpoints
echo "Testing /api/scores..."
curl -s http://127.0.0.1:8000/api/scores | python3 -c "import json, sys; d=json.load(sys.stdin); print(f\"✓ {len(d['scores'])} scores\")"

echo "Testing /api/alerts..."
curl -s http://127.0.0.1:8000/api/alerts | python3 -c "import json, sys; d=json.load(sys.stdin); print(f\"✓ {len(d['alerts'])} alerts\")"

echo "Testing /api/logs..."
curl -s http://127.0.0.1:8000/api/logs | python3 -c "import json, sys; d=json.load(sys.stdin); print(f\"✓ {len(d['logs'])} log entries\")"

echo "Testing /api/bias..."
curl -s http://127.0.0.1:8000/api/bias | python3 -c "import json, sys; d=json.load(sys.stdin); print(f\"✓ Bias data available\")"
```

Expected output:
```
Testing /api/scores...
✓ X scores
Testing /api/alerts...
✓ X alerts
Testing /api/logs...
✓ X log entries
Testing /api/bias...
✓ Bias data available
```

### Step 10: Full Health Check (5 minutes)

```bash
bash scripts/full_health_check.sh
```

Expected output:
```
[1/5] Starting backend
[2/5] Starting frontend
[3/5] Waiting for services
[4/5] Validating API
[5/5] Running diagnostics
✓ All checks passed
```

## Verification Summary

Complete the checklist below:

- [ ] Backend imports work (Step 1)
- [ ] Frontend builds successfully (Step 2)
- [ ] Configuration is valid (Step 3)
- [ ] Scoring functions work (Step 4)
- [ ] Database connection works (Step 5)
- [ ] Backend API responds (Step 6)
- [ ] Frontend serves content (Step 7)
- [ ] Dashboard loads in browser (Step 8)
- [ ] All API endpoints respond (Step 9)
- [ ] Full health check passes (Step 10)

## If Verification Fails

### Common Issues

**"Connection refused on port 8000"**
- Ensure backend is running
- Check backend startup logs for errors
- Try: `python -m uvicorn main:app --port 8001`

**"Frontend won't load"**
- Ensure npm dependencies installed: `npm install`
- Check frontend logs: `npm run dev` (run in terminal)
- Try: `npm run dev -- --port 5174`

**"Database errors"**
- Reset database: `rm backend/ai4mh.db`
- Restart backend

**"CORS errors"**
- Verify frontend URL in CORS config (main.py)
- Clear browser cache
- Check browser console for specific errors

### Get Help

See [INSTALLATION.md](INSTALLATION.md) troubleshooting section for more solutions.

---

**Verification completed successfully!** 🎉

Next step: Run tests - See [TESTING.md](SUBMISSION/TESTING.md)
