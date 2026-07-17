from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.planner.score_model import PlannerWeights, compute_search_score
from robosearch.types import SearchContext, SearchDecision


@dataclass
class SearchPlanner:
    prior_database: PriorDatabase
    weights: PlannerWeights

    def score_candidates(
        self,
        context: SearchContext,
        candidate_waypoints: List[str],
        failure_counts: Optional[Dict[str, int]] = None,
    ) -> List[SearchDecision]:
        target_priors = self.prior_database.priors.get(context.target_label, {})
        failure_counts = failure_counts or {}
        decisions: List[SearchDecision] = []

        for waypoint_id in sorted(candidate_waypoints):
            semantic_prior = float(target_priors.get(waypoint_id, 0.0))
            unvisited_bonus = 0.0 if waypoint_id in context.visited_waypoints else 1.0
            failure_penalty = min(float(failure_counts.get(waypoint_id, 0)), 1.0)
            breakdown = compute_search_score(
                semantic_prior=semantic_prior,
                unvisited_bonus=unvisited_bonus,
                failure_penalty=failure_penalty,
                weights=self.weights,
            )
            decisions.append(
                SearchDecision(
                    decision_type="candidate_score",
                    waypoint_id=waypoint_id,
                    score=breakdown["total_score"],
                    score_breakdown=breakdown,
                    reason=self._build_reason_lines(
                        target_label=context.target_label,
                        waypoint_id=waypoint_id,
                        semantic_prior=semantic_prior,
                        unvisited_bonus=unvisited_bonus,
                        failure_penalty=failure_penalty,
                    ),
                )
            )

        return sorted(
            decisions,
            key=lambda item: (-item.score, item.waypoint_id or ""),
        )

    def select_next_waypoint(
        self,
        context: SearchContext,
        candidate_waypoints: List[str],
        failure_counts: Optional[Dict[str, int]] = None,
    ) -> SearchDecision:
        if not candidate_waypoints:
            return SearchDecision(
                decision_type="failure",
                waypoint_id=None,
                score=0.0,
                score_breakdown={},
                reason=["No candidate waypoints were provided to the planner."],
            )
        ranked_candidates = self.score_candidates(
            context=context,
            candidate_waypoints=candidate_waypoints,
            failure_counts=failure_counts,
        )
        best_candidate = ranked_candidates[0]

        return SearchDecision(
            decision_type="waypoint_selection",
            waypoint_id=best_candidate.waypoint_id,
            score=best_candidate.score,
            score_breakdown=best_candidate.score_breakdown,
            reason=best_candidate.reason,
        )

    def _build_reason_lines(
        self,
        target_label: str,
        waypoint_id: str,
        semantic_prior: float,
        unvisited_bonus: float,
        failure_penalty: float,
    ) -> List[str]:
        reasons = [
            (
                f"Target '{target_label}' has semantic prior "
                f"{semantic_prior:.2f} at waypoint '{waypoint_id}'."
            )
        ]
        if unvisited_bonus > 0:
            reasons.append("The waypoint has not been searched in the current session.")
        else:
            reasons.append("The waypoint has already been searched in the current session.")
        if failure_penalty > 0:
            reasons.append("The waypoint receives a failure penalty from prior unsuccessful attempts.")
        else:
            reasons.append("The waypoint has no recorded failure penalty.")
        return reasons
