# Crisis Signal Design and Governance Framework

*(AI4MH / HumanAI Crisis Detection Submission Template)*

## 1. System Overview

The proposed system detects emerging crisis signals from social media streams by combining sentiment signals, temporal activity spikes, and geographic clustering. The system aggregates weak signals from multiple posts into a structured crisis score for each region within a defined time window.

The system is designed with three goals:

1. early detection of crisis-related public discourse
2. reduction of false positives caused by noise or coordinated manipulation
3. transparent governance with human oversight

### Processing Pipeline

```text
Data Collection
    ↓
Preprocessing
    ↓
Sentiment Analysis
    ↓
Signal Aggregation
    ↓
Crisis Score Calculation
    ↓
Confidence Estimation
    ↓
Escalation Decision
```

### Architecture Diagram Structure (Text Format)

```text
                +-----------------------+
                |   Social Media APIs   |
                | (Twitter, Reddit etc) |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                |   Data Collection     |
                |  Streaming / Batch    |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                |     Preprocessing     |
                | - Text cleaning       |
                | - Language detection  |
                | - Location extraction |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                |   Feature Extraction  |
                | - Sentiment scoring   |
                | - Keyword detection   |
                | - Metadata features   |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                |  Signal Aggregation   |
                | - Time windowing      |
                | - Regional grouping   |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                |  Crisis Score Engine  |
                |                       |
                | Sentiment Intensity   |
                | Volume Spike          |
                | Geographic Cluster    |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Confidence Estimator  |
                | - Sample size         |
                | - Variance check      |
                | - Coverage measure    |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Escalation Decision   |
                | Threshold Evaluation  |
                +-----------+-----------+
                            |
                +-----------+-----------+
                |                       |
                v                       v
      +----------------+      +--------------------+
      | Monitoring     |      | Human Review Panel |
      | Dashboard      |      | Crisis Analysts    |
      +----------------+      +---------+----------+
                                        |
                                        v
                           +------------------------+
                           |   Governance Logging   |
                           | - Audit Records        |
                           | - Model Decisions      |
                           | - Reviewer Actions     |
                           +------------------------+
```

Placement: insert this immediately after the `System Overview` section in the PDF.

### Inputs

- Social media posts
- Timestamp
- Geographic metadata
- User metadata

### Outputs

```text
CrisisScore(region, time_window)
ConfidenceScore
EscalationFlag
```

The system aggregates signals within regional time windows (for example 6 to 24 hours) to produce interpretable crisis indicators.

## 2. Crisis Signal Design

The crisis signal integrates three components:

1. sentiment intensity
2. volume spike detection
3. geographic clustering

Each component contributes to a weighted crisis score.

### 2.1 Sentiment Intensity

Sentiment analysis estimates the emotional polarity of posts. Crisis-related posts often exhibit strongly negative sentiment.

Let sentiment scores range from `-1` (very negative) to `+1` (very positive).

```text
sentiment_intensity = mean(sentiment_scores)
```

Negative sentiment is converted to a crisis indicator:

```text
normalized_sentiment = max(0, -sentiment_intensity)
```

Higher values indicate stronger crisis-related sentiment.

### 2.2 Volume Spike Detection

A sudden increase in posts related to crisis keywords can indicate emerging events.

Baseline activity is estimated using a moving average.

```text
baseline_volume = moving_average(post_count, window = 7 days)
```

Spike ratio:

```text
volume_spike = current_volume / baseline_volume
```

Normalized spike score:

```text
volume_score = min(volume_spike / spike_limit, 1)
```

This ensures that extreme spikes do not dominate the signal.

### 2.3 Geographic Clustering

Local crises often produce geographically concentrated signals.

```text
geo_cluster = posts_in_region / total_posts
```

High clustering indicates spatially localized signals.

### 2.4 Crisis Score Aggregation

The final crisis score is computed using weighted aggregation.

```text
crisis_score =
    0.4 * normalized_sentiment +
    0.4 * volume_score +
    0.2 * geo_cluster
```

Weights emphasize emotional signal strength and temporal spikes while still considering geographic concentration.

### 2.5 Minimum Sample Size Threshold

Small samples can produce unstable signals. The system enforces a minimum number of posts before computing a crisis score.

```text
MIN_SAMPLE_SIZE = 50
```

If the number of posts in the time window is below the threshold:

```text
return insufficient_data
```

### 2.6 Signal Stabilization

Short-term fluctuations are reduced using exponential moving average smoothing.

```text
smoothed_score =
    alpha * crisis_score +
    (1 - alpha) * previous_score
```

Example parameter:

```text
alpha = 0.3
```

This prevents short-lived noise spikes from triggering alerts.

### 2.7 Confidence Estimation

Each crisis score is accompanied by a confidence estimate based on:

- sample size
- geographic coverage
- sentiment variance

Example formulation:

```text
confidence =
    min(
        log(sample_size)/log(1000),
        geo_coverage,
        1 - sentiment_variance
    )
```

Confidence values range from `0` to `1`.

Low confidence signals are flagged for monitoring but not escalation.

### 2.8 Pseudocode

```text
function compute_crisis_signal(posts):

    if len(posts) < MIN_SAMPLE_SIZE:
        return "insufficient_data"

    sentiment_score = avg_negative_sentiment(posts)

    volume_score = detect_volume_spike(posts)

    geo_score = geographic_cluster(posts)

    crisis_score =
        0.4*sentiment_score +
        0.4*volume_score +
        0.2*geo_score

    smoothed_score = EMA(crisis_score)

    confidence = estimate_confidence(posts)

    return smoothed_score, confidence
```

## 3. Governance and Risk Controls

The system must address manipulation risks and representation bias.

### 3.1 Bot Amplification and Coordinated Activity

Automated accounts can artificially inflate crisis signals.

Indicators include:

- abnormal posting frequency
- identical message content
- new or low-reputation accounts

Mitigation strategy:

```text
bot_weight = 0.3
human_weight = 1.0
```

Posts identified as bot-generated receive reduced influence in signal aggregation.

Coordinated campaigns are detected using message similarity clustering and synchronized activity patterns. Clustered posts are capped to prevent large coordinated campaigns from dominating the signal.

### 3.2 Media-Driven Spikes

Major news events can produce large spikes unrelated to real-time crisis conditions.

To mitigate this effect, the system measures the proportion of posts referencing major media sources.

```text
news_volume_ratio =
    media_mentions / total_mentions
```

If the ratio exceeds a threshold, the crisis score is discounted to prevent media amplification from triggering alerts.

### 3.3 Rural Underrepresentation

Rural regions often produce fewer social media signals, leading to sparse data.

Mitigation strategies include:

- expanding time windows for aggregation
- incorporating signals from neighboring regions
- lowering escalation confidence when coverage is low

These mechanisms prevent the system from falsely interpreting sparse signals.

### 3.4 Escalation Thresholds

The system uses a three-level escalation structure.

| Crisis Score | Action |
| --- | --- |
| < 0.4 | no action |
| 0.4-0.7 | monitoring |
| > 0.7 | human review escalation |

Escalation condition:

```text
if crisis_score > 0.75 and confidence > 0.6:
    escalate_to_human_review
```

The system does not trigger automated public alerts.

### 3.5 Human-in-the-Loop Review

Human analysts verify system signals before any operational response.

The reviewer evaluates:

- contextual interpretation of posts
- presence of coordinated manipulation
- reliability of geographic signals

Human oversight ensures that automated signals do not cause inappropriate escalation.

### 3.6 Audit Logging

Every system decision must be recorded for accountability and traceability.

Example audit record:

```text
{
timestamp
region
crisis_score
confidence
sample_size
sentiment_avg
volume_spike
geo_cluster
escalation_flag
reviewer_id
}
```

Logs allow post-event analysis and ensure transparency in public-sector deployments.

## 4. Governance Reflection

### Primary Risk of Premature Deployment

The primary risk is false crisis detection due to noisy or manipulated social media signals. Incorrect alerts could cause public panic, misallocation of emergency resources, or erosion of trust in public institutions.

### Most Important Safeguard

Mandatory human verification before escalation is the most important safeguard. Human analysts provide contextual interpretation and prevent automated systems from acting on unreliable or manipulated signals.

## Usage Notes

- Keep final PDF within 3-4 pages (excluding optional single diagram).
- Use clear section headers identical to this template.
- Disclose any generative AI assistance.
