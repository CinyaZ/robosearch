from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PlannerWeights:
    semantic_prior: float
    unvisited_bonus: float
    failure_penalty: float


def compute_search_score(
    semantic_prior: float,
    unvisited_bonus: float,
    failure_penalty: float,
    weights: PlannerWeights,
) -> Dict[str, float]:
    weighted_semantic = weights.semantic_prior * semantic_prior
    weighted_unvisited = weights.unvisited_bonus * unvisited_bonus
    weighted_failure = weights.failure_penalty * failure_penalty
    total_score = weighted_semantic + weighted_unvisited - weighted_failure

    return {
        "semantic_prior": weighted_semantic,
        "unvisited_bonus": weighted_unvisited,
        "failure_penalty": -weighted_failure,
        "total_score": total_score,
    }
