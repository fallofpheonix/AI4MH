# AI4MH Development Roadmap (GSoC 2026)

This roadmap outlines the 12-week development cycle for the **AI-Powered Behavioral Analysis in Mental Health Crisis Monitoring** project. The focus is on building a credible, uncertainty-aware signal detection framework that is safe for public health deployment.

## 🚀 Execution Principle (Non-Negotiable)
Development follows a deterministic logic to ensure systems-level reliability:
**Data Ingestion → Signal Extraction → Credibility Modeling (χ) → Threat Filtering → Decision Engine → Evaluation**

---

## 📅 Timeline & Milestones

### Phase 1: Community Bonding (May 2026)
- **Goal**: Finalize design decisions and environment setup.
- [x] Set up development environment and study existing AI4MH pipeline.
- [ ] Finalize χ formulation and threat-filtering metrics.
- [ ] Align on signal weights and escalation thresholds with mentors.

### Phase 2: Data Pipeline & Preprocessing (Weeks 1-2)
- **Goal**: Create a deterministic, replayable data stream.
- [ ] Implement ingestion module for timestamped text streams.
- [ ] Build replayable dataset loader for synthetic/historical data.
- [ ] Add preprocessing: deduplication, language filtering, and region mapping.

### Phase 3: Signal Extraction Layer (Weeks 3)
- **Goal**: Convert raw text into measurable regional signals.
- [ ] Implement VADER sentiment scoring and crisis keyword detection.
- [ ] Compute regional post volume and velocity metrics.
- [ ] Apply Exponential Moving Average (EMA) smoothing to reduce jitter.

### Phase 4: Credibility Modeling (χ) (Weeks 4)
- **Goal**: Stabilize signals under sparsity and variance.
- [ ] **Sample Stability**: Implement $\min(1.0, \sqrt{N\_posts / k})$ scaling.
- [ ] **Temporal Consistency**: Comparison of regional spikes vs. historical baselines.
- [ ] **Spatial Support**: Basic neighbor averaging/Moran's I correlation.

### Phase 5: Threat Filtering (Weeks 5)
- **Goal**: Detect and suppress non-organic or adversarial signals.
- [ ] Implement **Lexical Entropy** calculation for bot detection.
- [ ] Add **URL Density** detection to filter media-driven noise.
- [ ] Normalize threat scores to adjust the final credible signal index.

### Phase 6: Decision Engine & Escalation (Weeks 6)
- **Goal**: Convert calibrated signals into safe, human-ready actions.
- [ ] Combine χ, sentiment scores, and threat filters into the final **Credible Signal Index**.
- [ ] Implement threshold-based escalation logic (Monitoring → Review → Priority).
- [ ] Enforce **Confidence Gating** for all Level 2+ alerts.

### Phase 7: Evaluation Framework (Weeks 7)
- **Goal**: Validate system reliability under adversarial conditions.
- [ ] Create synthetic test scenarios (bot injection, media-driven spikes, sparse regions).
- [ ] Calculate **Precision @ 75% Recall** and False Positive Rates.
- [ ] Generate a comprehensive Calibration and Robustness report.

### Phase 8: Governance & Audit Logging (Weeks 8)
- **Goal**: Ensure full transparency and explainability.
- [ ] Implement structured audit logging for every ingestion cycle.
- [ ] Build explainability breakdowns (χ components, threat indicators) for the dashboard.
- [ ] Finalize documentation and GSoC project report.

---

## 🛠 Core Deliverables
1.  **Credible Signal Pipeline**: End-to-end service from raw posts to escalation decisions.
2.  **The Reliability Engine (χ)**: A standalone module for uncertainty-aware scoring.
3.  **Threat Filter Suite**: Bot and media-noise detection tools.
4.  **Audit Logs & Explainability API**: REST endpoints providing the "Why" behind every alert.
5.  **Technical Documentation**: Detailed system design and evaluation benchmarks.
