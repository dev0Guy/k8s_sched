from abc import abstractmethod
from typing import Protocol

class PluginProtocol(Protocol):

    @property
    @abstractmethod
    def name(self) -> str: ...
