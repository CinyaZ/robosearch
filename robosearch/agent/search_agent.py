from __future__ import annotations

from dataclasses import dataclass

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
