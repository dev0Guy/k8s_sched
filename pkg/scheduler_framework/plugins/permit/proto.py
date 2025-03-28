from abc import abstractmethod
from typing import Protocol, Tuple
from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.base import Context, CycleState, Status
from pkg.scheduler_framework.plugins.proto import PluginProtocol


class PermitPlugin(PluginProtocol, Protocol):
    """
    Permit plugins are invoked at the end of the scheduling cycle for each Pod, to prevent or delay the binding to
    the candidate node. A permit plugins can do one of the three things:

    1. approve
        Once all Permit plugins approve a Pod, it is sent for binding.

    2. deny
        If any Permit plugins denies a Pod, it is returned to the scheduling queue.
        This will trigger the Unreserve phase in Reserve plugins.

    3. wait (with a timeout)
        If a Permit plugins returns "wait", then the Pod is kept in an internal "waiting" Pods list,
        and the binding cycle of this Pod starts but directly blocks until it gets approved.
        If a timeout occurs, wait becomes deny and the Pod is returned to the scheduling queue,
        triggering the Unreserve phase in Reserve plugins.
    """

    @abstractmethod
    def permit(self, ctx: Context, state: CycleState, p: Pod, node_name: str) -> Tuple[Status, int]:
        """int is elapse time in seconds since the Unreserve phase."""
        ...
