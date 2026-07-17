from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

from robosearch.types import DetectionResult, MotionCommand, NBVDecision


@dataclass
class NBVPlanner:
    view_angles_deg: List[float]
    low_confidence_threshold: float = 0.5
    max_local_views: Optional[int] = None

    def get_default_view_sequence(self) -> List[float]:
        return list(self.view_angles_deg)

    def select_next_view_angle(self, visited_angles_deg: List[float]) -> Optional[float]:
        remaining_angles = [
            angle for angle in self.view_angles_deg if angle not in set(visited_angles_deg)
        ]
        if self.max_local_views is not None:
            max_candidates = max(self.max_local_views - len(visited_angles_deg), 0)
            remaining_angles = remaining_angles[:max_candidates]
        if not remaining_angles:
            return None
        return remaining_angles[0]

    def select_next_target_view_angle(
        self,
        target_label: str,
        waypoint_id: str,
        visited_angles_deg: List[float],
        has_searched_target_view: Callable[[str, str, float], bool],
    ) -> Optional[float]:
        candidates = [
            angle
            for angle in self.view_angles_deg
            if angle not in set(visited_angles_deg)
            and not has_searched_target_view(target_label, waypoint_id, angle)
        ]
        if self.max_local_views is not None:
            max_candidates = max(self.max_local_views - len(visited_angles_deg), 0)
            candidates = candidates[:max_candidates]
        if not candidates:
            return None
        return candidates[0]

    def select_next_target_view_decision(
        self,
        target_label: str,
        waypoint_id: str,
        visited_angles_deg: List[float],
        has_searched_target_view: Callable[[str, str, float], bool],
    ) -> Optional[NBVDecision]:
        next_angle = self.select_next_target_view_angle(
            target_label=target_label,
            waypoint_id=waypoint_id,
            visited_angles_deg=visited_angles_deg,
            has_searched_target_view=has_searched_target_view,
        )
        if next_angle is None:
            return None
        return NBVDecision(
            next_view_angle_deg=next_angle,
            command=MotionCommand(action="rotate", value=next_angle),
            reason=(
                f"Selected next unsearched local view for target '{target_label}' "
                f"at waypoint '{waypoint_id}'."
            ),
        )

    def suggest_recheck_action(
        self, detections: List[DetectionResult], target_label: str
    ) -> Optional[MotionCommand]:
        low_confidence_match = self._find_low_confidence_match(detections, target_label)
        if low_confidence_match is None:
            return None

        bbox = low_confidence_match.bbox or [0.0, 0.0, 1.0, 1.0]
        center_x = (bbox[0] + bbox[2]) / 2.0

        if center_x < 0.4:
            return MotionCommand(action="rotate", value=-15.0)
        if center_x > 0.6:
            return MotionCommand(action="rotate", value=15.0)
        return MotionCommand(action="recheck", value=0.0)

    def _find_low_confidence_match(
        self, detections: List[DetectionResult], target_label: str
    ) -> Optional[DetectionResult]:
        candidates = [
            item
            for item in detections
            if item.label == target_label and item.confidence < self.low_confidence_threshold
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda item: item.confidence)
