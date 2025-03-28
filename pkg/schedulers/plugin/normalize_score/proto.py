from typing import Protocol, List

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.schedulers.base import Context, CycleState, Status, NodeScore
from pkg.schedulers.plugin.proto import PluginProtocol


class NormalizeScore(PluginProtocol, Protocol):
    """
    These plugins are used to modify scores before the scheduler computes a final ranking of Nodes.
    A plugin that registers for this extension point will be called with the Score results from the same plugin.
    This is called once per plugin per scheduling cycle.
    """

    def normalize_score(self, context: Context, state: CycleState, p: Pod, scores: List[NodeScore]) ->Status: ...
