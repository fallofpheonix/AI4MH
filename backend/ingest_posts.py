"""
AI4MH — Data Ingestion Module
Simulates Reddit-style post ingestion across US regions.
Swap generate_post() with a real PRAW call for production.
"""

import json, random, datetime, pathlib

REGIONS = [
    {"id": "CA-LA",  "name": "Los Angeles, CA",  "population": 3980000},
    {"id": "TX-HOU", "name": "Houston, TX",       "population": 2300000},
    {"id": "NY-NYC", "name": "New York, NY",      "population": 8340000},
    {"id": "IL-CHI", "name": "Chicago, IL",       "population": 2700000},
    {"id": "AZ-PHX", "name": "Phoenix, AZ",       "population": 1680000},
    {"id": "PA-PHI", "name": "Philadelphia, PA",  "population": 1580000},
    {"id": "WV-CHA", "name": "Charleston, WV",    "population": 46000},
    {"id": "KY-HAZ", "name": "Hazard, KY",        "population": 4700},
    {"id": "OH-CHI", "name": "Chillicothe, OH",   "population": 21000},
]

CRISIS_TEXTS = [
    "I can't go on anymore",
    "thinking about suicide, no way out",
    "life feels completely hopeless",
    "overdose seems easier than this",
    "nobody would miss me if I was gone",
    "I've been cutting again, can't stop",
    "relapsed after 2 years, feel so hopeless",
    "can't take it anymore, done with everything",
]

NORMAL_TEXTS = [
    "today was a good day overall",
    "going for a walk to clear my head",
    "feeling okay, therapy is helping",
    "started a new medication, cautiously hopeful",
    "support group really helped tonight",
    "had my first good day in months",
]

SUBREDDITS = ["depression", "mentalhealth", "SuicideWatch", "addiction", "anxiety"]

def generate_post(is_bot: bool = False) -> dict:
    is_crisis = random.random() < 0.25
    text = random.choice(CRISIS_TEXTS if is_crisis else NORMAL_TEXTS)
    region = random.choice(REGIONS)
    return {
        "id": f"post_{random.randint(100000,999999)}",
        "text": text,
        "subreddit": random.choice(SUBREDDITS),
        "region_id": region["id"],
        "region_name": region["name"],
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "upvotes": random.randint(0, 500),
        "comments": random.randint(0, 80),
        "is_bot": is_bot,
        "is_crisis_text": is_crisis,
    }

def generate_dataset(n: int = 300) -> list[dict]:
    posts = []
    for _ in range(n):
        # ~7% bot rate
        posts.append(generate_post(is_bot=random.random() < 0.07))
    return posts

def save_dataset(n: int = 300, path: str = "data/sample_posts.json"):
    posts = generate_dataset(n)
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(posts, f, indent=2)
    print(f"Saved {len(posts)} posts to {path}")
    return posts

if __name__ == "__main__":
    save_dataset()
