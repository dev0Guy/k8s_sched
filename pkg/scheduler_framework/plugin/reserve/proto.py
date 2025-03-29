from typing import Protocol

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.base import Context, CycleState, Status
from pkg.scheduler_framework.plugin.proto import PluginProtocol


class ReservePlugin(PluginProtocol, Protocol):
    """
        A plugin that implements the Reserve interface has two methods, namely Reserve and Unreserve,
         that back two informational scheduling phases called Reserve and Unreserve, respectively.
         Plugins which maintain runtime state (aka "stateful plugins") should use these phases to be notified by the scheduler
        when resources on a node are being reserved and unreserved for a given Pod.
    """
    def reserve(self, ctx: Context, state: CycleState, p: Pod, node_name: str) -> Status: ...
    def un_reserve(self, ctx: Context, state: CycleState, p: Pod, node_name: str) -> None: ...

