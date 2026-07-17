from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from robosearch.executor.executor_base import RobotExecutor
from robosearch.memory.memory_manager import MemoryManager
from robosearch.nbv.nbv_planner import NBVPlanner
from robosearch.observation.observation_manager import ObservationManager
from robosearch.perception.detector_base import Detector
from robosearch.planner.search_planner import SearchPlanner
from robosearch.state_machine.search_fsm import SearchFSM
from robosearch.types import MotionCommand
from robosearch.types import SearchContext, SearchResult, SearchStatus


@dataclass
class SearchAgent:
    name: str = "RoboSearchAgent"

    def bootstrap(self, target_label: str) -> SearchResult:
        context = SearchContext(
            target_label=target_label,
            current_waypoint_id="living_room_table",
        )
        return SearchResult(
            success=False,
            status=SearchStatus.INITIALIZE,
            message=(
                f"{self.name} initialized for target '{context.target_label}' "
                f"at waypoint '{context.current_waypoint_id}'."
            ),
            target_label=target_label,
        )

    def run_mock_search(
        self,
        target_label: str,
        initial_waypoint_id: str,
        candidate_waypoints: List[str],
        waypoint_scene_map: Dict[str, str],
        detector: Detector,
        memory_manager: MemoryManager,
        nbv_planner: NBVPlanner,
        search_planner: SearchPlanner,
        executor: RobotExecutor,
        observation_manager: ObservationManager,
        max_waypoints: int = 3,
    ) -> SearchResult:
        fsm = SearchFSM(status=SearchStatus.INITIALIZE)
        context = SearchContext(
            target_label=target_label,
            current_waypoint_id=initial_waypoint_id,
        )
        failure_counts: Dict[str, int] = {}
        search_log: List[str] = []

        while len(context.visited_waypoints) < max_waypoints:
            current_waypoint = context.current_waypoint_id
            if current_waypoint not in context.visited_waypoints:
                context.visited_waypoints.append(current_waypoint)

            fsm.transition(SearchStatus.OBSERVE)
            search_log.append(f"observe:{current_waypoint}")

            local_view_sequence = nbv_planner.get_default_view_sequence()
            for view_angle in local_view_sequence:
                context.observation_count += 1
                search_log.append(f"view:{current_waypoint}@{view_angle}")
                observation = observation_manager.create_observation(
                    waypoint_id=current_waypoint,
                    view_angle_deg=float(view_angle),
                )
                scene_name = waypoint_scene_map.get(current_waypoint, "target_absent")
                observation.image_path = scene_name
                observation.detections = detector.detect(scene_name)
                memory_manager.record_observation(
                    observation=observation,
                    target_label=target_label,
                )
                context.visited_views.append(f"{current_waypoint}:{view_angle}")

                matched = [
                    item for item in observation.detections if item.label == target_label
                ]
                if matched:
                    fsm.transition(SearchStatus.SUCCESS)
                    confidence = max(item.confidence for item in matched)
                    search_log.append(
                        f"found:{current_waypoint}@{view_angle}:{confidence:.2f}"
                    )
                    return SearchResult(
                        success=True,
                        status=SearchStatus.SUCCESS,
                        message=(
                            f"Found target '{target_label}' at waypoint '{current_waypoint}' "
                            f"with confidence {confidence:.2f}. "
                            f"Search log: {' -> '.join(search_log)}"
                        ),
                        target_label=target_label,
                    )

            failure_counts[current_waypoint] = failure_counts.get(current_waypoint, 0) + 1
            fsm.transition(SearchStatus.SELECT_SEARCH_GOAL)
            search_log.append(f"planner:{current_waypoint}")

            remaining_waypoints = [
                item for item in candidate_waypoints if item not in context.visited_waypoints
            ]
            decision = search_planner.select_next_waypoint(
                context=context,
                candidate_waypoints=remaining_waypoints,
                failure_counts=failure_counts,
            )
            if decision.waypoint_id is None:
                fsm.transition(SearchStatus.FAILURE)
                search_log.append("failure:no_waypoint")
                return SearchResult(
                    success=False,
                    status=SearchStatus.FAILURE,
                    message=(
                        f"Search failed for target '{target_label}'. "
                        f"No waypoint left to visit. Search log: {' -> '.join(search_log)}"
                    ),
                    target_label=target_label,
                )

            fsm.transition(SearchStatus.EXECUTE_ACTION)
            command = MotionCommand(action="go_to_waypoint", target_id=decision.waypoint_id)
            executor.execute(command)
            search_log.append(
                f"decision:{decision.waypoint_id}:{decision.score:.2f}"
            )
            search_log.append(f"move:{decision.waypoint_id}")
            context.current_waypoint_id = decision.waypoint_id

        fsm.transition(SearchStatus.FAILURE)
        search_log.append("failure:max_waypoints")
        return SearchResult(
            success=False,
            status=SearchStatus.FAILURE,
            message=(
                f"Search failed for target '{target_label}' after visiting "
                f"{len(context.visited_waypoints)} waypoint(s). "
                f"Search log: {' -> '.join(search_log)}"
            ),
            target_label=target_label,
        )
