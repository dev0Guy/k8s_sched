from abc import abstractmethod
from typing import Protocol

from cloudcoil.models.kubernetes.core.v1 import NodeSystemInfo

from pkg.schedulers.base import CycleState, Status, Context
from pkg.schedulers.plugin.proto import PluginProtocol
from simulator.common import Pod


class FilterPlugin(PluginProtocol, Protocol):
    """
    These plugins are used to filter out nodes that cannot run the Pod.
    For each node, the scheduler will call filter plugins in their configured order.
    If any filter plugin marks the node as infeasible, the remaining plugins will not be called for that node.
    Nodes may be evaluated concurrently.
    """
    @abstractmethod
    def filter(self, ctx: Context, state: CycleState, pod: Pod, node_info: NodeSystemInfo) -> Status: ...