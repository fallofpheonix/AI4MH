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
        <h2 class="h4">Project Description</h2>
        <p>Public health agencies and crisis service providers need earlier indicators of suicide, substance use, and mental health deterioration than traditional reporting pipelines can provide. AI4MH combines behavioral tracking, crisis language analysis, and longitudinal geospatial modeling to detect distress signals and support proactive resource allocation.</p>
      </section>

      <section class="mb-4">
        <h2 class="h4">Core Activities</h2>
        <ul>
          <li>Behavioral tracking of engagement with crisis-related content to detect escalation patterns.</li>
          <li>Crisis lexicon and NLP analysis for explicit, coded, and slang expressions of distress.</li>
          <li>Location-based trend monitoring with longitudinal geospatial crisis heatmaps.</li>
          <li>Operational dashboard for public health teams to monitor and prioritize interventions.</li>
        </ul>
      </section>

      <section class="mb-4">
        <h2 class="h4">Expected Results</h2>
        <ul>
          <li>Crisis detection pipeline for suicide, substance-use, and mental-health risk signals.</li>
          <li>Interactive dashboard with real-time and historical crisis mapping.</li>
          <li>Predictive indicators to support earlier intervention and resource deployment.</li>
          <li>Evaluation framework for outreach effectiveness over time.</li>
        </ul>
      </section>

      <section class="mb-4">
        <h2 class="h4">Contributor Selection Task (GSoC 2026)</h2>
        <p>This assessment targets architectural reasoning, governance design, and communication quality. It is explicitly <strong>not</strong> a model-building competition.</p>
      </section>

      <section class="mb-4">
        <h3 class="h5">Scenario</h3>
        <p>Within a 72-hour window, three Alabama counties show a significant increase in depression and suicide-related language. The State Behavioral Health Office asks whether the signal is credible enough for escalation to human review.</p>
      </section>

      <section class="mb-4">
        <h3 class="h5">Required Deliverables</h3>
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
        <h3 class="h5">Submission Requirements</h3>
        <ul>
          <li>3-4 pages maximum (excluding optional diagram).</li>
          <li>Optional one architecture diagram.</li>
          <li>Clear section headings required.</li>
          <li>Single PDF submission via GSoC portal.</li>
          <li>Estimated effort: 6-8 hours over one week.</li>
          <li>Original work only; AI-tool use must be disclosed.</li>
        </ul>
      </section>

      <section class="mb-5">
        <h3 class="h5">Evaluation Criteria</h3>
        <ul>
          <li>Systems thinking and architectural clarity.</li>
          <li>Responsible AI and governance awareness.</li>
          <li>Bias identification and mitigation strategy.</li>
          <li>Treatment of uncertainty and confidence modeling.</li>
          <li>Professional technical communication.</li>
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
          <h2 class="h6 card-title">Skills Needed</h2>
          <ul class="mb-0">
            <li>Python and NLP (spaCy, NLTK, Transformers)</li>
            <li>Text ML (BERT, LDA, VADER)</li>
            <li>Visualization (Plotly, D3.js, Matplotlib)</li>
            <li>Geospatial analytics (GeoPandas, Folium, Leaflet)</li>
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
