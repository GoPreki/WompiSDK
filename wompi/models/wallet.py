from enum import Enum
from dataclasses import dataclass
from wompi.utils import optional_dict

class AvailablePaymentMethod(Enum):
    CARD='CARD'
    NEQUI='NEQUI'


WALLET_PROPERTY = {
    AvailablePaymentMethod.NEQUI.value:'phone_number'
}
@dataclass
class Wallet:
    type: AvailablePaymentMethod
    wallet_id: str

    def to_dict(self) -> dict:
        return optional_dict(
            type=self.type.value,
            **{WALLET_PROPERTY[self.type.value]:self.wallet_id},
        )

    @staticmethod
    def from_dict(req: dict) -> 'Wallet':
        return Wallet(
            type=AvailablePaymentMethod(req['type']),
            wallet_id=req[WALLET_PROPERTY[req['type']]],
        )