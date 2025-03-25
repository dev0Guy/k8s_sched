from typing import Iterable, Optional, Tuple

import numpy as np

from simulator.common import ABCK8sScheduler
from simulator.common.node import Node
from simulator.common.pod import Pod


class FIFOScheduler(ABCK8sScheduler):
    def pick(self, pods: Iterable[Pod]) -> Optional[Pod]:
        """Pick the first pod from the iterable (FCFS)."""
        try:
            return next(self.prerequisites(pods))
        except StopIteration:
            return None

    def score(self, p: Pod, nodes: Iterable[Node]) -> Iterable[Tuple[Node, float]]:
        """Assign a simple score based on remaining capacity (higher is better)."""
        return [(node, float(np.sum(node.free_compute - p.limit))) for node in nodes]

    def normalize(
        self, nodes: Iterable[Tuple[Node, float]]
    ) -> Iterable[Tuple[Node, float]]:
        """Normalize scores to a 0-1 range using NumPy, compact version."""
        nodes_list = list(nodes)
        if not nodes_list:
            return []

        nodes_array, scores = zip(*nodes_list)
        scores = np.array(scores)
        score_range = scores.max() - scores.min()
        normalized = (
            (scores - scores.min()) / score_range
            if score_range
            else np.ones_like(scores)
        )

        return [(node, float(score)) for node, score in zip(nodes_array, normalized)]
