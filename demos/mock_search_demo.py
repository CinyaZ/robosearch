from __future__ import annotations

from pathlib import Path

from robosearch import __version__
from robosearch.agent.search_agent import SearchAgent
from robosearch.api import load_yaml_config
from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.nbv.nbv_planner import NBVPlanner


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner_config = load_yaml_config(project_root / "configs" / "planner.yaml")
    detector_config = load_yaml_config(project_root / "configs" / "detector.yaml")
    waypoint_config = load_yaml_config(project_root / "configs" / "waypoints.yaml")
    prior_database = PriorDatabase.from_yaml(project_root / "configs" / "object_priors.yaml")
    nbv_planner = NBVPlanner(view_angles_deg=planner_config["default_turn_angles"])

    agent = SearchAgent()
    result = agent.bootstrap(target_label="bottle")

    print("=== RoboSearch Stage 0 Demo ===")
    print(f"version: {__version__}")
    print(f"project_root: {project_root}")
    print(f"agent: {agent.name}")
    print(f"planner max_observations: {planner_config['max_observations']}")
    print(f"planner max_waypoints: {planner_config['max_waypoints']}")
    print(f"planner max_actions: {planner_config['max_actions']}")
    print(f"detector: {detector_config['name']}")
    print(f"supported_labels: {', '.join(detector_config['labels'])}")
    print(
        "waypoints: "
        + ", ".join(item["id"] for item in waypoint_config["waypoints"])
    )
    print(
        "default_view_angles: "
        + ", ".join(str(angle) for angle in nbv_planner.get_default_view_sequence())
    )
    print(
        "known_priors_for_bottle: "
        + ", ".join(
            f"{waypoint}={score}"
            for waypoint, score in prior_database.priors.get("bottle", {}).items()
        )
    )
    print(f"startup status: {result.status.value}")
    print(f"message: {result.message}")


if __name__ == "__main__":
    main()
