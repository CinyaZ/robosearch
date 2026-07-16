from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

from robosearch.perception.detector_base import Detector
from robosearch.types import DetectionResult


@dataclass(frozen=True)
class MockScene:
    name: str
    detections: Sequence[DetectionResult]


class MockDetector(Detector):
    def __init__(self, target_label: str = "bottle") -> None:
        self.target_label = target_label

    def detect(self, image_path: str) -> List[DetectionResult]:
        scene = self.get_scene(scene_name=image_path)
        return [
            DetectionResult(
                label=item.label,
                confidence=item.confidence,
                bbox=item.bbox,
                matched_target=item.label == self.target_label,
                metadata={
                    **item.metadata,
                    "source": "mock",
                    "scene_name": scene.name,
                    "requested_image_path": image_path,
                },
            )
            for item in scene.detections
        ]

    def get_scene(self, scene_name: str) -> MockScene:
        scenes = {
            "target_present": MockScene(
                name="target_present",
                detections=[
                    DetectionResult(
                        label="bottle",
                        confidence=0.93,
                        bbox=[0.18, 0.22, 0.44, 0.78],
                        matched_target=False,
                        metadata={"note": "high confidence bottle target"},
                    ),
                    DetectionResult(
                        label="cup",
                        confidence=0.67,
                        bbox=[0.55, 0.26, 0.70, 0.64],
                        matched_target=False,
                        metadata={"note": "secondary cup candidate"},
                    )
                ],
            ),
            "target_absent": MockScene(
                name="target_absent",
                detections=[
                    DetectionResult(
                        label="chair",
                        confidence=0.88,
                        bbox=[0.05, 0.12, 0.61, 0.91],
                        matched_target=False,
                        metadata={"note": "non-target distractor"},
                    )
                ],
            ),
            "low_confidence_target": MockScene(
                name="low_confidence_target",
                detections=[
                    DetectionResult(
                        label="bottle",
                        confidence=0.34,
                        bbox=[0.51, 0.20, 0.73, 0.69],
                        matched_target=False,
                        metadata={"note": "low confidence bottle requires re-check"},
                    )
                ],
            ),
        }
        if scene_name not in scenes:
            raise ValueError(
                f"Unknown mock scene '{scene_name}'. "
                f"Available scenes: {', '.join(sorted(scenes))}."
            )
        return scenes[scene_name]
