from typing import Protocol
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
)


class SchedulerProtocol(Protocol):
    ...