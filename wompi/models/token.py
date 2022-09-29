from enum import Enum
from dataclasses import dataclass
from wompi.models.utils import Dictionable
from wompi.utils import optional_dict


class PaymentSource(Enum):
    AVAILABLE = 'AVAILABLE'
    PENDING = 'PENDING'


class TokenStatus(Enum):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'


@dataclass
class Token(Dictionable):
    status:	TokenStatus

    def to_dict(self) -> dict:
        return optional_dict(
            status=self.status.value,
        )

    @staticmethod
    def from_dict(res: dict) -> 'Token':
        return Token(
            status=TokenStatus(res['status']),
        )
