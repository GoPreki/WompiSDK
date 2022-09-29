from abc import ABC, abstractmethod


class Dictionable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def from_dict(res: dict) -> 'Dictionable':
        raise NotImplementedError()
