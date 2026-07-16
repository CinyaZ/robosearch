from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from robosearch.types import Observation


@dataclass
class ObservationManager:
    def create_observation(self, waypoint_id: str, view_angle_deg: float) -> Observation:
        return Observation(
            waypoint_id=waypoint_id,
            view_angle_deg=view_angle_deg,
            timestamp=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
