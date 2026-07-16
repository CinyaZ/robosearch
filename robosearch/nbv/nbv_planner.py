from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from robosearch.types import DetectionResult, MotionCommand


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
