from abc import abstractmethod
from typing import Protocol, List

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.plugins.proto import PluginProtocol


class QueueSortPlugin(PluginProtocol, Protocol):
    """
        These plugins are used to sort Pods in the scheduling queue.
        A queue sort plugins essentially provides a Less(Pod1, Pod2) function.
        Only one queue sort plugins may be enabled at a time.
    """

    @abstractmethod
    def less(self, p1: Pod, p2: Pod) -> bool: ...

    def sort(self, pods: List[Pod]) -> List[Pod]:
        return pods
