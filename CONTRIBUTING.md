# Contributing to AI4MH

Thank you for your interest in contributing to AI4MH. This project is dedicated to building robust, governance-first behavioral analysis tools for mental health crisis monitoring.

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+ (for dashboard)
- **Git**: For version control

### Local Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/fallofpheonix/AI4MH.git
   cd AI4MH
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**:
   ```bash
   cd ../frontend
   npm install
   ```

## 🛠 Development Workflow

### Running the Services

- **Backend (FastAPI)**: `cd backend && uvicorn main:app --reload`
- **Frontend (React)**: `cd frontend && npm run dev`

### Repository Standards

- **Determinism**: Every signal extraction and scoring component must be deterministic.
- **Explainability**: New features must include audit logging and explainability hooks.
- **Safety**: Do not implement automated crisis intervention; all high-risk signals must be gated for human review.

## 📝 Documentation Rules

Always update the following if your changes affect the core logic or API:
- `README.md`: For high-level features and setup.
- `ROADMAP.md`: If adding or shifting major milestones.
- `GSoC_2026_Proposal_fallofpheonix.md`: If the core technical design or evaluation plan evolves.

## 🧪 Validation Before Pull Request

Ensure your changes do not break the existing verification suite:

1. **Backend Tests**: `cd backend && pytest`
2. **Frontend Build**: `cd frontend && npm run build`
3. **Health Check**: `bash scripts/full_health_check.sh`

---

*For technical deep-dives, please refer to the [GSoC 2026 Proposal](GSoC_2026_Proposal_fallofpheonix.md).*
