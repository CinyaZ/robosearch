from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from robosearch.api import load_yaml_config


@dataclass
class PriorDatabase:
    priors: Dict[str, Dict[str, float]]

    @classmethod
    def from_yaml(cls, path: str) -> "PriorDatabase":
        data = load_yaml_config(path)
        priors = data.get("object_priors", {})
        if not isinstance(priors, dict):
            raise ValueError("object_priors must be a mapping.")
        return cls(priors=priors)
