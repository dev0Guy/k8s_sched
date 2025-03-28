"""
Permit plugins are invoked at the end of the scheduling cycle for each Pod, to prevent or delay the binding to
the candidate node. A permit plugin can do one of the three things:

1. approve
    Once all Permit plugins approve a Pod, it is sent for binding.

2. deny
    If any Permit plugin denies a Pod, it is returned to the scheduling queue.
    This will trigger the Unreserve phase in Reserve plugins.

3. wait (with a timeout)
    If a Permit plugin returns "wait", then the Pod is kept in an internal "waiting" Pods list,
    and the binding cycle of this Pod starts but directly blocks until it gets approved.
    If a timeout occurs, wait becomes deny and the Pod is returned to the scheduling queue,
    triggering the Unreserve phase in Reserve plugins.
"""



from typing import Protocol, Tuple

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.schedulers.base import Context, CycleState, Status
from pkg.schedulers.plugin.proto import PluginProtocol


class Permit(PluginProtocol, Protocol):
    """
        A plugin that implements the Reserve interface has two methods, namely Reserve and Unreserve,
         that back two informational scheduling phases called Reserve and Unreserve, respectively.
         Plugins which maintain runtime state (aka "stateful plugins") should use these phases to be notified by the scheduler
        when resources on a node are being reserved and unreserved for a given Pod.
    """

    def permit(self, ctx: Context, state: CycleState, p: Pod, node_name: str) -> Tuple[Status, int]:
        """int is elapse time in seconds since the Unreserve phase."""
        ...
