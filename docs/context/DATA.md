# DATA

## Source Data

Generator: `backend/app/services/ingestion_service.py`

- regions: `9`
- crisis-post probability: `0.25`
- bot-post probability: `0.07`
- subreddits:
  - `depression`
  - `mentalhealth`
  - `SuicideWatch`
  - `addiction`
  - `anxiety`

## Region IDs

- `CA-LA`
- `TX-HOU`
- `NY-NYC`
- `IL-CHI`
- `AZ-PHX`
- `PA-PHI`
- `WV-CHA`
- `KY-HAZ`
- `OH-CHI`

## Schemas

### `RawPost`

- `id:str`
- `text:str`
- `subreddit:str`
- `region_id:str`
- `region_name:str`
- `timestamp:str`
- `upvotes:int`
- `comments:int`
- `is_bot:bool`
- `is_crisis_text:bool`
- `ground_truth_crisis:bool`

### `EnrichedPost`

Extends `RawPost` with:

- `sentiment:float[-1,1]`
- `keyword_count:int`
- `keyword_terms:list[str]`
- `nlp_crisis_flag:bool`
- `ai_correct:bool`

### `RegionScore`

- `region_id:str`
- `post_count:int`
- `bot_count:int`
- `bot_ratio:float`
- `sentiment_intensity:float`
- `volume_spike:float`
- `geo_cluster:float`
- `trend_accel:float`
- `crisis_score:float`
- `confidence:float`
- `should_escalate:bool`
- `avg_sentiment:float`

### `Alert`

- `id:str`
- `region:str`
- `score:float`
- `status:review_required|acknowledged|dismissed|resolved`
- `confidence:float`
- `sample_size:int`
- `created_at:str`
- `updated_at:str`
- `score_breakdown:dict`
- `evidence_post_ids:list[str]`

### `LogEvent`

- `timestamp:str`
- `event:str`
- `payload:dict`

## Edge Cases

- empty post text -> sentiment `0.0`
- all-bot region -> no `RegionScore`
- fewer than `4` posts in a region -> trend acceleration `0.0`
- low sample region in bias output -> `low_sample_flag=true` when `post_count < 20`
- unknown region population -> tier defaults to `suburban`
