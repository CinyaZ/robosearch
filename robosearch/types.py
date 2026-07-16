from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SearchStatus(str, Enum):
    IDLE = "IDLE"
    INITIALIZE = "INITIALIZE"
    CHECK_MEMORY = "CHECK_MEMORY"
    OBSERVE = "OBSERVE"
    EVALUATE_TARGET = "EVALUATE_TARGET"
    SELECT_LOCAL_VIEW = "SELECT_LOCAL_VIEW"
    SELECT_SEARCH_GOAL = "SELECT_SEARCH_GOAL"
    EXECUTE_ACTION = "EXECUTE_ACTION"
    VERIFY_TARGET = "VERIFY_TARGET"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ERROR = "ERROR"


@dataclass
class DetectionResult:
    label: str
    confidence: float
    bbox: Optional[List[float]] = None
    matched_target: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    waypoint_id: str
    view_angle_deg: float
    image_path: Optional[str] = None
    detections: List[DetectionResult] = field(default_factory=list)
    timestamp: str = ""


@dataclass
class ObjectMemory:
    target_label: str
    last_seen_waypoint_id: Optional[str] = None
    last_seen_angle_deg: Optional[float] = None
    confidence: float = 0.0
    found: bool = False
    timestamp: str = ""


@dataclass
class SearchContext:
    target_label: str
    current_waypoint_id: str
    visited_waypoints: List[str] = field(default_factory=list)
    visited_views: List[str] = field(default_factory=list)
    observation_count: int = 0
    action_count: int = 0


@dataclass
class SearchDecision:
    next_waypoint_id: Optional[str]
    next_view_angle_deg: Optional[float]
    score: float
    reason: str


@dataclass
class MotionCommand:
    action: str
    value: Optional[float] = None
    target_id: Optional[str] = None


@dataclass
class SearchResult:
    success: bool
    status: SearchStatus
    message: str
    target_label: str
