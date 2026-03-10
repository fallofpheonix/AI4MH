# AI4MH Minimum Requirement Prototype

## Official Project Header

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis [AI4MH (AI for Mental Health Crisis Monitoring)]

Google Summer of Code 2026 - Contributor Selection Task

Organization: Institute for Social Science Research (ISSR), The University of Alabama

Mentor: David M. White, MPH, MPA

Contact: dmwhite@ua.edu

## Project Title

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis

## Description

Public health agencies and crisis service providers face challenges in detecting and addressing emerging suicide, substance use, and mental health crises in real time. Traditional public health data sources such as hospital admissions, overdose reports, and crisis hotline statistics are valuable but lag behind the actual emergence of crises within communities.

This project proposes an AI-driven public health monitoring system that integrates:

- Behavioral tracking: analyzing how individuals engage with crisis-related content to identify patterns of distress escalation.
- Crisis-related language analysis: detecting keywords, slang, and coded language used to discuss mental health struggles, suicidality, and substance use.
- Geospatial crisis mapping with longitudinal trend analysis: identifying where distress-related discussions are concentrated and tracking changes over time to detect increasing crisis trends within specific geographic regions.

By collecting and analyzing this data over time, the system provides early-warning indicators of worsening mental health conditions and emerging substance use risks in communities. These insights help service providers predict areas of growing crisis and proactively allocate resources where needed most.

## Duration

Total project length: 175 hours (Medium).

## Task Ideas

- Monitor crisis-related discussions and communication patterns:
  - Develop a crisis lexicon for tracking explicit and coded language related to mental health and substance use.
  - Use AI-driven sentiment analysis and topic modeling to track changes over time.
- Track engagement behaviors with crisis content:
  - Analyze how users interact with crisis-related posts to identify distress escalation trends.
  - Evaluate whether mental health outreach is effectively reaching communities in need.
- Develop location-based crisis mapping and longitudinal analysis:
  - Use NLP and metadata extraction to geotag crisis-related discussions.
  - Generate real-time and historical heatmaps of crisis trends.
- Implement a public health dashboard for crisis monitoring:
  - Build an interactive visualization tool to display trends and insights.
  - Provide analytics for public health agencies and service providers to refine outreach efforts.

## Expected Results

- An AI-driven crisis detection system that identifies suicide, substance use, and mental health risks by analyzing social media discussions and engagement behaviors over time.
- An interactive dashboard with real-time and longitudinal crisis heatmaps to help mental health service providers identify trends and direct outreach efforts effectively.
- Predictive indicators for crisis escalation that enable public health agencies to preemptively deploy crisis intervention resources.
- A framework for evaluating the long-term effectiveness of crisis outreach campaigns and adjusting intervention strategies accordingly.

## Requirements

- Strong Python programming skills.
- Experience with Natural Language Processing (NLP) frameworks (spaCy, NLTK, or Hugging Face Transformers).
- Familiarity with machine learning models for text analysis (for example BERT, LDA topic modeling, VADER for sentiment analysis).
- Data visualization experience with Plotly, D3.js, or Matplotlib.
- Experience with geospatial data analysis and GIS mapping tools (for example GeoPandas, Folium, Leaflet.js).
- Understanding of public health or behavioral crisis indicators is a plus.

## Project Difficulty Level

Intermediate to Advanced - suitable for students with prior experience in NLP, social media analysis, and geospatial data visualization.

## MVP Status

This repository satisfies the minimum implementation target for the AI4MH GSoC task:
- Working backend service
- Working frontend dashboard
- Connected ingestion -> NLP -> scoring -> governance -> alert review -> audit flow

## Minimum Requirement Checklist

- [x] Crisis signal scoring with weighted factors:
  - sentiment intensity (0.35)
  - volume spike (0.30)
  - geographic clustering (0.20)
  - trend acceleration (0.15)
- [x] Sample-size gate (`min_posts`, tier-adjusted by population)
- [x] Stabilization/smoothing logic (`trend_accel` split-window, capped score components)
- [x] Confidence estimate (volume x consistency x coverage)
- [x] Governance controls:
  - bot filtering and bot ratio threshold
  - media-event dampening hook
  - rural underrepresentation normalization
- [x] Human-in-the-loop escalation and review states
- [x] Audit log for score evaluation, alert creation, and analyst review actions

## System Layout

- `backend/main.py`: FastAPI API
- `backend/ingest_posts.py`: synthetic ingestion pipeline
- `backend/nlp_processing.py`: VADER sentiment + crisis lexicon detection
- `backend/crisis_scoring.py`: weighted regional score + escalation gates
- `backend/governance_filters.py`: risk controls and normalization
- `backend/alert_engine.py`: alert lifecycle + audit logging
- `frontend/src/App.jsx`: operational dashboard

## Run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API

- `GET /api/posts?limit=60`
- `GET /api/scores`
- `GET /api/alerts`
- `POST /api/alerts/{id}/review`
- `GET /api/audit`
- `POST /api/ingest?n=30`

## Scope Limits (Intentional)

- In-memory storage only (no database)
- Simulated posts, not live platform ingestion
- Deterministic heuristic logic over advanced ML models

This scope is intentional for minimum requirement compliance.
