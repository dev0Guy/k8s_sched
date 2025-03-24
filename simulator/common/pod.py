from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterable

import numpy as np


class PodStatus(IntEnum):
    UN_AVAILABLE = 0
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3


@dataclass
class Pod:
    limit: Iterable[float]
    """On pod configuration max number of resource allowed to pod"""
    _status: PodStatus = field(default=PodStatus.UN_AVAILABLE)
    name: str = field(init=False)
    _instance_count: int = 0

    def __post_init__(self):
        if isinstance(self.limit, np.ndarray):
            self.limit = self.limit.astype(np.float64)
        self.name = f"pod_{Pod._instance_count}"
        Pod._instance_count += 1

    @property
    def status(self) -> PodStatus:
        return self._status

    @status.setter
    def status(self, s: PodStatus) -> None:
        self._status = s
