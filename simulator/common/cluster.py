from typing import List

import numpy as np
from result import Ok, Err

from pod import Pod, Status
from node import Node
from scheduler import SchedulerProtocol
from dataclasses import dataclass, field

@dataclass
class Cluster:
    scheduler: SchedulerProtocol
    nodes: List[Node]
    pods: List[Pod]
    _tick: int = field(default=0)

    @property
    def tick(self) -> int:
        return self._tick

    def _shift_nodes_usage_by_one(self):
        for node in self.nodes:
            node.usage = np.roll(node.usage, -1, axis=1)

    def _inc_tick(self) -> None:
        def is_pod_completed(p: Pod) -> bool:
            p_run_time = self.tick - p.start_run_time
            return p_run_time == p.length

        def is_pod_just_change_status_to_running(p: Pod) -> bool:
            return p.arrival_time == self.tick

        new_pending_pods = [*filter(is_pod_just_change_status_to_running, self.pods)]
        new_completed_pods = [*filter(is_pod_completed, self.pods)]

        self._tick += 1

        self._shift_nodes_usage_by_one()

        for p in new_pending_pods:
            p.status = Status.RUNNING

        for p in new_completed_pods:
            p.completion_time = self.tick

    def is_complete(self) -> bool:
        n_completed_pods = len(filter(lambda n: n.status == Status.COMPLETED, self.nodes))
        n_pods = len(self.pods)
        return n_pods == n_completed_pods

    def run(self):
        while not self.is_complete():

            match self.scheduler.schedule(self.pods, self.nodes):
                case Err(_):
                    self._inc_tick()
                case Ok((p, n)):
                    p.status = Status.RUNNING
                    n.allocate(p)
