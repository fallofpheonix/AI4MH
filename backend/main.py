from app.main import app, create_app

__all__ = ["app", "create_app"]
    scores = _store.get_scores()
    alerts = _store.get_alerts()
    return {
        "message": f"Ingested {n} posts",
        "total_posts": len(all_posts),
        "regions_scored": len(scores),
        "alerts": len(alerts),
    }
