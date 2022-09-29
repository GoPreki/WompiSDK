from abc import ABC, abstractmethod
from typing import Literal, Optional, Union


class Dictionable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def from_dict(res: dict) -> 'Dictionable':
        raise NotImplementedError()


SandboxStatus = Optional[Union[Literal['APPROVED'], Literal['DECLINED'], Literal['ERROR']]]
