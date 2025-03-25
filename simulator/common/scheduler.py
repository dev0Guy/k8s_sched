from abc import ABC
from typing import Iterable, Optional, Protocol, Tuple

from result import Err, Ok, Result

from simulator.common.node import Node
from simulator.common.pod import Pod, Status


class SchedulerProtocol(Protocol):
    def schedule(
        self, pods: Iterable[Pod], nodes: Iterable[Node]
    ) -> Optional[Tuple[Pod, Node]]: ...


class ABCK8sScheduler(ABC):
    def pick(self, pods: Iterable[Pod]) -> Optional[Pod]: ...
    def filter(self, p: Pod, nodes: Iterable[Node]) -> Iterable[Node]: ...
    def score(self, p: Pod, nodes: Iterable[Node]) -> Iterable[Tuple[Node, float]]: ...

    def normalize(
        self, nodes: Iterable[Tuple[Node, float]]
    ) -> Iterable[Tuple[Node, float]]: ...

    @staticmethod
    def prerequisites(pods: Iterable[Pod]) -> Iterable[Pod]:
        return filter(lambda p: p.status == Status.PENDING, pods)

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
