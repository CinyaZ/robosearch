from __future__ import annotations

from dataclasses import dataclass

from robosearch.types import SearchStatus


@dataclass
class SearchFSM:
    status: SearchStatus = SearchStatus.IDLE

    def transition(self, new_status: SearchStatus) -> None:
        self.status = new_status
