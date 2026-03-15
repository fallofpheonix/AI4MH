# AI4MH: AI-Powered Crisis Monitoring

AI4MH (AI for Mental Health) is a public health monitoring system designed to detect emerging suicide, substance use, and mental health crises in real time using NLP and geospatial analysis.

## 🚀 Key Features
- **Behavioral Analysis**: Detects crisis-related language and distress escalation patterns.
- **Geospatial Hotspots**: Real-time and longitudinal heatmaps of crisis trends across regions.
- **Governance-Ready**: Mandatory human-in-the-loop escalation logic with bot-filtering.
- **Explainable Scoring**: Weighted crisis indicators for transparent decision support.
- **Alert Lifecycle**: Full `review_required → acknowledged → resolved/dismissed` workflow.
- **Modular Pipeline**: Independent, testable stages for ingest, enrichment, scoring, and alerting.

## 🛠 Project Architecture
The system consists of a **FastAPI backend** with a modular pipeline and a **React frontend** for regional monitoring.

```text
Synthetic Posts
  → NLP Enrichment  (pipeline/enrich.py)
  → Aggregation     (pipeline/aggregate.py)
  → Crisis Scoring  (pipeline/score.py)
  → Alert Gen       (pipeline/alert.py)
  → HTTP API        (main.py)
  → React Dashboard (frontend/src/App.jsx)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full module breakdown.

## 📥 Installation

### Prerequisites
- Python 3.10+
- Node.js & npm

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## ⚙️ Configuration

All backend constants can be overridden via environment variables with the `AI4MH_` prefix:

```bash
export AI4MH_ALERT_THRESHOLD=0.80
export AI4MH_MAX_POSTS=1000
```

See `backend/config.py` for the full list of settings.

## 📈 Usage
1. Start the backend and frontend servers.
2. Access the operator dashboard at `http://localhost:5173`.
3. Monitor real-time logs and regional score escalations.
4. Use the `biases` panel to audit data quality and geographic representation.
5. Acknowledge, dismiss, or resolve alerts via `POST /api/alerts/{id}/ack|dismiss|resolve`.

## 🧪 Tests

```bash
cd backend
python -m pytest tests/ -v
```

Tests cover:
- Scoring signal functions (`sentiment_intensity`, `volume_spike`, `geo_cluster`, `trend_acceleration`, `confidence`)
- Region-level scoring and `score_all_regions` aggregation
- All API endpoints including alert lifecycle transitions

## 🤝 Contribution
Contributions are welcome! Please see the [GSoC 2026 Proposal](docs/gsoc_proposal.md) for the roadmap and technical methodology. 
- **Tests**: Run `scripts/full_health_check.sh` before submitting PRs.
- **Contact**: human-ai@cern.ch

## 📜 License
MIT License. See `LICENSE` for details.
