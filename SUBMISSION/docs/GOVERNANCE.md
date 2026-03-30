# Governance Notes

AI4MH is a decision-support demo. It is not an autonomous intervention system.

## Operating Model

- The system ingests synthetic posts and computes region scores.
- Alerts are created in `review_required` state only.
- Human operators must decide whether to acknowledge, dismiss, or resolve an alert.
- All transitions are appended to the log stream.

## Current Safeguards

### Explainability

- Scoring is a weighted white-box calculation.
- Alert payloads include `score_breakdown`.
- Alert payloads include `evidence_post_ids`.

### Bias Visibility

- The `/api/v1/bias` endpoint exposes population-tier diagnostics.
- Region rows include `low_sample_flag`.
- Scores expose `confidence` independently from `crisis_score`.

### Manipulation Resistance

- Bot traffic lowers confidence through `bot_ratio`.
- All-bot regions are dropped from scoring.

### Auditability

- Ingest cycles append `ingest_completed` events.
- Alert transitions append `alert_status_changed` events.
- Alerts retain creation and update timestamps.

## Operational Constraints

- Data is synthetic; production claims cannot be made from this repository alone.
- No user identity, approval workflow, or per-operator attribution is implemented.
- No access control or encrypted secret management layer is present.

## Recommended Deployment Controls

If this system is adapted for real deployment, add:

- authentication and role-based access control
- operator identity on alert transitions
- retention and deletion policies
- documented review procedures
- threshold change management
- incident response and audit review workflow
