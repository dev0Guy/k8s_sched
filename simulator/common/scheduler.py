from abc import ABC,  abstractmethod
from typing import Optional, Protocol, Tuple, List

from result import Err, Ok, Result

from simulator.common.node import Node
from simulator.common.pod import Pod, Status

class SchedulerProtocol(Protocol):
    def schedule(
        self, pods: List[Pod], nodes: List[Node]
    ) -> Optional[Tuple[Pod, Node]]: ...


class ABCK8sScheduler(ABC):
    @abstractmethod
    def score(self, p: Pod, nodes: List[Node]) -> List[Tuple[Node, float]]: ...

    @abstractmethod
    def normalize(
        self, nodes: List[Tuple[Node, float]]
    ) -> List[Tuple[Node, float]]: ...

    @staticmethod
    def prerequisites(pods: List[Pod]) -> List[Pod]:
        """Return all of the pods with status pending"""
        return filter(lambda p: p.status == Status.PENDING, pods)

    @staticmethod
    def filter(p: Pod, nodes: List[Node]) -> List[Node]:
        """Filter nodes that have enough remaining compute capacity for the pod's request."""
        return list(filter(lambda n: n.can_allocate(p), nodes))

    def pick(self, pods: List[Pod]) -> Optional[Pod]:
        """Pick the first pod from the iterable (FCFS)."""
        try:
            return next(self.prerequisites(pods))
        except StopIteration:
            return None

    def schedule(
        self, pods: List[Pod], nodes: List[Node]
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
