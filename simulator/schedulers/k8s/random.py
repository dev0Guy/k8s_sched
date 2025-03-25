from typing import Tuple, List

from simulator.common import ABCK8sScheduler, Pod, Node
import random

class RandomScheduler(ABCK8sScheduler):
    def normalize(self, nodes: List[Tuple[Node, float]]) -> List[Tuple[Node, float]]:
        return nodes

    def score(self, p: Pod, nodes: List[Node]) -> List[Tuple[Node, float]]:
        selected_node_idx = random.randint(0, len(nodes))
        return [
            (n, float(idx == selected_node_idx))
            for idx, n in enumerate(nodes)
        ]

