import numpy as np
import numba as nb
import pytest
from hypothesis import given, settings, strategies as st
from hugsy_scheduler.k8s.resource import Resource, ResourcesUsage

# Hypothesis strategies
float32_strategy = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False).map(np.float32)
uint64_strategy = st.integers(min_value=1, max_value=1000).map(nb.uint64)
array_strategy = st.lists(float32_strategy, min_size=1, max_size=10).map(lambda x: np.array(x, dtype=np.float32))


@given(
    cpu=float32_strategy,
    ram=float32_strategy,
    disk=float32_strategy,
    gpu=float32_strategy
)
def test_resource_init(cpu, ram, disk, gpu):
    res = Resource(cpu=cpu, ram=ram, disk=disk, gpu=gpu)
    assert res.cpu == cpu
    assert res.ram == ram
    assert res.disk == disk
    assert res.gpu == gpu
    assert isinstance(res.cpu, float)
    assert isinstance(res.ram, float)
    assert isinstance(res.disk, float)
    assert isinstance(res.gpu, float)


# Test ResourcesUsage initialization with Hypothesis
@given(
    cpu_array=array_strategy,
    ram_array=array_strategy,
    disk_array=array_strategy,
    gpu_array=array_strategy
)
@settings(deadline=500)
def test_resources_usage_init(cpu_array, ram_array, disk_array, gpu_array):
    # Ensure all arrays have the same length for valid initialization
    min_length = min(len(cpu_array), len(ram_array), len(disk_array), len(gpu_array))
    cpu_array = cpu_array[:min_length]
    ram_array = ram_array[:min_length]
    disk_array = disk_array[:min_length]
    gpu_array = gpu_array[:min_length]

    usage = ResourcesUsage(cpu=cpu_array, ram=ram_array, disk=disk_array, gpu=gpu_array)

    np.testing.assert_array_equal(usage.cpu, cpu_array)
    np.testing.assert_array_equal(usage.ram, ram_array)
    np.testing.assert_array_equal(usage.disk, disk_array)
    np.testing.assert_array_equal(usage.gpu, gpu_array)
    assert usage.cpu.dtype == np.float32
    assert usage.ram.dtype == np.float32
    assert usage.disk.dtype == np.float32
    assert usage.gpu.dtype == np.float32