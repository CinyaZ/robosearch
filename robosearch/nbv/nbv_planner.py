from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class NBVPlanner:
    view_angles_deg: List[float]

    def get_default_view_sequence(self) -> List[float]:
        return list(self.view_angles_deg)
