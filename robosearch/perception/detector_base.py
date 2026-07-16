from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from robosearch.types import DetectionResult


class Detector(ABC):
    @abstractmethod
    def detect(self, image_path: str) -> List[DetectionResult]:
        raise NotImplementedError
