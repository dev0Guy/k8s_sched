
from typing import Protocol, List

from cloudcoil.models.kubernetes.core.v1 import Pod, Node

from pkg.schedulers.base import Context, CycleState, Status
from pkg.schedulers.plugin.proto import PluginProtocol


class PreScore(PluginProtocol, Protocol):
    """
    These plugins are used to perform "pre-scoring" work, which generates a sharable state for Score plugins to use.
    If a PreScore plugin returns an error, the scheduling cycle is aborted.
    """

    def pre_score(self, context: Context, state: CycleState, pod: Pod, nodes: List[Node]) -> Status: ...

