from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from robosearch.memory.json_store import JsonStore
from robosearch.types import ObjectMemory


class MemoryManager:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def get_object_memory(self, target_label: str) -> Optional[ObjectMemory]:
        data = self.store.load()
        item = data.get(target_label)
        if item is None:
            return None
        return ObjectMemory(**item)

    def save_object_memory(self, memory: ObjectMemory) -> None:
        data = self.store.load()
        data[memory.target_label] = asdict(memory)
        self.store.save(data)
