from typing import List, Tuple, Optional

from simulator.common import Pod, Node, ABCK8sScheduler


class ShortestJobFirstScheduler(ABCK8sScheduler):

    def pick(self, pods: List[Pod]) -> Optional[Pod]:

        pass

    def score(self, p: Pod, nodes: List[Node]) -> List[Tuple[Node, float]]:
        pass

    def normalize(self, nodes: List[Tuple[Node, float]]) -> List[Tuple[Node, float]]:
        pass

