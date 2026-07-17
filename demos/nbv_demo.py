from __future__ import annotations

from pathlib import Path

from robosearch.api import load_yaml_config
from robosearch.memory.json_store import JsonStore
from robosearch.memory.memory_manager import MemoryManager
from robosearch.nbv.nbv_planner import NBVPlanner
from robosearch.perception.mock_detector import MockDetector
from robosearch.types import Observation


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner_config = load_yaml_config(project_root / "configs" / "planner.yaml")
    memory_path = project_root / "work" / "nbv_demo_store.json"

    planner = NBVPlanner(
        view_angles_deg=planner_config["default_turn_angles"],
        low_confidence_threshold=0.5,
        max_local_views=5,
    )

    visited_angles = [0.0, 45.0]
    next_view = planner.select_next_view_angle(visited_angles)

    detector = MockDetector(target_label="bottle")
    memory_manager = MemoryManager(JsonStore(memory_path))
    memory_manager.clear()

    memory_manager.record_observation(
        observation=Observation(
            waypoint_id="living_room_table",
            view_angle_deg=-45.0,
            image_path="target_absent",
            detections=detector.detect("target_absent"),
            timestamp="2026-07-16T21:00:00Z",
        ),
        target_label="bottle",
    )

    low_confidence_detections = detector.detect("low_confidence_target")
    absent_detections = detector.detect("target_absent")
    next_bottle_view = planner.select_next_target_view_angle(
        target_label="bottle",
        waypoint_id="living_room_table",
        visited_angles_deg=visited_angles,
        has_searched_target_view=memory_manager.has_searched_target_view,
    )
    next_cup_view = planner.select_next_target_view_angle(
        target_label="cup",
        waypoint_id="living_room_table",
        visited_angles_deg=visited_angles,
        has_searched_target_view=memory_manager.has_searched_target_view,
    )
    bottle_decision = planner.select_next_target_view_decision(
        target_label="bottle",
        waypoint_id="living_room_table",
        visited_angles_deg=visited_angles,
        has_searched_target_view=memory_manager.has_searched_target_view,
    )

    recheck_action = planner.suggest_recheck_action(
        detections=low_confidence_detections,
        target_label="bottle",
    )
    no_recheck_action = planner.suggest_recheck_action(
        detections=absent_detections,
        target_label="bottle",
    )

    print("=== RoboSearch Stage 3 NBV Demo ===")
    print(
        "default_view_sequence: "
        + ", ".join(str(angle) for angle in planner.get_default_view_sequence())
    )
    print("visited_angles: " + ", ".join(str(angle) for angle in visited_angles))
    print(f"next_view_angle: {next_view}")
    print(f"next_bottle_view_angle: {next_bottle_view}")
    print(f"next_cup_view_angle: {next_cup_view}")
    print(f"bottle_decision_present: {bottle_decision is not None}")
    if bottle_decision is not None:
        print(
            "bottle_decision: "
            f"angle={bottle_decision.next_view_angle_deg}, "
            f"command={bottle_decision.command.action}, "
            f"value={bottle_decision.command.value}, "
            f"reason={bottle_decision.reason}"
        )
    print(f"recheck_action_present: {recheck_action is not None}")
    if recheck_action is not None:
        print(
            "recheck_action: "
            f"action={recheck_action.action}, value={recheck_action.value}"
        )
    print(f"recheck_action_for_absent_scene: {no_recheck_action is not None}")


if __name__ == "__main__":
    main()
