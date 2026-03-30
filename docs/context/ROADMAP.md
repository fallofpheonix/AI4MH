# ROADMAP

## Near Term

- add alert transition controls to dashboard
- add bias diagnostics panel to dashboard
- add frontend automated tests

## Mid Term

- replace synthetic ingestion with replayable datasets
- add source normalization and deduplication
- add threshold/audit metadata for operator actions

## Longer Term

- add relational persistence or migration tooling if SQLite JSON blobs become limiting
- add background execution for long-running ingest jobs
- add offline evaluation and benchmark reporting

## Exit Criteria Per Milestone

- UI milestone: alert actions + bias view shipped without breaking build/tests
- data milestone: deterministic replayable ingest path exists
- governance milestone: alert actions include operator identity / notes
- evaluation milestone: metrics are reproducible from checked-in fixtures
