"""
AI4MH — Regional Aggregation Pipeline Stage

Groups enriched posts by region and calculates baselines needed by the
scoring stage. This module has no FastAPI dependency.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from models.post import EnrichedPost


def group_by_region(posts: List[EnrichedPost]) -> Dict[str, List[EnrichedPost]]:
    """Return a mapping of region_id → list of enriched posts."""
    groups: Dict[str, List[EnrichedPost]] = defaultdict(list)
    for post in posts:
        groups[post.region_id].append(post)
    return dict(groups)


def compute_global_avg(groups: Dict[str, List[EnrichedPost]]) -> float:
    """
    Compute the mean posts-per-region across all regions.

    Returns 0.0 if there are no regions (avoids division by zero).
    """
    if not groups:
        return 0.0
    return sum(len(v) for v in groups.values()) / len(groups)
