# Installation Guide

Complete step-by-step instructions to set up AI4MH for development or evaluation.

## Prerequisites

### System Requirements
- macOS, Linux, or Windows (with WSL2)
- 4GB RAM minimum
- 2GB disk space

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **Git**: For version control

### Verify Prerequisites

```bash
python3 --version    # Should show 3.10+
node --version       # Should show 16+
npm --version        # Should show 8+
git --version        # Should show 2.x+
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI4MH.git
cd AI4MH
```

### 2. Backend Setup

#### Option A: Using Virtual Environment (Recommended)

```bash
cd backend

# Create virtual environment
python3 -m venv .venv312

# Activate virtual environment
source .venv312/bin/activate    # macOS/Linux
# or
.venv312\Scripts\activate       # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using Conda

```bash
cd backend

# Create conda environment
conda create -n ai4mh python=3.12
conda activate ai4mh

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Verify installation
npm list react vue
```

### 4. Verify Installation

```bash
# Test backend imports
cd backend
python3 -c "from main import app; print('✓ Backend OK')"

# Test frontend setup
cd ../frontend
npm run build --dry-run && echo "✓ Frontend OK"
```

## Configuration

### Backend Configuration

All settings are in `backend/config.py`. Override with environment variables:

```bash
# Example: Override alert threshold
export AI4MH_ALERT_THRESHOLD=0.75
export AI4MH_MAX_POSTS=500
export AI4MH_CONFIDENCE_THRESHOLD=0.65
```

### Available Configuration Options

```python
# Alert generation
AI4MH_ALERT_THRESHOLD=0.80        # Score threshold for alerts
AI4MH_CONFIDENCE_THRESHOLD=0.70   # Confidence threshold

# Scoring weights (must sum to 1.0)
AI4MH_WEIGHT_SENTIMENT=0.40
AI4MH_WEIGHT_VOLUME=0.35
AI4MH_WEIGHT_GEO=0.15
AI4MH_WEIGHT_TREND=0.10

# Data processing
AI4MH_MAX_POSTS=1000              # Maximum posts to keep
AI4MH_MIN_REGION_SAMPLE=10        # Minimum samples for region

# Storage
AI4MH_DB_PATH=ai4mh.db            # SQLite database location
```

## Running the Application

### Start Backend

```bash
cd backend
source .venv312/bin/activate  # Activate venv
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Start Frontend (in a new terminal)

```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v... ready in ... ms
➜  Local:   http://127.0.0.1:5173/
```

### Access the Application

- **API Dashboard**: http://localhost:8000/docs
- **Monitoring Dashboard**: http://localhost:5173
- **API Base URL**: http://localhost:8000/api

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd backend
source .venv312/bin/activate
pip install -r requirements.txt
```

### Issue: "npm command not found"

**Solution:**
```bash
# Install Node.js via Homebrew (macOS)
brew install node

# Or download from https://nodejs.org/
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn main:app --port 8001
```

### Issue: "Port 5173 already in use"

**Solution:**
```bash
# Kill process or use different port
npm run dev -- --port 5174
```

### Issue: "Permission denied" on .venv312/bin/activate

**Solution:**
```bash
chmod +x .venv312/bin/activate
source .venv312/bin/activate
```

### Issue: "CORS error" when accessing API

**Solution:**
- Verify backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Clear browser cache (Ctrl+Shift+Delete)

## Database

### SQLite Setup

The application uses SQLite with WAL mode for data persistence.

```bash
# Database is automatically created at backend/ai4mh.db
# No additional setup required

# To reset database:
cd backend
rm ai4mh.db
```

### Database Location

- **Default**: `backend/ai4mh.db`
- **Custom**: Set `AI4MH_DB_PATH` environment variable

## Testing Installation

### Run Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

Expected: 27 tests passing

### Run Full Health Check

```bash
bash scripts/full_health_check.sh
```

Expected: All checks passing ✓

## Next Steps

1. **Verify Installation**: See [VERIFICATION.md](SUBMISSION/VERIFICATION.md)
2. **Run Tests**: See [TESTING.md](SUBMISSION/TESTING.md)
3. **Understand Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
4. **Try the Dashboard**: Open http://localhost:5173

## Docker Setup (Optional)

If you prefer to run with Docker:

```bash
docker-compose -f SUBMISSION/deployment/docker-compose.yml up
```

See [DEPLOYMENT.md](SUBMISSION/DEPLOYMENT.md) for details.

---

**Installation completed successfully!** 🎉

You can now proceed to [VERIFICATION.md](SUBMISSION/VERIFICATION.md) to validate your setup.
