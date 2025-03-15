from typing import Union
import numpy as np
import cython

Resources = cython.struct(
    cpu=cython.float, ram=cython.float, disk=cython.float, gpu=cython.float
)

@cython.cclass
class ResourcesUsage:
    cpu: cython.float[:]
    ram: cython.float[:]
    disk: cython.float[:]
    gpu: cython.float[:]

    def __init__(self, cpu: cython.float[:], ram: cython.float[:], disk: cython.float[:], gpu: cython.float[:]) -> None:
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.gpu = gpu
    
    @staticmethod
    def zeros(time_limit: cython.uint) -> 'ResourcesUsage':
        _shape = (time_limit,)
        return ResourcesUsage(np.zeros(_shape), np.zeros(_shape), np.zeros(_shape), np.zeros(_shape))

    @staticmethod
    def like(resources: Resources, time_limit: cython.uint) -> 'ResourcesUsage':
        _shape = (time_limit,)
        cpu = np.full(_shape, fill_value=resources.cpu)
        ram = np.full(_shape, fill_value=resources.ram)
        disk = np.full(_shape, fill_value=resources.disk)
        gpu = np.full(_shape, fill_value=resources.gpu)
        return ResourcesUsage(
            cpu=cpu, ram=ram, disk=disk, gpu=gpu
        )


    def __add__(self, other: Union['ResourcesUsage', float, int]) -> 'ResourcesUsage':
        if isinstance(other, self.__class__):
            return ResourcesUsage(
                cpu=self.cpu + other.cpu,
                ram=self.ram + other.ram,
                disk=self.disk + other.disk,
                gpu=self.gpu + other.gpu
            )
        if isinstance(other, (float, int)):
            return ResourcesUsage(
                cpu=self.cpu + other,
                ram=self.ram + other,
                disk=self.disk + other,
                gpu=self.gpu + other
            )
        return NotImplemented
        
    def __mul__(self, num: Union[float, int]) -> 'ResourcesUsage':
        if not isinstance(num, (float, int)):
            return NotImplemented
        return ResourcesUsage(
            cpu=self.cpu * num,
            ram=self.ram * num,
            disk=self.disk * num,
            gpu=self.gpu * num
        )
