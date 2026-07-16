from __future__ import annotations

from typing import List

from robosearch.perception.detector_base import Detector
from robosearch.types import DetectionResult


class MindSporeDetector(Detector):
    def detect(self, image_path: str) -> List[DetectionResult]:
        raise NotImplementedError(
            "MindSporeDetector will be implemented in a later stage."
        )
