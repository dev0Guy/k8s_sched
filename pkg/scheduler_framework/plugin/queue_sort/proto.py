from typing import Protocol

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.plugin.proto import PluginProtocol


class QueueSortPlugin(PluginProtocol, Protocol):
    """
        These plugins are used to sort Pods in the scheduling queue.
        A queue sort plugin essentially provides a Less(Pod1, Pod2) function.
        Only one queue sort plugin may be enabled at a time.
    """

    def less(self, p1: Pod, p2: Pod) -> bool: ...
