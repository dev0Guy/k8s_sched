import numpy as np
import numba as nb


@nb.experimental.jitclass([
    ('cpu', nb.float32),
    ('ram', nb.float32),
    ('disk', nb.float32),
    ('gpu', nb.float32),
])
class Resource:
    def __init__(self, cpu: nb.float32, ram: nb.float32, disk: nb.float32, gpu: nb.float32):
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.gpu = gpu


@nb.experimental.jitclass([
    ('cpu', nb.float32[:]),
    ('ram', nb.float32[:]),
    ('disk', nb.float32[:]),
    ('gpu', nb.float32[:]),
])
class ResourcesUsage:

    def __init__(self, cpu: nb.float32[:], ram: nb.float32[:], disk: nb.float32[:], gpu: nb.float32[:]) -> None:
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.gpu = gpu

    @staticmethod
    def zeros(time_limit: nb.uint64) -> 'ResourcesUsage':
        _shape = (time_limit,)
        return ResourcesUsage(np.zeros(_shape), np.zeros(_shape), np.zeros(_shape), np.zeros(_shape))

    @staticmethod
    def like(resources: Resource, time_limit: nb.uint64) -> 'ResourcesUsage':
        _shape = (time_limit,)
        cpu = np.full(_shape, fill_value=resources.cpu, dtype=np.float32)
        ram = np.full(_shape, fill_value=resources.ram, dtype=np.float32)
        disk = np.full(_shape, fill_value=resources.disk, dtype=np.float32)
        gpu = np.full(_shape, fill_value=resources.gpu, dtype=np.float32)
        return ResourcesUsage(
            cpu=cpu, ram=ram, disk=disk, gpu=gpu
        )
