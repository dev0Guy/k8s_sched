from functools import partial
from typing import List

from simulator.common.pod import PodManageFields, Status
from simulator.common import Node, Pod
from simulator.schedulers.k8s.random import RandomScheduler
import pytest

UnAvailablePod = partial(Pod, _manage_fields=PodManageFields(status=Status.UN_AVAILABLE, length=0))
PendingPod = partial(Pod, _manage_fields=PodManageFields(status=Status.PENDING, length=0))
RunningPod = partial(Pod, _manage_fields=PodManageFields(status=Status.RUNNING, length=0))
CompletedPod = partial(Pod, _manage_fields=PodManageFields(status=Status.COMPLETED, length=0))

@pytest.fixture(scope="module")
def scheduler():
    return RandomScheduler()

@pytest.mark.parametrize(
    "pods, nodes",
    [
        ([PendingPod([[2, 2]])], [Node([1, 1])]),
        ([PendingPod([[3, 3]])], [Node([2.9, 2.9]), Node([1, 1])]),
        ([PendingPod([[3, 3]]), PendingPod([[1, 1]])], [Node([2.9, 2.9]), Node([1, 1])]),
    ],
)
def test_pod_with_more_resource_than_nodes(
    scheduler,
    pods: List[Pod],
    nodes: List[Node],
):
    assert scheduler.schedule(pods, nodes).is_err(), (
        "Can't allocate pod to nodes witless resource"
    )

@pytest.mark.parametrize(
    "pods, nodes",
    [
        ([UnAvailablePod([[1, 1]])], [Node([1, 1])]),
        ([RunningPod([[1, 1]])], [Node([1, 1])]),
        ([CompletedPod([[1, 1]])], [Node([1, 1])]),
    ],
)
def test_dont_schedule_none_pending_pod(
    scheduler,
    pods: List[Pod],
    nodes: List[Node],
):
    assert scheduler.schedule(pods=pods, nodes=nodes).is_err(), (
        "Can't schedule pod with status diffreant than Pedning"
    )

@pytest.mark.parametrize(
    "pods, nodes",
    [
        ([PendingPod([[1, 1]])], [Node([1, 1])]),
        ([PendingPod([[1, 1]]), PendingPod([0.5, 0.5])], [Node([1, 1])]),
        ([PendingPod([[1, 1]])], [Node([0.5, 1]), Node([1, 1])]),
    ],
)
def test_pod_less_than_nodes_with_correct_status(
    scheduler,
    pods: List[Pod],
    nodes: List[Node],
):
    scheduled = scheduler.schedule(pods=pods, nodes=nodes)
    assert scheduled.is_ok()
    scheduled = scheduled.unwrap()
    assert isinstance(scheduled, tuple)
    assert len(scheduled) == 2
    assert scheduled[0] == pods[0]