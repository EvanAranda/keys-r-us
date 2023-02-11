from abc import ABC, abstractmethod


class AbstractSpec(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def validate(self, seed): ...


class BipSpec(AbstractSpec):
    @property
    def name(self) -> str:
        return 'BIP-0032/0039'

    def validate(self, seed):
        pass


class SlipSpec(AbstractSpec):
    @property
    def name(self) -> str:
        return 'SLIP-0039'

    def validate(self, seed):
        pass