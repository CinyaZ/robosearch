from __future__ import annotations

from robosearch.executor.executor_base import RobotExecutor
from robosearch.types import MotionCommand


class MockExecutor(RobotExecutor):
    def execute(self, command: MotionCommand) -> str:
        return f"mock execute: action={command.action}, value={command.value}, target={command.target_id}"
