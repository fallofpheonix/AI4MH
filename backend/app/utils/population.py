from __future__ import annotations


def classify_population_tier(population: int | None) -> str:
    if population is None:
        return "suburban"
    if population < 100_000:
        return "rural"
    if population < 1_000_000:
        return "suburban"
    return "urban"
