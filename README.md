# AI4MH (AI for Mental Health Crisis Monitoring)

## Official Problem Statement

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis [AI4MH (AI for Mental Health Crisis Monitoring)]

Google Summer of Code 2026 - Contributor Selection Task  
Organization: Institute for Social Science Research (ISSR), The University of Alabama  
Mentor: David M. White, MPH, MPA  
Program listing contact: dmwhite@ua.edu  
Application contact route: human-ai@cern.ch

## Description

Public health agencies and crisis service providers face challenges in detecting and addressing emerging suicide, substance use, and mental health crises in real time. Traditional public health data sources such as hospital admissions, overdose reports, and crisis hotline statistics are valuable but lag behind the actual emergence of crises within communities.

This project proposes an AI-driven public health monitoring system that integrates:

- Behavioral tracking: analyzing how individuals engage with crisis-related content to identify patterns of distress escalation
- Crisis-related language analysis: detecting keywords, slang, and coded language used to discuss mental health struggles, suicidality, and substance use
- Geospatial crisis mapping with longitudinal trend analysis: identifying where distress-related discussions are concentrated and tracking changes over time to detect increasing crisis trends within specific geographic regions

By collecting and analyzing this data over time, the system provides early-warning indicators of worsening mental health conditions and emerging substance use risks in communities. These insights help service providers predict areas of growing crisis and proactively allocate resources where needed most.

## Duration

Total project length: 175 hours (Medium)

## Task Ideas

- Monitor crisis-related discussions and communication patterns:
  - Develop a crisis lexicon for tracking explicit and coded language related to mental health and substance use
  - Use AI-driven sentiment analysis and topic modeling to track changes over time
- Track engagement behaviors with crisis content:
  - Analyze how users interact with crisis-related posts to identify distress escalation trends
  - Evaluate whether mental health outreach is effectively reaching communities in need
- Develop location-based crisis mapping and longitudinal analysis:
  - Use NLP and metadata extraction to geotag crisis-related discussions
  - Generate real-time and historical heatmaps of crisis trends
- Implement a public health dashboard for crisis monitoring:
  - Build an interactive visualization tool to display trends and insights
  - Provide analytics for public health agencies and service providers to refine outreach efforts

## Expected Results

- An AI-driven crisis detection system that identifies suicide, substance use, and mental health risks by analyzing social media discussions and engagement behaviors over time
- An interactive dashboard with real-time and longitudinal crisis heatmaps to help mental health service providers identify trends and direct outreach efforts effectively
- Predictive indicators for crisis escalation that enable public health agencies to preemptively deploy crisis intervention resources
- A framework for evaluating the long-term effectiveness of crisis outreach campaigns and adjusting intervention strategies accordingly

## Requirements

- Strong Python programming skills
- Experience with NLP frameworks (spaCy, NLTK, or Hugging Face Transformers)
- Familiarity with text-analysis ML methods (for example BERT, LDA topic modeling, VADER sentiment)
- Data visualization experience (Plotly, D3.js, or Matplotlib)
- Experience with geospatial analysis/GIS tools (GeoPandas, Folium, Leaflet.js)
- Understanding of public health or behavioral crisis indicators is a plus

## Project Difficulty Level

Intermediate to Advanced - suitable for students with prior experience in NLP, social media analysis, and geospatial data visualization.

## Tests

Please use the official project test link provided by the program listing.

## Mentors and Contact

- David M. White (University of Alabama)
- Hailey Richardson (University of Alabama)
- Dr. Andrea Underhill (University of Alabama)

Do not contact mentors directly by email. Use `human-ai@cern.ch` with project title, CV, and test results.

## Corresponding Project

ISSR

## Participating Organizations

Alabama

## Purpose of This Task

This assessment evaluates architectural thinking, responsible AI reasoning, and communication clarity. It is designed to reflect the type of systems-level work required during GSoC.

This is not a model-building competition.

## Project Context

AI4MH has completed its prototype phase (data ingestion, sentiment analysis, geocoding, dashboard visualization).

The next phase focuses on governance readiness. The system must operate in a public health environment where reliability, auditability, bias mitigation, and human oversight are mandatory.

This task simulates the type of design and reasoning work expected during the GSoC coding period.

## Scenario

AI4MH monitors aggregated public sentiment across Alabama counties.

Within a 72-hour window, three counties show a significant increase in negative sentiment associated with depression and suicide-related language.

The State Behavioral Health Office asks: "Is this a credible signal requiring attention?"

Design the logic layer that determines whether escalation to human review is warranted.

## Required Deliverables

1. Crisis Signal Design (Core Component)
- Design a structured crisis scoring framework integrating:
  - Sentiment intensity
  - Volume spike detection
  - Geographic clustering
- Your framework must include:
  - Minimum sample size threshold
  - Smoothing or stabilization method
  - Confidence or uncertainty estimate
- Pseudocode is acceptable. Advanced machine learning is not required.

2. Governance & Risk Controls
- Explain how the system addresses:
  - Bot amplification or coordinated activity
  - Media-driven spikes
  - Rural underrepresentation or sparse data
- Define escalation thresholds and human-in-the-loop processes.
- Specify audit logging structure.

3. Governance Reflection (Short Section)
- Identify the primary risk of premature deployment.
- Identify the single most important safeguard.

## Submission Requirements

- 3-4 pages maximum (excluding optional diagram)
- Optional single architecture diagram
- Clear section headings required
- Submit as a single PDF via the GSoC portal
- Estimated time: 6-8 hours over one week
- Work must be original
- Use of generative AI tools must be disclosed
- Plagiarized or template-based submissions will not be considered

## Evaluation Criteria

Submissions will be evaluated on:

- Systems thinking and architectural clarity
- Responsible AI and governance awareness
- Bias identification and mitigation strategy
- Treatment of uncertainty and confidence modeling
- Professional written communication

Strong submissions demonstrate constraint discipline, clear logic, and understanding of public-sector responsibility.

## Prototype Implementation in This Repository

Implemented components:

- FastAPI backend for ingestion, NLP enrichment, scoring, governance, alerts, and audit
- React frontend dashboard connected to backend APIs
- Crisis signal and governance engines
- JSON/CSV export endpoints for analysis

Core API endpoints:

- `GET /api/posts?limit=60`
- `GET /api/scores`
- `GET /api/alerts`
- `POST /api/alerts/{id}/review`
- `GET /api/audit`
- `POST /api/ingest?n=30`
- `GET /api/export/json?kind=posts|scores|alerts|audit`
- `GET /api/export/csv?kind=posts|scores|alerts|audit`

## Run

Backend:

```bash
cd backend
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Quick validation:

```bash
./scripts/full_health_check.sh --no-start
```
