from typing import Protocol

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.base import Context, CycleState, NodeToStatus
from pkg.scheduler_framework.plugin.proto import PluginProtocol


class PostFilterPlugin(PluginProtocol, Protocol):
    """
    These plugins are called after the Filter phase, but only when no feasible nodes were found for the pod.
    Plugins are called in their configured order.
    If any postFilter plugin marks the node as Schedulable, the remaining plugins will not be called.
    A typical PostFilter implementation is preemption, which tries to make the pod schedulable by preempting other Pods.
    """
    def post_filter(self, ctx: Context, state: CycleState, pod: Pod, filtered_node_status: NodeToStatus): ...
