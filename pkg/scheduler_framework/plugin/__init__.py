from pkg.scheduler_framework.plugin.queue_sort.proto import QueueSortPlugin
from pkg.scheduler_framework.plugin.pre_filter.proto import PreFilterPlugin
from pkg.scheduler_framework.plugin.filter.proto import FilterPlugin
from pkg.scheduler_framework.plugin.post_filter.proto import PostFilterPlugin
from pkg.scheduler_framework.plugin.pre_score.proto import PreScorePlugin
from pkg.scheduler_framework.plugin.score.proto import ScorePlugin
from pkg.scheduler_framework.plugin.normalize_score.proto import NormalizeScorePlugin
from pkg.scheduler_framework.plugin.reserve.proto import ReservePlugin
from pkg.scheduler_framework.plugin.permit.proto import PermitPlugin
from pkg.scheduler_framework.plugin.proto import PluginProtocol
from typing import TypeVar


Plugin = TypeVar("Plugin", bound=PluginProtocol)

