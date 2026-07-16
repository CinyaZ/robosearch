from __future__ import annotations


def simple_score(prior_score: float, revisit_penalty: float, travel_cost: float) -> float:
    return prior_score - revisit_penalty - travel_cost
