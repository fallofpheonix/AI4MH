"""
AI4MH — NLP Processing Module
Sentiment analysis via VADER + crisis keyword detection.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

CRISIS_TERMS = [
    "suicide", "kill myself", "can't go on", "overdose",
    "no reason to live", "end it all", "self harm", "cutting",
    "hopeless", "worthless", "disappear forever", "nobody would miss me",
    "done with everything", "can't take it anymore",
]

def sentiment_score(text: str) -> float:
    """Returns compound VADER score in [-1, 1]. Negative = distress."""
    return _analyzer.polarity_scores(text)["compound"]

def keyword_score(text: str) -> dict:
    """Returns count and list of matched crisis keywords."""
    lower = text.lower()
    matched = [t for t in CRISIS_TERMS if t in lower]
    return {"count": len(matched), "terms": matched}

def analyze_post(post: dict) -> dict:
    """Enriches a post dict with NLP signals."""
    sentiment = sentiment_score(post["text"])
    keywords  = keyword_score(post["text"])
    predicted_crisis = sentiment < -0.4 or keywords["count"] > 0
    ground_truth = bool(post.get("ground_truth_crisis", post.get("is_crisis_text", False)))
    return {
        **post,
        "sentiment":       round(sentiment, 4),
        "keyword_count":   keywords["count"],
        "keyword_terms":   keywords["terms"],
        "nlp_crisis_flag": predicted_crisis,
        "ground_truth_crisis": ground_truth,
        "ai_correct": predicted_crisis == ground_truth,
    }

def analyze_batch(posts: list[dict]) -> list[dict]:
    return [analyze_post(p) for p in posts]
