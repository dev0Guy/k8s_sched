from abc import ABC,  abstractmethod
from typing import Iterable, Optional, Protocol, Tuple

from result import Err, Ok, Result

from simulator.common.node import Node
from simulator.common.pod import Pod, Status
import numpy as np

class SchedulerProtocol(Protocol):
    def schedule(
        self, pods: Iterable[Pod], nodes: Iterable[Node]
    ) -> Optional[Tuple[Pod, Node]]: ...


class ABCK8sScheduler(ABC):
    @abstractmethod
    def pick(self, pods: Iterable[Pod]) -> Optional[Pod]: ...
    @abstractmethod
    def score(self, p: Pod, nodes: Iterable[Node]) -> Iterable[Tuple[Node, float]]: ...

    @abstractmethod
    def normalize(
        self, nodes: Iterable[Tuple[Node, float]]
    ) -> Iterable[Tuple[Node, float]]: ...

    @staticmethod
    def prerequisites(pods: Iterable[Pod]) -> Iterable[Pod]:
        """Return all of the pods with status pending"""
        return filter(lambda p: p.status == Status.PENDING, pods)

    @staticmethod
    def filter(p: Pod, nodes: Iterable[Node]) -> Iterable[Node]:
        """Filter nodes that have enough remaining compute capacity for the pod's request."""
        return list(filter(lambda n: n.can_allocate(p.limit), nodes))

    def schedule(
        self, pods: Iterable[Pod], nodes: Iterable[Node]
    ) -> Result[Tuple[Pod, Node], None]:
        """Override to include resource allocation after scheduling."""
        pod = self.pick(pods)
        if pod is None:
            return Err(None)

        possible_nodes = self.filter(pod, nodes)

        if not possible_nodes:
            return Err(None)

        nodes_with_score = self.score(pod, possible_nodes)
        nodes_with_score = self.normalize(nodes_with_score)

        if not nodes_with_score:
            return Err(None)

        selected_node, score = max(nodes_with_score, key=lambda x: x[1])

        return Ok((pod, selected_node))
