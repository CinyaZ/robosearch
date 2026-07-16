from __future__ import annotations

from typing import List

from robosearch.perception.detector_base import Detector
from robosearch.types import DetectionResult


class MockDetector(Detector):
    def detect(self, image_path: str) -> List[DetectionResult]:
        return [
            DetectionResult(
                label="bottle",
                confidence=0.1,
                bbox=[0.1, 0.1, 0.2, 0.4],
                matched_target=False,
                metadata={"source": "mock", "image_path": image_path},
            )
        ]
