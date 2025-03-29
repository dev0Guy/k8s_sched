from dataclasses import dataclass, field
import time
import enum
from typing import List, Optional, Set, Dict, Callable

from pydantic import BaseModel, NonNegativeInt, ConfigDict, Field

NodeNames = Set[str]


@dataclass
class Context:
    deadline: int = field(default_factory=lambda: time.time() + 60)


@dataclass
class NodeScore:
    name: str
    score: int


@dataclass
class CycleState:
    data: dict = field(default_factory=dict)


class Code(enum.IntEnum):
    Success = 0
    Error = 1
    Unschedulable = 2
    UnschedulableAndUnresolvable = 3
    Wait = 4
    Skip = 5
    Pending = 6


@dataclass
class Status:
    code: int
    error: Optional[Exception] = None
    plugin: Optional[str] = None
    reasons: List[str] = field(default=list)

    def is_success(self) -> bool:
        return self.code == Code.Success

    def is_rejected(self) -> bool:
        return self.code in (Code.Unschedulable, Code.UnschedulableAndUnresolvable, Code.Pending)


def prefix_alias_generator(prefix: str) -> Callable[[str], str]:
    def inner(name: str) -> str:
        return f'{prefix}{name}'
    return inner

class SimulatorAnnotation(BaseModel):
    running_tick_count: NonNegativeInt = Field(alias="runningTickCount")
    length: NonNegativeInt = Field(alias="length")
    scheduled_at_tick: Optional[NonNegativeInt] = Field(alias="scheduledAtTick", default=None)
    completed_at_tick: Optional[NonNegativeInt] = Field(alias="completedAtTick", default=None)

    model_config = ConfigDict(
        alias_generator=prefix_alias_generator('simulator.'),
        extra='allow'
    )


NodeToStatus = Dict[str, Status]
