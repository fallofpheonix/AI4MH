# Testing Guide

Complete guide to running AI4MH tests and validating functionality.

## Test Structure

```
backend/tests/
├── conftest.py          # Shared pytest fixtures
├── test_scoring.py      # Scoring function tests (15 tests)
└── test_api.py          # API endpoint tests (12 tests)
```

**Total Tests:** 27  
**Expected Duration:** ~30 seconds

## Prerequisites

- Backend virtual environment activated
- All dependencies installed
- Python 3.10+

## Running Tests

### Run All Tests

```bash
cd backend
source .venv312/bin/activate
python -m pytest tests/ -v
```

Expected output:
```
tests/test_scoring.py::test_sentiment_intensity_positive PASSED
tests/test_scoring.py::test_sentiment_intensity_negative PASSED
...
======================== 27 passed in X.XXs ========================
```

### Run Specific Test File

```bash
# Scoring tests only
python -m pytest tests/test_scoring.py -v

# API tests only
python -m pytest tests/test_api.py -v
```

### Run Specific Test

```bash
# Run one test
python -m pytest tests/test_scoring.py::test_sentiment_intensity_positive -v
```

### Run with Coverage

```bash
pip install pytest-cov
python -m pytest tests/ --cov=backend --cov-report=html
```

Generates: `htmlcov/index.html` with coverage report

## Test Details

### Scoring Tests (15 tests)

Located in `tests/test_scoring.py`

#### Signal Function Tests
- `test_sentiment_intensity_positive` - High sentiment scores
- `test_sentiment_intensity_negative` - Low sentiment scores
- `test_sentiment_intensity_mixed` - Mixed sentiment posts
- `test_volume_spike_above_baseline` - Volume increase detection
- `test_volume_spike_below_baseline` - Volume decrease detection
- `test_geo_cluster_concentrated` - Geographic concentration
- `test_geo_cluster_sparse` - Geographic distribution
- `test_trend_acceleration_rising` - Trend increase detection
- `test_trend_acceleration_stable` - Stable trend handling
- `test_confidence_high_sample` - High sample confidence
- `test_confidence_low_sample` - Low sample penalty
- `test_confidence_bot_ratio` - Bot activity penalty

#### Aggregation Tests
- `test_score_region_returns_score` - Region scoring
- `test_score_all_regions_partial_update` - Partial region updates
- `test_score_all_regions_sorting` - Score ranking

### API Tests (12 tests)

Located in `tests/test_api.py`

#### Endpoint Tests
- `test_get_posts_returns_posts` - GET /api/posts
- `test_get_scores_returns_scores` - GET /api/scores
- `test_get_alerts_returns_alerts` - GET /api/alerts
- `test_post_alert_ack` - POST /api/alerts/{id}/ack
- `test_post_alert_dismiss` - POST /api/alerts/{id}/dismiss
- `test_post_alert_resolve` - POST /api/alerts/{id}/resolve
- `test_get_logs` - GET /api/logs
- `test_get_bias` - GET /api/bias

#### Integration Tests
- `test_ingest_pipeline_end_to_end` - Full pipeline execution
- `test_alert_lifecycle` - Complete alert workflow
- `test_concurrent_ingestion` - Parallel data handling
- `test_error_handling` - Graceful failure modes

## Running Health Check

The health check script validates the complete stack:

```bash
bash scripts/full_health_check.sh
```

**Validates:**
1. Backend server startup
2. Frontend server startup
3. API health check
4. Database connectivity
5. JSON response validation
6. Bias diagnostics

## Continuous Testing

### Using pytest-watch

```bash
pip install pytest-watch
ptw tests/
```

Automatically reruns tests when files change.

### Using GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest tests/ -v
```

## Test Output Examples

### Successful Run

```
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.0.2, py-1.13.0, pluggy-1.6.0 -- 
/Users/fallofpheonix/Project/Human AI/AI4MH/backend/.venv312/bin/python3
cachedir: .pytest_cache
rootdir: /Users/fallofpheonix/Project/Human AI/AI4MH/backend
collected 27 items

tests/test_scoring.py::test_sentiment_intensity_positive PASSED        [  3%]
tests/test_scoring.py::test_sentiment_intensity_negative PASSED        [  7%]
tests/test_scoring.py::test_sentiment_intensity_mixed PASSED           [ 11%]
tests/test_scoring.py::test_volume_spike_above_baseline PASSED         [ 15%]
tests/test_scoring.py::test_volume_spike_below_baseline PASSED         [ 19%]
tests/test_scoring.py::test_geo_cluster_concentrated PASSED            [ 23%]
tests/test_scoring.py::test_geo_cluster_sparse PASSED                  [ 26%]
tests/test_scoring.py::test_trend_acceleration_rising PASSED           [ 30%]
tests/test_scoring.py::test_trend_acceleration_stable PASSED           [ 33%]
tests/test_scoring.py::test_confidence_high_sample PASSED              [ 37%]
tests/test_scoring.py::test_confidence_low_sample PASSED               [ 40%]
tests/test_scoring.py::test_confidence_bot_ratio PASSED                [ 44%]
tests/test_scoring.py::test_score_region_returns_score PASSED          [ 48%]
tests/test_scoring.py::test_score_all_regions_partial_update PASSED   [ 51%]
tests/test_scoring.py::test_score_all_regions_sorting PASSED           [ 55%]
tests/test_api.py::test_get_posts_returns_posts PASSED                 [ 59%]
tests/test_api.py::test_get_scores_returns_scores PASSED               [ 63%]
tests/test_api.py::test_get_alerts_returns_alerts PASSED               [ 66%]
tests/test_api.py::test_post_alert_ack PASSED                          [ 70%]
tests/test_api.py::test_post_alert_dismiss PASSED                      [ 74%]
tests/test_api.py::test_post_alert_resolve PASSED                      [ 77%]
tests/test_api.py::test_get_logs PASSED                                [ 81%]
tests/test_api.py::test_get_bias PASSED                                [ 85%]
tests/test_api.py::test_ingest_pipeline_end_to_end PASSED              [ 88%]
tests/test_api.py::test_alert_lifecycle PASSED                         [ 92%]
tests/test_api.py::test_concurrent_ingestion PASSED                    [ 96%]
tests/test_api.py::test_error_handling PASSED                          [100%]

============================== 27 passed in 0.32s ==============================
```

## Debugging Failed Tests

### Verbose Output

```bash
python -m pytest tests/ -v -s
```

The `-s` flag shows print statements during tests.

### Single Failing Test

```bash
python -m pytest tests/test_scoring.py::test_sentiment_intensity_positive -vv
```

The `-vv` flag increases verbosity.

### With Tracebacks

```bash
python -m pytest tests/ --tb=long
```

### Stop on First Failure

```bash
python -m pytest tests/ -x
```

## Test Fixtures

All tests use shared fixtures from `conftest.py`:

```python
@pytest.fixture
def sample_posts():
    """Generate sample posts for testing"""
    ...

@pytest.fixture
def test_store():
    """Create in-memory test store"""
    ...

@pytest.fixture
def test_client():
    """Create test API client"""
    ...
```

## Mocking Database

Tests use in-memory SQLite for speed:

```python
def test_example(test_store):
    # test_store is :memory: database
    posts = test_store.get_posts()
    assert len(posts) == 0
```

## Performance Testing

### Timing Tests

```bash
python -m pytest tests/ -v --durations=10
```

Shows: 10 slowest tests

### Profile a Test

```bash
pip install pytest-profile
python -m pytest tests/ --profile
```

## Before Submission

### Pre-Submission Checklist

- [ ] All tests passing locally
- [ ] Health check passes
- [ ] Coverage > 80%
- [ ] No warnings or deprecations
- [ ] Documentation updated
- [ ] Code formatters applied (if applicable)

### Run Final Verification

```bash
# 1. Run tests
python -m pytest tests/ -v

# 2. Run health check
bash scripts/full_health_check.sh

# 3. Check code quality
cd ..
pylint backend/main.py 2>/dev/null || echo "pylint not installed (optional)"

# 4. Verify documentation
ls -la docs/*.md
```

## Continuous Integration

### GitHub Actions Workflow

See `.github/workflows/test.yml` for CI configuration.

### Local Pre-commit Hook

Create `backend/.git/hooks/pre-commit`:

```bash
#!/bin/bash
python -m pytest tests/ -q || exit 1
```

Make executable:
```bash
chmod +x backend/.git/hooks/pre-commit
```

## Test Results Tracking

### Generate Report

```bash
python -m pytest tests/ --html=report.html --self-contained-html
```

Opens: `report.html` in browser

---

**All tests completed!** 🎉

Next: Read [SUBMISSION/docs/FEATURES.md](SUBMISSION/docs/FEATURES.md) for feature checklist.
