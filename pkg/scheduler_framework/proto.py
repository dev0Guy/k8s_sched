from typing import Generic
from dataclasses import dataclass, field
from pkg.scheduler_framework.plugin import (
    QueueSortPlugin,
    PreFilterPlugin,
    FilterPlugin,
    PostFilterPlugin,
    PreScorePlugin,
    ScorePlugin,
    NormalizeScorePlugin,
    ReservePlugin,
    PermitPlugin,
    Plugin
)


@dataclass(frozen=True)
class PluginSet(Generic[Plugin]):
    enabled: list[Plugin] = field(default_factory=list)
    disabled: list[Plugin] = field(default_factory=list)


@dataclass
class Plugins:
    queue_sort: PluginSet[QueueSortPlugin] = field(default_factory=list)
    prefilter: PluginSet[PreFilterPlugin] = field(default_factory=list)
    filter: PluginSet[FilterPlugin] = field(default_factory=list)
    post_filter: PluginSet[PostFilterPlugin] = field(default_factory=list)
    pre_score: PluginSet[PreScorePlugin] = field(default_factory=list)
    score: PluginSet[ScorePlugin] = field(default_factory=list)
    normalize_score: PluginSet[NormalizeScorePlugin] = field(default_factory=list)
    reserve: PluginSet[ReservePlugin] = field(default_factory=list)
    permit: PluginSet[PermitPlugin] = field(default_factory=list)
