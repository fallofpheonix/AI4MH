# Mentor Rejection Checklist (Pre-Submission)

Use this checklist before submitting the 3-4 page PDF.

## 1) Problem Definition Clarity

- Problem is defined in one clear paragraph.
- Scope is signal detection (not exact event prediction).
- Inputs and outputs are explicit.
- Flow is explicit: `Input -> Signal Detection -> Crisis Score -> Escalation`.

## 2) Architecture Completeness

Required components are all present:

- Data Collection
- Preprocessing
- Feature Extraction
- Signal Aggregation
- Crisis Scoring
- Confidence Estimation
- Escalation Decision
- Human Review
- Audit Logging

Reject pattern: `Data -> Model -> Output` only.

## 3) Crisis Signal Design Quality

- Includes sentiment intensity, volume spike, geographic clustering.
- Includes weighted mathematical aggregation.
- Uses explicit formula (not qualitative description only).

## 4) Minimum Sample Size Constraint

- `MIN_SAMPLE_SIZE` is explicitly defined.
- Logic handles sparse sample: `if posts < MIN_SAMPLE_SIZE: insufficient_data`.

## 5) Stabilization Mechanism

- Includes smoothing method (EMA/rolling/time-window).
- Avoids raw volatile spike decisions.

## 6) Confidence / Uncertainty Modeling

- Outputs both `crisis_score` and `confidence`.
- Confidence depends on sample size, variance, and geographic coverage.

## 7) Manipulation Risk Handling

- Addresses bot amplification.
- Addresses coordinated campaigns.
- Addresses media amplification.
- Includes mitigation controls (down-weighting/capping/discounting).

## 8) Rural Data Bias Handling

- Defines sparse-region strategy (window extension, neighboring context, lower confidence).

## 9) Escalation Policy

- Defines explicit thresholds for escalation.
- Includes non-escalation states (monitor/no action).

## 10) Human-in-the-Loop Design

- Explicit analyst verification workflow is present.
- System does not trigger automatic public intervention.

## 11) Audit Logging

Required fields in logs:

- `timestamp`
- `region`
- `crisis_score`
- `confidence`
- `sample_size`
- `decision`
- `reviewer_id`

## 12) Governance Reflection Section

- States primary premature-deployment risk.
- States most important safeguard.
- Focuses on governance/public trust risk, not only technical bugs.

## 13) Writing Quality

- Clear headings.
- Short technical paragraphs.
- Consistent terminology.
- No marketing language or vague claims.

## Final PDF Gate

Must include:

1. System Overview
2. Architecture Diagram
3. Crisis Signal Design
4. Governance and Risk Controls
5. Governance Reflection

Length limit: 3-4 pages.
