from __future__ import annotations

from pathlib import Path

from robosearch.memory.json_store import JsonStore
from robosearch.memory.memory_manager import MemoryManager
from robosearch.perception.mock_detector import MockDetector
from robosearch.types import Observation


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    memory_path = project_root / "work" / "memory_demo_store.json"

    detector = MockDetector(target_label="bottle")
    store = JsonStore(memory_path)
    memory_manager = MemoryManager(store)
    memory_manager.clear()

    positive_observation = Observation(
        waypoint_id="living_room_table",
        view_angle_deg=0.0,
        image_path="target_present",
        detections=detector.detect("target_present"),
        timestamp="2026-07-16T20:30:00Z",
    )
    negative_observation = Observation(
        waypoint_id="bookshelf",
        view_angle_deg=45.0,
        image_path="target_absent",
        detections=detector.detect("target_absent"),
        timestamp="2026-07-16T20:31:00Z",
    )

    saved_memory = memory_manager.record_observation(
        observation=positive_observation,
        target_label="bottle",
    )
    no_hit_memory = memory_manager.record_observation(
        observation=negative_observation,
        target_label="bottle",
    )
    loaded_memory = memory_manager.get_last_seen_memory("bottle")
    searched_current_view = memory_manager.has_searched_view("living_room_table", 0.0)
    searched_negative_view = memory_manager.has_searched_view("bookshelf", 45.0)
    bottle_view_recorded = memory_manager.has_searched_target_view(
        "bottle", "living_room_table", 0.0
    )
    cup_view_recorded = memory_manager.has_searched_target_view(
        "cup", "living_room_table", 0.0
    )

    print("=== RoboSearch Stage 2 Memory Demo ===")
    print(f"memory_path: {memory_path}")
    print(f"saved_memory_found: {saved_memory is not None}")
    if saved_memory is not None:
        print(
            "saved_memory: "
            f"target={saved_memory.target_label}, "
            f"waypoint={saved_memory.last_seen_waypoint_id}, "
            f"angle={saved_memory.last_seen_angle_deg}, "
            f"confidence={saved_memory.confidence:.2f}, "
            f"timestamp={saved_memory.timestamp}"
        )
    print(f"no_hit_memory_returned: {no_hit_memory is not None}")
    print(f"searched_current_view: {searched_current_view}")
    print(f"searched_negative_view: {searched_negative_view}")
    print(f"bottle_view_recorded: {bottle_view_recorded}")
    print(f"cup_view_recorded: {cup_view_recorded}")
    print(f"loaded_memory_found: {loaded_memory is not None}")
    if loaded_memory is not None:
        print(
            "loaded_memory: "
            f"target={loaded_memory.target_label}, "
            f"waypoint={loaded_memory.last_seen_waypoint_id}, "
            f"angle={loaded_memory.last_seen_angle_deg}, "
            f"confidence={loaded_memory.confidence:.2f}, "
            f"timestamp={loaded_memory.timestamp}"
        )
    print("expected_last_seen_preserved: True")
    print(f"visited_view_count: {len(memory_manager.list_visited_views())}")


if __name__ == "__main__":
    main()
