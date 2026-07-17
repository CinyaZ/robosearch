from __future__ import annotations

from pathlib import Path

from robosearch import __version__
from robosearch.agent.search_agent import SearchAgent
from robosearch.api import load_yaml_config
from robosearch.executor.mock_executor import MockExecutor
from robosearch.knowledge.prior_database import PriorDatabase
from robosearch.memory.json_store import JsonStore
from robosearch.memory.memory_manager import MemoryManager
from robosearch.nbv.nbv_planner import NBVPlanner
from robosearch.observation.observation_manager import ObservationManager
from robosearch.perception.mock_detector import MockDetector
from robosearch.planner.score_model import PlannerWeights
from robosearch.planner.search_planner import SearchPlanner


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner_config = load_yaml_config(project_root / "configs" / "planner.yaml")
    detector_config = load_yaml_config(project_root / "configs" / "detector.yaml")
    waypoint_config = load_yaml_config(project_root / "configs" / "waypoints.yaml")
    prior_database = PriorDatabase.from_yaml(project_root / "configs" / "object_priors.yaml")
    nbv_planner = NBVPlanner(view_angles_deg=planner_config["default_turn_angles"])
    weights = PlannerWeights(**planner_config["weights"])
    search_planner = SearchPlanner(prior_database=prior_database, weights=weights)
    detector = MockDetector(target_label="bottle")
    executor = MockExecutor()
    observation_manager = ObservationManager()
    memory_store = JsonStore(project_root / "work" / "mock_search_memory.json")
    memory_manager = MemoryManager(memory_store)
    memory_manager.clear()

    agent = SearchAgent()
    bootstrap_result = agent.bootstrap(target_label="bottle")
    waypoint_ids = [item["id"] for item in waypoint_config["waypoints"]]
    waypoint_scene_map = {
        "living_room_table": "target_absent",
        "bookshelf": "target_absent",
        "kitchen_counter": "target_present",
    }
    search_result = agent.run_mock_search(
        target_label="bottle",
        initial_waypoint_id="living_room_table",
        candidate_waypoints=waypoint_ids,
        waypoint_scene_map=waypoint_scene_map,
        detector=detector,
        memory_manager=memory_manager,
        nbv_planner=nbv_planner,
        search_planner=search_planner,
        executor=executor,
        observation_manager=observation_manager,
        max_waypoints=planner_config["max_waypoints"],
    )
    memory_manager.clear()
    failed_search_result = agent.run_mock_search(
        target_label="bottle",
        initial_waypoint_id="living_room_table",
        candidate_waypoints=waypoint_ids,
        waypoint_scene_map={
            "living_room_table": "target_absent",
            "bookshelf": "target_absent",
            "kitchen_counter": "target_absent",
        },
        detector=detector,
        memory_manager=memory_manager,
        nbv_planner=nbv_planner,
        search_planner=search_planner,
        executor=executor,
        observation_manager=observation_manager,
        max_waypoints=planner_config["max_waypoints"],
    )

    print("=== RoboSearch V0 Search Loop Demo ===")
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
    print(f"bootstrap status: {bootstrap_result.status.value}")
    print(f"bootstrap message: {bootstrap_result.message}")
    print(f"search status: {search_result.status.value}")
    print(f"search success: {search_result.success}")
    print(f"search message: {search_result.message}")
    print("---")
    print(f"failed search status: {failed_search_result.status.value}")
    print(f"failed search success: {failed_search_result.success}")
    print(f"failed search message: {failed_search_result.message}")


if __name__ == "__main__":
    main()
