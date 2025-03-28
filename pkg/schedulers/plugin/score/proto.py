from typing import Protocol, Tuple

from cloudcoil.models.kubernetes.core.v1 import Pod

from pkg.schedulers.base import Context, CycleState, Status
from pkg.schedulers.plugin.proto import PluginProtocol


class Score(PluginProtocol, Protocol):
    """
    These plugins are used to rank nodes that have passed the filtering phase.
    The scheduler will call each scoring plugin for each node.
    There will be a well-defined range of integers representing the minimum and maximum scores.
    After the NormalizeScore phase, the scheduler will combine node scores from all plugins according to the configured
    plugin weights.
    """

    def score(self, context: Context, state: CycleState, p: Pod, node_name: str) -> Tuple[int, Status]: ...
