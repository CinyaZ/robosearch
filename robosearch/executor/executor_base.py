from __future__ import annotations

from abc import ABC, abstractmethod

from robosearch.types import MotionCommand


class RobotExecutor(ABC):
    @abstractmethod
    def execute(self, command: MotionCommand) -> str:
        raise NotImplementedError
