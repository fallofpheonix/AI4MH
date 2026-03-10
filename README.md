# AI4MH Minimum Requirement Prototype

## Official Project Header

AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis [AI4MH (AI for Mental Health Crisis Monitoring)]

Google Summer of Code 2026 - Contributor Selection Task

Organization: Institute for Social Science Research (ISSR), The University of Alabama

Mentor: David M. White, MPH, MPA

Contact: dmwhite@ua.edu

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
2. Governance and Risk Controls
   - Explain how the system addresses:
     - Bot amplification or coordinated activity
     - Media-driven spikes
     - Rural underrepresentation or sparse data
   - Define escalation thresholds and human-in-the-loop processes.
   - Specify audit logging structure.
3. Governance Reflection (Short Section)
   - Identify the primary risk of premature deployment.
   - Identify the single most important safeguard.

## Submission Blueprint (3-4 Pages, Maximum)

Use exactly four sections in the written submission to stay within the page limit.

### 1) System Overview (about 1/2 page)

Include:
- Inputs: social posts, timestamps, location metadata, interaction metadata.
- Processing stages: collection -> preprocessing -> sentiment -> aggregation -> crisis scoring -> confidence -> escalation.
- Outputs: `CrisisScore(region, window)`, `ConfidenceScore`, `EscalationFlag`.
- Optional single architecture diagram.

### 2) Crisis Signal Design (Core Component)

Required signal families:
- Sentiment intensity.
- Volume spike detection.
- Geographic clustering.

Required methods:
- Minimum sample-size threshold.
- Smoothing/stabilization (for example EMA).
- Confidence/uncertainty estimate.
- Pseudocode for decision flow.

Example scoring form (illustrative):
- `score = w1*sentiment + w2*volume + w3*geo`
- `smoothed = alpha*score + (1-alpha)*prev`
- `if sample_size < N: low_confidence`

Note:
- Weight values in the document can be examples.
- Keep them explicitly separated from implementation constants in this repository.

### 3) Governance and Risk Controls

Address explicitly:
- Bot amplification / coordinated activity (detection + down-weighting/capping).
- Media-driven spikes (dampening when non-local amplification dominates).
- Rural underrepresentation / sparse data (window extension, confidence reduction, neighboring context policy).
- Escalation thresholds and human-in-the-loop gating.
- Audit logging schema with immutable decision trace.

Minimum escalation policy format:
- `<0.4`: no action
- `0.4-0.7`: monitoring
- `>0.7`: escalate to human review

### 4) Governance Reflection (short)

State:
- Primary premature-deployment risk (false escalation -> panic/resource misallocation).
- Single most important safeguard (mandatory human verification before action).

### Evaluator Focus

Evaluators prioritize:
- System-level reasoning.
- Instability/uncertainty awareness.
- Risk mitigation quality.
- Clear, constrained decision logic.

Avoid:
- Model-centric writeups without governance and decision policy.

Supporting templates:
- [3-4 Page Submission Template](docs/GSOC_submission_template.md)
- [Mentor Rejection Checklist](docs/mentor_rejection_checklist.md)

## Submission Requirements

- 3-4 pages maximum (excluding optional diagram).
- Optional single architecture diagram.
- Clear section headings required.
- Submit as a single PDF via the GSoC portal.
- Estimated time: 6-8 hours over one week.
- Work must be original.
- Use of generative AI tools must be disclosed.
- Plagiarized or template-based submissions will not be considered.

## Evaluation Criteria

- Systems thinking and architectural clarity.
- Responsible AI and governance awareness.
- Bias identification and mitigation strategy.
- Treatment of uncertainty and confidence modeling.
- Professional written communication.
- Strong submissions demonstrate constraint discipline, clear logic, and understanding of public-sector responsibility.

## Evaluation Criteria Interpretation (Technical)

### 1. Systems Thinking and Architectural Clarity

Evaluators expect a coherent end-to-end system, not isolated modeling.

Required evidence:
- Clear boundaries: inputs, processing stages, outputs, external dependencies.
- Layered pipeline: ingestion, preprocessing, feature extraction, scoring/inference, uncertainty, escalation policy, human review, audit logging.
- Component responsibilities and failure modes.
- Data flow or architecture diagram.

### 2. Responsible AI and Governance Awareness

Public-sector use requires explicit accountability controls.

Required evidence:
- Audit trail for score generation and human decisions.
- Human override and review thresholds.
- Explainability and traceability of escalation decisions.
- Assumption and model-update governance notes.

### 3. Bias Identification and Mitigation Strategy

Bias must be named and handled with measurable controls.

Required evidence:
- Bias sources: sampling, labeling, representation, model amplification.
- Mitigation actions: reweighting/normalization/filtering and group-level checks.
- Monitoring outputs that detect performance disparity over time.

### 4. Treatment of Uncertainty and Confidence Modeling

Predictions must include uncertainty-aware decision logic.

Required evidence:
- Confidence score or uncertainty proxy attached to each escalation decision.
- Deferral rule (for example low confidence -> human review).
- Threshold rationale tied to risk tolerance.

### 5. Professional Written Communication

The document must read like an institutional engineering design note.

Required evidence:
- Structured sections with concise technical language.
- Clear definitions, formulas, and thresholds.
- Diagram/table support where useful.
- No marketing language or vague claims.

### Strong Submission Characteristics

- Constraint discipline: data, operational, ethical, and deployment limits are explicit.
- Clear logic: each method has rationale and trade-off acknowledgment.
- Public-sector responsibility: fairness, auditability, reversibility, and human oversight are non-negotiable.

### Common Failure Patterns

- Describing only model architecture without full decision pipeline.
- Missing uncertainty handling.
- Vague bias statements without mechanisms or metrics.
- No governance thresholds or review policy.
- Non-technical or promotional writing style.

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
