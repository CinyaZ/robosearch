from __future__ import annotations

from dataclasses import dataclass
from typing import List

from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.types import SearchContext, SearchDecision


@dataclass
class SearchPlanner:
    prior_database: PriorDatabase

    def select_next_waypoint(
        self, context: SearchContext, candidate_waypoints: List[str]
    ) -> SearchDecision:
        target_priors = self.prior_database.priors.get(context.target_label, {})
        best_waypoint = None
        best_score = float("-inf")

        for waypoint_id in candidate_waypoints:
            score = float(target_priors.get(waypoint_id, 0.0))
            if waypoint_id in context.visited_waypoints:
                score -= 1.0
            if score > best_score:
                best_waypoint = waypoint_id
                best_score = score

        return SearchDecision(
            next_waypoint_id=best_waypoint,
            next_view_angle_deg=0.0,
            score=best_score if best_waypoint is not None else 0.0,
            reason="Stage 0 placeholder planner decision.",
        )
