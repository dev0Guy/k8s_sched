from dataclasses import dataclass, field
from typing import Iterable

import numpy as np
import numpy.typing as npt


@dataclass
class Node:
    compute: Iterable[float]
    name: str = field(init=False)
    _usage: npt.NDArray[np.float64] = field(init=False)
    _instance_count: int = 0

    def __post_init__(self):
        if isinstance(self.compute, np.ndarray):
            self.compute = self.compute.astype(np.float64)
        self._usage = np.zeros_like(self.compute)
        self.name = f"node_{Node._instance_count}"
        Node._instance_count += 1

    @property
    def usage(self) -> npt.NDArray[np.float64]:
        return self._usage.copy()

    @property
    def free_compute(self) -> npt.NDArray[np.float64]:
        return self.compute - self._usage

    @usage.setter
    def usage(self, value: npt.NDArray[np.float64]) -> None:
        self._usage = value
