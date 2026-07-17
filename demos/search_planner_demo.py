from __future__ import annotations

from pathlib import Path

from robosearch.api import load_yaml_config
from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.planner.score_model import PlannerWeights
from robosearch.planner.search_planner import SearchPlanner
from robosearch.types import SearchContext


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner_config = load_yaml_config(project_root / "configs" / "planner.yaml")
    waypoint_config = load_yaml_config(project_root / "configs" / "waypoints.yaml")
    prior_database = PriorDatabase.from_yaml(project_root / "configs" / "object_priors.yaml")

    weights = PlannerWeights(**planner_config["weights"])
    planner = SearchPlanner(prior_database=prior_database, weights=weights)

    candidate_waypoints = [item["id"] for item in waypoint_config["waypoints"]]
    context = SearchContext(
        target_label="bottle",
        current_waypoint_id="living_room_table",
        visited_waypoints=["living_room_table"],
    )
    failure_counts = {
        "living_room_table": 1,
        "bookshelf": 1,
    }

    ranked_candidates = planner.score_candidates(
        context=context,
        candidate_waypoints=candidate_waypoints,
        failure_counts=failure_counts,
    )
    decision = planner.select_next_waypoint(
        context=context,
        candidate_waypoints=candidate_waypoints,
        failure_counts=failure_counts,
    )

    print("=== RoboSearch Stage 4 Search Planner Demo ===")
    print(f"target: {context.target_label}")
    print("candidate_waypoints: " + ", ".join(candidate_waypoints))
    print("visited_waypoints: " + ", ".join(context.visited_waypoints))
    print("failure_counts: " + ", ".join(f"{k}={v}" for k, v in sorted(failure_counts.items())))
    print("candidate_scores:")
    for item in ranked_candidates:
        print(f"  - {item.waypoint_id}: {item.score:.2f}")
    print(f"decision_type: {decision.decision_type}")
    print(f"selected_waypoint: {decision.waypoint_id}")
    print(f"score: {decision.score:.2f}")
    print("score_breakdown:")
    for key, value in decision.score_breakdown.items():
        print(f"  {key}: {value:.2f}")
    print("reason:")
    for item in decision.reason:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
