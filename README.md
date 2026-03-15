# AI4MH: AI-Powered Crisis Monitoring

AI4MH (AI for Mental Health) is a public health monitoring system designed to detect emerging suicide, substance use, and mental health crises in real time using NLP and geospatial analysis.

## 🚀 Key Features
- **Behavioral Analysis**: Detects crisis-related language and distress escalation patterns.
- **Geospatial Hotspots**: Real-time and longitudinal heatmaps of crisis trends across regions.
- **Governance-Ready**: Mandatory human-in-the-loop escalation logic with bot-filtering.
- **Explainable Scoring**: Weighted crisis indicators for transparent decision support.

## 🛠 Project Architecture
The system consists of a **FastAPI backend** for high-performance scoring and a **React frontend** for regional monitoring.

```text
Synthetic Posts -> NLP Enrichment -> Regional Aggregation -> Crisis Scoring -> Human Alerting
```

## 📥 Installation

### Prerequisites
- Python 3.10+
- Node.js & npm

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📈 Usage
1. Start the backend and frontend servers.
2. Access the operator dashboard at `http://localhost:5173`.
3. Monitor real-time logs and regional score escalations.
4. Use the `biases` panel to audit data quality and geographic representation.

## 🤝 Contribution
Contributions are welcome! Please see the [GSoC 2026 Proposal](docs/gsoc_proposal.md) for the roadmap and technical methodology. 
- **Tests**: Run `scripts/full_health_check.sh` before submitting PRs.
- **Contact**: human-ai@cern.ch

## 📜 License
MIT License. See `LICENSE` for details.
