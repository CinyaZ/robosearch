from __future__ import annotations

from pathlib import Path

from robosearch.api import load_yaml_config
from robosearch.nbv.nbv_planner import NBVPlanner
from robosearch.perception.mock_detector import MockDetector


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    planner_config = load_yaml_config(project_root / "configs" / "planner.yaml")

    planner = NBVPlanner(
        view_angles_deg=planner_config["default_turn_angles"],
        low_confidence_threshold=0.5,
        max_local_views=5,
    )

    visited_angles = [0.0, 45.0]
    next_view = planner.select_next_view_angle(visited_angles)

    detector = MockDetector(target_label="bottle")
    low_confidence_detections = detector.detect("low_confidence_target")
    absent_detections = detector.detect("target_absent")

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
    print(f"recheck_action_present: {recheck_action is not None}")
    if recheck_action is not None:
        print(
            "recheck_action: "
            f"action={recheck_action.action}, value={recheck_action.value}"
        )
    print(f"recheck_action_for_absent_scene: {no_recheck_action is not None}")


if __name__ == "__main__":
    main()
