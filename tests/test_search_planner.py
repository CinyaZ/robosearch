from __future__ import annotations

from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.planner.score_model import PlannerWeights
from robosearch.planner.search_planner import SearchPlanner
from robosearch.types import SearchContext


def build_planner() -> SearchPlanner:
    prior_database = PriorDatabase(
        priors={
            "bottle": {
                "living_room_table": 0.5,
                "kitchen_counter": 0.9,
                "bookshelf": 0.2,
            }
        }
    )
    weights = PlannerWeights(
        semantic_prior=0.70,
        unvisited_bonus=0.20,
        failure_penalty=0.10,
    )
    return SearchPlanner(prior_database=prior_database, weights=weights)


def test_select_next_waypoint_prefers_high_prior_unvisited_candidate() -> None:
    planner = build_planner()
    context = SearchContext(
        target_label="bottle",
        current_waypoint_id="living_room_table",
        visited_waypoints=["living_room_table"],
    )

    decision = planner.select_next_waypoint(
        context=context,
        candidate_waypoints=["living_room_table", "kitchen_counter", "bookshelf"],
        failure_counts={"living_room_table": 1, "bookshelf": 1},
    )

    assert decision.decision_type == "waypoint_selection"
    assert decision.waypoint_id == "kitchen_counter"
    assert round(decision.score, 2) == 0.83


def test_empty_candidates_return_failure_decision() -> None:
    planner = build_planner()
    context = SearchContext(
        target_label="bottle",
        current_waypoint_id="living_room_table",
    )

    decision = planner.select_next_waypoint(
        context=context,
        candidate_waypoints=[],
    )

    assert decision.decision_type == "failure"
    assert decision.waypoint_id is None
    assert decision.score == 0.0


def test_score_candidates_returns_deterministic_sorted_results() -> None:
    planner = build_planner()
    context = SearchContext(
        target_label="bottle",
        current_waypoint_id="living_room_table",
        visited_waypoints=["living_room_table"],
    )

    ranked = planner.score_candidates(
        context=context,
        candidate_waypoints=["bookshelf", "kitchen_counter", "living_room_table"],
        failure_counts={"living_room_table": 1, "bookshelf": 1},
    )

    assert [item.waypoint_id for item in ranked] == [
        "kitchen_counter",
        "living_room_table",
        "bookshelf",
    ]
