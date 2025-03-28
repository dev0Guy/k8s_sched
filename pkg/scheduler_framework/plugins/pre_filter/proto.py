from abc import abstractmethod
from typing import Protocol

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.base import Context, CycleState, Status, NodeNames
from pkg.scheduler_framework.plugins.proto import PluginProtocol
from result import Result


class PreFilterPlugin(PluginProtocol, Protocol):
    """
    These plugins are used to pre-process info about the Pod,
    or to check certain conditions that the cluster or the Pod must meet.
    If a PreFilter plugins returns an error, the scheduling cycle is aborted.
    """

    @abstractmethod
    def pre_filter(
        self,
        ctx: Context,
        state: CycleState,
        pod: Pod
    ) -> Result[NodeNames, Status]: ...
