"""
AI4MH — Evaluation Metrics

Computes precision, recall, F1, and false-positive rate for
NLP crisis prediction against ground-truth labels.
"""

from __future__ import annotations

from typing import List

from models.post import EnrichedPost


def compute_classification_metrics(posts: List[EnrichedPost]) -> dict:
    """
    Compute binary classification metrics using ``nlp_crisis_flag`` as the
    predicted label and ``ground_truth_crisis`` as the reference label.

    Returns a dict with keys: tp, fp, fn, tn, precision, recall, f1, fpr.
    """
    tp = fp = fn = tn = 0

    for p in posts:
        pred = p.nlp_crisis_flag
        truth = p.ground_truth_crisis
        if pred and truth:
            tp += 1
        elif pred and not truth:
            fp += 1
        elif not pred and truth:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fpr, 4),
    }
