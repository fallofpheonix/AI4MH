from __future__ import annotations

REGIONS: list[dict[str, int | str]] = [
    {"id": "CA-LA", "name": "Los Angeles, CA", "population": 3_980_000},
    {"id": "TX-HOU", "name": "Houston, TX", "population": 2_300_000},
    {"id": "NY-NYC", "name": "New York, NY", "population": 8_340_000},
    {"id": "IL-CHI", "name": "Chicago, IL", "population": 2_700_000},
    {"id": "AZ-PHX", "name": "Phoenix, AZ", "population": 1_680_000},
    {"id": "PA-PHI", "name": "Philadelphia, PA", "population": 1_580_000},
    {"id": "WV-CHA", "name": "Charleston, WV", "population": 46_000},
    {"id": "KY-HAZ", "name": "Hazard, KY", "population": 4_700},
    {"id": "OH-CHI", "name": "Chillicothe, OH", "population": 21_000},
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
