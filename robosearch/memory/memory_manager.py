from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Optional

from robosearch.memory.json_store import JsonStore
from robosearch.types import DetectionResult, ObjectMemory, Observation


class MemoryManager:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def record_observation(
        self, observation: Observation, target_label: str
    ) -> Optional[ObjectMemory]:
        data = self.store.load()
        found_target = self._find_best_match(observation.detections, target_label) is not None
        visited_views = self._get_visited_views(data)
        visited_views.append(
            {
                "waypoint_id": observation.waypoint_id,
                "view_angle_deg": observation.view_angle_deg,
                "timestamp": observation.timestamp,
                "target_label": target_label,
                "found_target": found_target,
            }
        )
        data["visited_views"] = visited_views
        self._mark_searched_target_view(
            data=data,
            target_label=target_label,
            waypoint_id=observation.waypoint_id,
            view_angle_deg=observation.view_angle_deg,
            found_target=found_target,
        )

        last_seen_memory = self._build_object_memory(observation, target_label)
        if last_seen_memory is not None:
            data.setdefault("object_memories", {})
            data["object_memories"][target_label] = asdict(last_seen_memory)

        self.store.save(data)
        return last_seen_memory

    def get_object_memory(self, target_label: str) -> Optional[ObjectMemory]:
        data = self.store.load()
        object_memories = data.get("object_memories", {})
        item = object_memories.get(target_label)
        if item is None:
            return None
        return ObjectMemory(**item)

    def save_object_memory(self, memory: ObjectMemory) -> None:
        data = self.store.load()
        data.setdefault("object_memories", {})
        data["object_memories"][memory.target_label] = asdict(memory)
        self.store.save(data)

    def get_last_seen_memory(self, target_label: str) -> Optional[ObjectMemory]:
        return self.get_object_memory(target_label)

    def has_searched_view(self, waypoint_id: str, view_angle_deg: float) -> bool:
        data = self.store.load()
        visited_views = self._get_visited_views(data)
        return any(
            item["waypoint_id"] == waypoint_id
            and float(item["view_angle_deg"]) == float(view_angle_deg)
            for item in visited_views
        )

    def has_searched_target_view(
        self, target_label: str, waypoint_id: str, view_angle_deg: float
    ) -> bool:
        data = self.store.load()
        searched_target_views = self._get_searched_target_views(data)
        key = self._build_target_view_key(target_label, waypoint_id, view_angle_deg)
        return key in searched_target_views

    def list_visited_views(self) -> List[Dict[str, object]]:
        data = self.store.load()
        return self._get_visited_views(data)

    def clear(self) -> None:
        self.store.save({})

    def _build_object_memory(
        self, observation: Observation, target_label: str
    ) -> Optional[ObjectMemory]:
        matched_detection = self._find_best_match(observation.detections, target_label)
        if matched_detection is None:
            return None
        return ObjectMemory(
            target_label=target_label,
            last_seen_waypoint_id=observation.waypoint_id,
            last_seen_angle_deg=observation.view_angle_deg,
            confidence=matched_detection.confidence,
            found=True,
            timestamp=observation.timestamp,
        )

    def _find_best_match(
        self, detections: List[DetectionResult], target_label: str
    ) -> Optional[DetectionResult]:
        matches = [item for item in detections if item.label == target_label]
        if not matches:
            return None
        return max(matches, key=lambda item: item.confidence)

    def _get_visited_views(self, data: Dict[str, object]) -> List[Dict[str, object]]:
        visited_views = data.get("visited_views", [])
        if not isinstance(visited_views, list):
            raise ValueError("visited_views must be a list in memory store.")
        return visited_views

    def _get_searched_target_views(
        self, data: Dict[str, object]
    ) -> Dict[str, Dict[str, object]]:
        searched_target_views = data.get("searched_target_views", {})
        if not isinstance(searched_target_views, dict):
            raise ValueError("searched_target_views must be a mapping in memory store.")
        return searched_target_views

    def _mark_searched_target_view(
        self,
        data: Dict[str, object],
        target_label: str,
        waypoint_id: str,
        view_angle_deg: float,
        found_target: bool,
    ) -> None:
        searched_target_views = self._get_searched_target_views(data)
        key = self._build_target_view_key(target_label, waypoint_id, view_angle_deg)
        searched_target_views[key] = {
            "target_label": target_label,
            "waypoint_id": waypoint_id,
            "view_angle_deg": float(view_angle_deg),
            "found_target": found_target,
        }
        data["searched_target_views"] = searched_target_views

    def _build_target_view_key(
        self, target_label: str, waypoint_id: str, view_angle_deg: float
    ) -> str:
        normalized_angle = float(view_angle_deg)
        return f"{target_label}::{waypoint_id}::{normalized_angle:.2f}"
