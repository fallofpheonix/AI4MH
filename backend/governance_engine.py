"""
Governance and risk-control layer for crisis signal escalation.

Implements:
- bot-activity scoring
- coordinated-activity detection
- media-amplification detection
- sparse-region handling
- escalation decision policy
- human-review queue routing
- append-only audit logging
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any


class GovernanceEngine:
    """
    Governance engine for public-sector crisis monitoring.

    Expected `posts` fields (best-effort; missing fields are tolerated):
    - text
    - timestamp (ISO string)
    - region
    - user_id
    - account_age_days (optional, numeric)
    - followers (optional, numeric)
    - following (optional, numeric)
    """

    BOT_POST_FREQ_THRESHOLD = 10
    BOT_DUPLICATE_THRESHOLD = 0.8
    BOT_NEW_ACCOUNT_DAYS = 14
    BOT_FOLLOW_RATIO_THRESHOLD = 0.1

    COORDINATED_CLUSTER_MIN_USERS = 5
    COORDINATED_MAX_INFLUENCE = 0.5

    MEDIA_RATIO_THRESHOLD = 0.5
    MEDIA_DISCOUNT_FACTOR = 0.8

    RURAL_THRESHOLD = 20
    RURAL_WINDOW_EXTENSION_HOURS = 48
    RURAL_CONFIDENCE_FACTOR = 0.8

    def __init__(self) -> None:
        self.review_queue: list[dict[str, Any]] = []
        self.decision_log: list[dict[str, Any]] = []
        self.major_media_tokens = {
            "cnn",
            "bbc",
            "fox",
            "reuters",
            "ap news",
            "headline",
            "breaking news",
            "news report",
        }

    @staticmethod
    def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
        return max(lo, min(hi, value))

    @staticmethod
    def _to_hour_bucket(ts: str | None) -> str:
        if not ts:
            return "unknown"
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%dT%H")
        except Exception:
            return "unknown"

    @staticmethod
    def _extract_hashtags(text: str) -> set[str]:
        tags = set()
        for token in text.split():
            if token.startswith("#") and len(token) > 1:
                tags.add(token.lower())
        return tags

    def detect_bot_activity(self, posts: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Return bot probability in [0, 1] using four heuristic signals:
        - abnormal posting frequency
        - duplicate/near-duplicate text concentration
        - recent account creation
        - low follower/following ratio
        """
        if not posts:
            return {
                "bot_probability": 0.0,
                "reduce_influence": False,
                "influence_multiplier": 1.0,
                "signals": {},
            }

        total = len(posts)
        user_counts = Counter(str(p.get("user_id", "unknown")) for p in posts)
        max_posts_per_user = max(user_counts.values()) if user_counts else 0
        freq_signal = 1.0 if max_posts_per_user >= self.BOT_POST_FREQ_THRESHOLD else (
            max_posts_per_user / self.BOT_POST_FREQ_THRESHOLD
        )

        texts = [str(p.get("text", "")).strip().lower() for p in posts if p.get("text")]
        duplicate_signal = 0.0
        if texts:
            duplicate_signal = max(Counter(texts).values()) / len(texts)

        account_ages = [
            float(p.get("account_age_days"))
            for p in posts
            if p.get("account_age_days") is not None
        ]
        recent_ratio = 0.0
        if account_ages:
            recent_ratio = sum(1 for age in account_ages if age <= self.BOT_NEW_ACCOUNT_DAYS) / len(account_ages)

        follow_ratios = []
        for p in posts:
            followers = p.get("followers")
            following = p.get("following")
            if followers is None or following in (None, 0):
                continue
            follow_ratios.append(float(followers) / float(following))
        low_ratio_signal = 0.0
        if follow_ratios:
            low_ratio_signal = sum(
                1 for ratio in follow_ratios if ratio <= self.BOT_FOLLOW_RATIO_THRESHOLD
            ) / len(follow_ratios)

        # Simple weighted heuristic score.
        bot_probability = self._clamp(
            0.35 * freq_signal
            + 0.30 * duplicate_signal
            + 0.20 * recent_ratio
            + 0.15 * low_ratio_signal
        )

        reduce_influence = bot_probability > 0.7
        return {
            "bot_probability": round(bot_probability, 4),
            "reduce_influence": reduce_influence,
            "influence_multiplier": 0.5 if reduce_influence else 1.0,
            "signals": {
                "freq_signal": round(freq_signal, 4),
                "duplicate_signal": round(duplicate_signal, 4),
                "recent_account_signal": round(recent_ratio, 4),
                "low_follow_ratio_signal": round(low_ratio_signal, 4),
                "max_posts_per_user": max_posts_per_user,
                "total_posts": total,
            },
        }

    def detect_coordinated_activity(self, posts: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Detect coordinated clusters using:
        - identical hashtags
        - repeated message patterns
        - synchronized timestamps (hour buckets)
        """
        if not posts:
            return {
                "coordinated_activity": False,
                "cluster_count": 0,
                "influence_cap": 1.0,
            }

        hashtag_clusters: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
        text_clusters: defaultdict[tuple[str, str], set[str]] = defaultdict(set)

        for p in posts:
            user = str(p.get("user_id", "unknown"))
            text = str(p.get("text", "")).strip().lower()
            hour = self._to_hour_bucket(p.get("timestamp"))

            for tag in self._extract_hashtags(text):
                hashtag_clusters[(tag, hour)].add(user)
            if text:
                text_clusters[(text, hour)].add(user)

        cluster_count = 0
        for clusters in (hashtag_clusters, text_clusters):
            cluster_count += sum(
                1 for users in clusters.values()
                if len(users) >= self.COORDINATED_CLUSTER_MIN_USERS
            )

        coordinated = cluster_count > 0
        return {
            "coordinated_activity": coordinated,
            "cluster_count": cluster_count,
            "influence_cap": self.COORDINATED_MAX_INFLUENCE if coordinated else 1.0,
        }

    def detect_media_amplification(self, posts: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Estimate media amplification ratio:
        media_ratio = media_mentions / total_posts
        """
        if not posts:
            return {
                "media_ratio": 0.0,
                "reduce_influence": False,
                "influence_multiplier": 1.0,
            }

        media_hits = 0
        for p in posts:
            text = str(p.get("text", "")).lower()
            if any(token in text for token in self.major_media_tokens):
                media_hits += 1

        media_ratio = media_hits / len(posts)
        reduce_influence = media_ratio > self.MEDIA_RATIO_THRESHOLD
        return {
            "media_ratio": round(media_ratio, 4),
            "reduce_influence": reduce_influence,
            "influence_multiplier": self.MEDIA_DISCOUNT_FACTOR if reduce_influence else 1.0,
        }

    def handle_sparse_regions(self, signal: dict[str, Any]) -> dict[str, Any]:
        """
        Sparse-region policy:
        - if sample size is below rural threshold, extend time window
        - reduce confidence and tag signal
        """
        sample_size = int(signal.get("sample_size", 0))
        confidence_key = "confidence"
        if confidence_key not in signal:
            confidence_key = "confidence_score"

        if sample_size >= self.RURAL_THRESHOLD:
            signal["sparse_region"] = False
            signal["window_extension_hours"] = 0
            return signal

        signal["sparse_region"] = True
        signal["window_extension_hours"] = self.RURAL_WINDOW_EXTENSION_HOURS
        current_conf = float(signal.get(confidence_key, 0.0))
        signal[confidence_key] = round(self._clamp(current_conf * self.RURAL_CONFIDENCE_FACTOR), 4)
        signal["low_confidence_reason"] = "sparse_region"
        return signal

    def evaluate_escalation(self, crisis_score: float, confidence: float) -> dict[str, Any]:
        """
        Escalation policy:
        - crisis_score > 0.75 and confidence > 0.6 -> HUMAN_REVIEW_REQUIRED
        - crisis_score > 0.4 -> MONITOR
        - otherwise -> NO_ACTION
        """
        if crisis_score > 0.75 and confidence > 0.6:
            decision = "HUMAN_REVIEW_REQUIRED"
        elif crisis_score > 0.4:
            decision = "MONITOR"
        else:
            decision = "NO_ACTION"

        return {
            "decision": decision,
            "escalation_flag": decision == "HUMAN_REVIEW_REQUIRED",
        }

    def route_to_human_review(self, signal: dict[str, Any]) -> dict[str, Any]:
        """
        Simulate routing to human review queue.

        Human reviewers should check:
        - context of posts
        - manipulation indicators
        - geographic relevance
        """
        if signal.get("decision") != "HUMAN_REVIEW_REQUIRED":
            signal["human_review_required"] = False
            signal["review_status"] = "NOT_REQUIRED"
            return signal

        review_item = {
            "queue_id": f"review-{len(self.review_queue) + 1}",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "region": signal.get("region"),
            "crisis_score": signal.get("crisis_score"),
            "confidence": signal.get("confidence", signal.get("confidence_score")),
            "checks_required": [
                "context_verification",
                "manipulation_signal_check",
                "geographic_relevance_check",
            ],
            "status": "PENDING_REVIEW",
        }
        self.review_queue.append(review_item)

        signal["human_review_required"] = True
        signal["review_status"] = "PENDING_REVIEW"
        signal["review_queue_id"] = review_item["queue_id"]
        return signal

    def log_decision(
        self,
        signal: dict[str, Any],
        decision: dict[str, Any],
        reviewer_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Append-only audit log for governance decisions.
        """
        confidence = signal.get("confidence", signal.get("confidence_score"))
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "region": signal.get("region"),
            "crisis_score": signal.get("crisis_score"),
            "confidence": confidence,
            "sample_size": int(signal.get("sample_size", 0)),
            "decision": decision.get("decision"),
            "bot_probability": signal.get("bot_probability", 0.0),
            "coordinated_activity": bool(signal.get("coordinated_activity", False)),
            "reviewer_id": reviewer_id,
        }
        self.decision_log.append(record)
        return record

    def apply_governance_controls(
        self,
        signal: dict[str, Any],
        posts: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        End-to-end governance pass:
        - compute manipulation indicators
        - apply influence reductions/caps
        - apply sparse-region handling
        - evaluate escalation
        - route to human review
        - append audit log
        """
        governed = dict(signal)

        bot = self.detect_bot_activity(posts)
        coord = self.detect_coordinated_activity(posts)
        media = self.detect_media_amplification(posts)

        governed["bot_probability"] = bot["bot_probability"]
        governed["coordinated_activity"] = coord["coordinated_activity"]
        governed["media_ratio"] = media["media_ratio"]

        influence = 1.0
        influence *= bot["influence_multiplier"]
        influence *= media["influence_multiplier"]
        influence = min(influence, coord["influence_cap"])
        governed["governance_influence_multiplier"] = round(influence, 4)

        base_score = float(governed.get("crisis_score", 0.0))
        governed["crisis_score"] = round(self._clamp(base_score * influence), 4)

        governed = self.handle_sparse_regions(governed)

        confidence = float(governed.get("confidence", governed.get("confidence_score", 0.0)))
        decision = self.evaluate_escalation(governed["crisis_score"], confidence)
        governed.update(decision)
        governed = self.route_to_human_review(governed)
        governed["audit_record"] = self.log_decision(governed, decision)
        return governed
