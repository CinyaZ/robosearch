from __future__ import annotations

from robosearch.executor.executor_base import RobotExecutor
from robosearch.types import MotionCommand


class ManualExecutor(RobotExecutor):
    def execute(self, command: MotionCommand) -> str:
        return (
            "manual execute requested: "
            f"action={command.action}, value={command.value}, target={command.target_id}"
        )
