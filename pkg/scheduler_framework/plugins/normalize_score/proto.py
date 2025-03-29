from typing import Protocol, List

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.scheduler_framework.base import Context, CycleState, Status, NodeScore
from pkg.scheduler_framework.plugins.proto import PluginProtocol


class NormalizeScorePlugin(PluginProtocol, Protocol):
    """
    These plugins are used to modify scores before the scheduler computes a final ranking of Nodes.
    A plugins that registers for this extension point will be called with the Score results from the same plugins.
    This is called once per plugins per scheduling cycle.
    """

    def normalize_score(self, context: Context, state: CycleState, p: Pod, scores: List[NodeScore]) ->Status: ...
