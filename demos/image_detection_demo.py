from __future__ import annotations

from robosearch.perception.mock_detector import MockDetector


def main() -> None:
    target_labels = ["bottle", "cup", "book"]
    scene_names = [
        "target_present",
        "target_absent",
        "low_confidence_target",
    ]

    print("=== RoboSearch Stage 1 MockDetector Demo ===")
    for target_label in target_labels:
        detector = MockDetector(target_label=target_label)
        print(f"target_label: {target_label}")
        for scene_name in scene_names:
            detections = detector.detect(scene_name)
            print(f"  scene: {scene_name}")
            if not detections:
                print("    detections: none")
                continue
            for index, detection in enumerate(detections, start=1):
                print(
                    "    "
                    f"[{index}] label={detection.label}, "
                    f"confidence={detection.confidence:.2f}, "
                    f"matched_target={detection.matched_target}, "
                    f"bbox={detection.bbox}, "
                    f"note={detection.metadata.get('note', '')}"
                )


if __name__ == "__main__":
    main()
