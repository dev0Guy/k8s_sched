import abc
import asyncio
from typing import Optional, List, Tuple, Iterable

from cloudcoil.models.kubernetes.core.v1 import Pod, Node, PodStatus
from cloudcoil.resources import ResourceList
from pydantic import NonNegativeInt
from result import Result

from pkg.scheduler_framework.base import SimulatorAnnotation
from plugins import Plugins  # noqa: F401


def get_pods_by_status(status: str, *, should_wait: bool = False) -> List[Pod]:
    filed_selector = "status.phase={}".format(status)
    if should_wait:
        _ = next(Pod.watch(field_selector=filed_selector))
    return Pod.list(field_selector=filed_selector).items


class AbstractScheduler(abc.ABC):
    _current_tick: NonNegativeInt

    @abc.abstractmethod
    def schedule(self) -> Result[Tuple[Pod, Node], Exception]: ...

    @classmethod
    def get_simulator_annotation(cls, p: Pod) -> SimulatorAnnotation:
        return SimulatorAnnotation(**p.metadata.annotations)

    def clock_forward(self) -> None:
        """Move all pods time_running +1 and update all of their status"""
        running_pods_annotation = map(self.get_simulator_annotation, get_pods_by_status("Running"))

        # TODO: update annotation by tick
        # when completed change the pod status
        # check for arriving jobs and submit them on install
        #
        # for p in running_pods_annotation:
        #     if p.length == p.time_running:
        #         p.completed_at = self._current_tick
        #     else:
        #         p.time_running += 1

