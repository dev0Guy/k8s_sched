from dataclasses import dataclass, field
import time
import enum
from typing import List, Optional, Set, Dict

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


NodeToStatus = Dict[str, Status]
