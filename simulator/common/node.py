from simulator.common.pod import Pod
from dataclasses import dataclass, field
from typing import Iterable, List

import numpy as np
import numpy.typing as npt


@dataclass
class Node:
    compute: Iterable[float]
    _usage: npt.NDArray[np.float64] = field(init=False)
    _instance_count: int = 0
    _name: str = field(init=False)
    _history_of_pods: List[Pod] = field(init=False, default_factory=list)

    def __post_init__(self):
        if isinstance(self.compute, np.ndarray):
            self.compute = self.compute.astype(np.float64)
        self._usage = np.zeros_like(self.compute)
        self._name = f"{Node.__name__}_{Node._instance_count}"
        Node._instance_count += 1

    def allocate(self, p: Pod) -> None:
        self._history_of_pods.append(p)
        self._usage += p.limit

    def can_allocate(self, p: Pod) -> bool:
        return bool(np.all(self.compute - self._usage >= p.limit))

    @property
    def name(self) -> str:
        return self._name

    @property
    def usage(self) -> npt.NDArray[np.float64]:
        return self._usage.copy()

    @property
    def free_compute(self) -> npt.NDArray[np.float64]:
        return self.compute - self._usage

    @usage.setter
    def usage(self, value: npt.NDArray[np.float64]) -> None:
        self._usage = value
