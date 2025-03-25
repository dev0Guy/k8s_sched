from dataclasses import dataclass, field
from functools import cached_property
from enum import IntEnum
from typing import Iterable, Optional
import numpy.typing as npt
import numpy as np


class Status(IntEnum):
    UN_AVAILABLE = 0
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3


@dataclass
class PodManageFields:
    status: Status = field(default=Status.UN_AVAILABLE)
    arrival_time: int = field(default=0)
    start_run_time: Optional[int] = field(default=None)
    completion_time: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    length: npt.DTypeLike = field(default=0)


@dataclass
class Pod:
    limit: npt.NDArray[np.float64]
    _manage_fields: PodManageFields
    _instance_count: int = 0

    def __post_init__(self):

        if not isinstance(self.limit, np.ndarray):
            self.limit = np.array(self.limit).astype(np.float64)
            self.limit = np.atleast_2d(self.limit)

        if self._manage_fields.name is None:
            self._manage_fields.name = f"{Pod.__name__}_{Pod._instance_count}"
            Pod._instance_count += 1

        reversed_nonzero = np.argmax(self.limit[:, ::-1] != 0, axis=1)
        self._manage_fields.length = np.where(
            self.limit.any(axis=1),
            self.limit.shape[1] - 1 - reversed_nonzero, -1
        ).max()

    @property
    def length(self) -> npt.DTypeLike:
        return self._manage_fields.length

    @property
    def arrival_time(self) -> int:
        return self._manage_fields.arrival_time

    @property
    def status(self) -> Status:
        return self._manage_fields.status

    @property
    def name(self) -> str:
        return self._manage_fields.name

    @property
    def idle_time(self) -> Optional[int]:
        if self._manage_fields.status not in (Status.RUNNING, Status.COMPLETED):
            return None

        return self._manage_fields.arrival_time - self._manage_fields.start_run_time

    @property
    def run_time(self) -> Optional[int]:
        if self._manage_fields.status != Status.COMPLETED:
            return None

        return self._manage_fields.start_run_time - self._manage_fields.completion_time

    @property
    def start_run_time(self) -> Optional[int]:
        return self._manage_fields.start_run_time

    @property
    def completion_time(self) -> Optional[int]:
        return self._manage_fields.completion_time

    @completion_time.setter
    def completion_time(self, completion_time: int) -> None:
        if self._manage_fields.status != Status.RUNNING:
            raise ValueError("Cannot set completion time for pod without a running pod")
        self._manage_fields.completion_time = completion_time
        self._manage_fields.status = Status.COMPLETED

    @start_run_time.setter
    def start_run_time(self, value: int) -> None:
        self._manage_fields.start_run_time = value
        self._manage_fields.status = Status.RUNNING
