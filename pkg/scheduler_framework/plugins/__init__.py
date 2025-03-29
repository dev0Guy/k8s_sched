from pkg.scheduler_framework.plugins.queue_sort.proto import QueueSortPlugin
from pkg.scheduler_framework.plugins.pre_filter.proto import PreFilterPlugin
from pkg.scheduler_framework.plugins.filter.proto import FilterPlugin
from pkg.scheduler_framework.plugins.post_filter.proto import PostFilterPlugin
from pkg.scheduler_framework.plugins.pre_score.proto import PreScorePlugin
from pkg.scheduler_framework.plugins.score.proto import ScorePlugin
from pkg.scheduler_framework.plugins.normalize_score.proto import NormalizeScorePlugin
from pkg.scheduler_framework.plugins.reserve.proto import ReservePlugin
from pkg.scheduler_framework.plugins.permit.proto import PermitPlugin
from pkg.scheduler_framework.plugins.proto import PluginProtocol
from typing import TypeVar


Plugin = TypeVar("Plugin", bound=PluginProtocol)

