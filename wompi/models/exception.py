from dataclasses import dataclass
from email import message
from enum import Enum
from typing import List, Optional
from wompi.utils import optional_dict


class WompiExceptionType(Enum):
    INVALID_ACCESS_TOKEN = 'INVALID_ACCESS_TOKEN'
    INPUT_VALIDATION_ERROR = 'INPUT_VALIDATION_ERROR'
    UNPROCESSABLE = 'UNPROCESSABLE'

@dataclass
class WompiException(Exception):
    type: WompiExceptionType
    reason: Optional[str]
    messages: Optional[List[str]]

    def to_dict(self) -> dict:
        return optional_dict(
            type=self.type.value,
            messages=self.messages,
            reason=self.reason,
        )

    @staticmethod
    def from_dict(res: dict) -> 'WompiException':
        return WompiException(
            type=WompiExceptionType(res['type']),
            messages=[msg for list_msg in res['messages'].values() for msg in list_msg] if res.get('messages') else None,
            reason=res.get('reason')
        )