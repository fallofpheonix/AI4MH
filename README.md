# AI4MH: AI-Powered Behavioral Analysis for Mental Health Crisis Monitoring

AI4MH is a decision-support platform that converts online discussion signals into regional mental-health crisis indicators. It identifies shifts in distress-related discourse, providing high-confidence early warning signals for public health teams.

## 🚀 Key Features

- **Real-time Ingestion**: Processes synthetic mental-health discussion posts across 9 major regions.
- **NLP Enrichment**: Sentiment analysis (VADER) and crisis keyword detection.
- **Multi-Dimensional Scoring**: Aggregates sentiment intensity, volume spikes, geographic clustering, and trend acceleration.
- **Governance Gate**: Automated "Review Required" alerts triggered by score and confidence thresholds.
- **Audit Logging**: Full lifecycle tracking of alerts (Acknowledged, Dismissed, Resolved).
- **Monitoring Dashboard**: React-based visual interface for tracking regional health signals.

---

## 🏛 Project Architecture

### Data Flow
```text
Synthetic Post -> Enrichment (Sentiment/Keywords) -> Scoring (Regional Aggregation) 
-> Alert Logic (Threshold Gating) -> Persistence (SQLite) -> API (FastAPI) 
-> Dashboard (React)
```

### Repository Layout
- **`src/backend/`**: FastAPI application.
  - `app/api/`: Endpoint definitions and dependency wiring.
  - `app/core/`: Application configuration and service container.
  - `app/crud/`: Persistence layer (SQLite/In-Memory).
  - `app/schemas/`: Pydantic domain models.
  - `app/services/`: Core business logic (Ingestion, Scoring, Alerts).
- **`src/frontend/`**: React/Vite dashboard.
  - `src/components/`: Modular UI widgets and layout.
  - `src/hooks/`: Stateful orchestration and polling.
  - `src/pages/`: Page composition.
  - `src/services/`: API client and dashboard queries.
- **`scripts/`**: Automation and health checks.
- **`docs/`**: Project documentation.

---

## 🛠 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### Setup & Run
1. **Clone & Install**:
   ```bash
   git clone https://github.com/fallofpheonix/AI4MH.git
   cd AI4MH
   # Setup Backend
   python3 -m venv .venv312 && source .venv312/bin/activate
   pip install -r requirements.txt
   # Setup Frontend
   cd src/frontend && npm install
   ```

2. **Launch Services**:
   - **Backend**: `cd src/backend && uvicorn app.main:app --reload` (Runs on `http://localhost:8000`)
   - **Frontend**: `cd src/frontend && npm run dev` (Runs on `http://localhost:5173`)

### Verification
Run the full-stack health check to ensure everything is wired correctly:
```bash
bash scripts/full_health_check.sh
```

---

## 🔌 API Reference

Base URL: `http://localhost:8000/api/v1`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/ingest?n=30` | `POST` | Generate and process `n` synthetic posts. |
| `/posts` | `GET` | Retrieve latest processed posts. |
| `/scores` | `GET` | Get current regional crisis scores. |
| `/alerts` | `GET` | List active crisis alerts. |
| `/alerts/{id}/ack` | `POST` | Acknowledge an alert. |
| `/logs` | `GET` | Retrieve audit trail logs. |
| `/bias` | `GET` | View population and sample-size diagnostics. |


---

## 📊 Data & Scoring Logic

### Regional Coverage
We monitor 9 major hubs: `CA-LA`, `TX-HOU`, `NY-NYC`, `IL-CHI`, `AZ-PHX`, `PA-PHI`, `WV-CHA`, `KY-HAZ`, `OH-CHI`.

### Scoring Signals
1. **Sentiment Intensity**: Proportion of negative affect in regional discourse.
2. **Volume Spike**: Deviation from historical frequency baselines.
3. **Geo-Clustering**: Concentration of crisis-related language in specific regions.
4. **Trend Acceleration**: Rate of change in distress signals over time.

### Confidence Gating
An alert enters the **`review_required`** state ONLY if:
- `crisis_score >= 0.7`
- `confidence >= 0.6`
- `post_count >= 10`
- `bot_ratio < 0.2`

---

## 🛤 Roadmap
- [ ] **Data Realism**: Integrate replayable fixture datasets and windowed baselines.
- [ ] **Governance Hardening**: Multi-user authentication and operator audit trails.
- [ ] **Persistence Evolution**: Migrate to a fully normalized relational schema.
- [ ] **Extended Analytics**: Introduce longitudinal heatmaps and bias diagnostic views.

---

## ⚖️ Design Decisions & Constraints
- **White-Box Scoring**: Weighted formulas are used instead of opaque ML to ensure public-health explainability.
- **Human-in-the-Loop**: Automated alerts never escalate beyond "Review Required" without human interaction.
- **Sparse Data Handling**: Regions with low sample sizes (N < 20) are explicitly flagged in bias diagnostics.
- **Synthetic Foundation**: Current data is generated for demonstration; live API connectors are planned for future phases.

---

## 🤝 Contributing
Contributions are welcome! Please ensure:
1. API changes are reflected in Pydantic schemas.
2. New logic includes corresponding tests in `tests/backend`.
3. The `full_health_check.sh` passes before submitting a PR.
