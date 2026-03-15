---
layout: default
title: AI4MH (AI for Mental Health Crisis Monitoring)
---

<div class="container py-4">
  <div class="row">
    <div class="col-12">
      <h1 class="display-6 fw-bold mb-2">AI4MH (AI for Mental Health Crisis Monitoring)</h1>
      <p class="lead mb-1">AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Trend Analysis</p>
      <p class="text-muted mb-4">Google Summer of Code 2026 · Institute for Social Science Research (ISSR), The University of Alabama</p>
    </div>
  </div>

  <div class="row g-3 mb-4">
    <div class="col-md-4">
      <div class="card h-100">
        <div class="card-body">
          <h2 class="h6 card-title">Project Difficulty</h2>
          <p class="card-text mb-0">Intermediate to Advanced</p>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card h-100">
        <div class="card-body">
          <h2 class="h6 card-title">Estimated Duration</h2>
          <p class="card-text mb-0">175 hours (Medium)</p>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card h-100">
        <div class="card-body">
          <h2 class="h6 card-title">Participating Organization</h2>
          <p class="card-text mb-0">Alabama</p>
        </div>
      </div>
    </div>
  </div>

  <div class="row">
    <div class="col-lg-8">
      <section class="mb-4">
        <h2 class="h4">Problem</h2>
        <p>Public health teams need earlier signals of suicide, substance-use, and mental-health crises than hospital records, overdose reports, and hotline summaries can provide. AI4MH addresses that latency gap by turning public online discussion into structured regional indicators for analyst review.</p>
      </section>

      <section class="mb-4">
        <h2 class="h4">What the System Does</h2>
        <ul>
          <li>Detects crisis-related language, including explicit and coded expressions of distress.</li>
          <li>Tracks regional changes in negative sentiment and crisis-related discussion volume over time.</li>
          <li>Aggregates signals by geography to identify localized trend escalation.</li>
          <li>Routes only qualified signals to human review rather than automating response.</li>
        </ul>
      </section>

      <section class="mb-4">
        <h2 class="h4">Technical Approach</h2>
        <p>The core logic layer combines three required signals:</p>
        <ol>
          <li><strong>Sentiment intensity</strong> to measure the strength of negative affect in a region.</li>
          <li><strong>Volume spike detection</strong> to compare current discussion volume against historical baselines.</li>
          <li><strong>Geographic clustering</strong> to determine whether distress-related discussion is concentrated in specific counties.</li>
        </ol>
        <p>The score is stabilized with smoothing, gated by minimum sample thresholds, paired with a confidence estimate, and then evaluated against escalation thresholds.</p>
      </section>

      <section class="mb-4">
        <h2 class="h4">Project Scope</h2>
        <ul>
          <li>Behavioral tracking and crisis-language analysis.</li>
          <li>Longitudinal geospatial trend analysis.</li>
          <li>Interactive dashboard for monitoring and review.</li>
          <li>Governance-ready scoring and escalation logic.</li>
        </ul>
      </section>

      <section class="mb-4">
        <h2 class="h4">Contributor Selection Scenario</h2>
        <p>Within a 72-hour window, three Alabama counties show a significant increase in depression and suicide-related language. The State Behavioral Health Office asks whether the signal is credible enough for escalation to human review.</p>
      </section>

      <section class="mb-4">
        <h2 class="h4">Required Deliverables</h2>
        <ol>
          <li>
            <strong>Crisis Signal Design (Core Component)</strong>
            <ul>
              <li>Structured scoring framework integrating sentiment intensity, volume spikes, and geographic clustering.</li>
              <li>Minimum sample-size threshold.</li>
              <li>Smoothing/stabilization method.</li>
              <li>Confidence/uncertainty estimate.</li>
              <li>Pseudocode acceptable; advanced ML not required.</li>
            </ul>
          </li>
          <li>
            <strong>Governance and Risk Controls</strong>
            <ul>
              <li>Mitigation for bot amplification/coordinated activity.</li>
              <li>Mitigation for media-driven spikes.</li>
              <li>Mitigation for rural underrepresentation/sparse data.</li>
              <li>Escalation thresholds and human-in-the-loop workflow.</li>
              <li>Audit logging schema.</li>
            </ul>
          </li>
          <li>
            <strong>Governance Reflection (Short Section)</strong>
            <ul>
              <li>Primary risk of premature deployment.</li>
              <li>Single most important safeguard.</li>
            </ul>
          </li>
        </ol>
      </section>

      <section class="mb-4">
        <h2 class="h4">Evaluation Focus</h2>
        <ul>
          <li>Systems thinking and architectural clarity.</li>
          <li>Responsible AI and governance awareness.</li>
          <li>Bias identification and mitigation strategy.</li>
          <li>Treatment of uncertainty and confidence modeling.</li>
          <li>Professional technical communication.</li>
        </ul>
      </section>

      <section class="mb-5">
        <h2 class="h4">Repository Outputs</h2>
        <ul>
          <li><code>docs/PROJECT_SPEC.md</code> for project scope and invariants.</li>
          <li><code>docs/ARCHITECTURE.md</code> for runtime design and interfaces.</li>
          <li><code>docs/ROADMAP.md</code> for future development priorities.</li>
          <li><code>backend/</code> and <code>frontend/</code> for the working prototype.</li>
        </ul>
      </section>
    </div>

    <div class="col-lg-4">
      <div class="card mb-3">
        <div class="card-body">
          <h2 class="h6 card-title">Mentors</h2>
          <ul class="mb-0">
            <li>David M. White (University of Alabama)</li>
            <li>Hailey Richardson (University of Alabama)</li>
            <li>Dr. Andrea Underhill (University of Alabama)</li>
          </ul>
        </div>
      </div>

      <div class="card mb-3 border-warning">
        <div class="card-body">
          <h2 class="h6 card-title">Contact Policy</h2>
          <p class="mb-0">Do not contact mentors directly by email. Email <code>human-ai@cern.ch</code> with project title, CV, and test results.</p>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h2 class="h6 card-title">Required Skills</h2>
          <ul class="mb-0">
            <li>Python and NLP (spaCy, NLTK, Transformers)</li>
            <li>Text ML (BERT, LDA, VADER)</li>
            <li>Visualization (Plotly, D3.js, Matplotlib)</li>
            <li>Geospatial analytics (GeoPandas, Folium, Leaflet)</li>
          </ul>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h2 class="h6 card-title">Expected Results</h2>
          <ul class="mb-0">
            <li>Regional crisis detection with longitudinal trend analysis.</li>
            <li>Interactive dashboard with real-time and historical heatmaps.</li>
            <li>Decision-support indicators for earlier intervention planning.</li>
          </ul>
        </div>
      </div>

      <div class="alert alert-secondary" role="alert">
        <h2 class="h6">Open Item</h2>
        <p class="mb-0">The project test link is referenced but not provided. Add the actual URL before publication.</p>
      </div>
    </div>
  </div>

  <hr class="my-4">
  <p class="text-muted small mb-0">Built with GitHub Pages, Jekyll, and Bootstrap.</p>
</div>
