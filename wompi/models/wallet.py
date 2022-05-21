from enum import Enum
from dataclasses import dataclass
from wompi.models.payment import AvailablePaymentMethod, PaymentInfo
from wompi.utils import optional_dict


WALLET_PROPERTY = {
    AvailablePaymentMethod.NEQUI.value:'phone_number'
}


@dataclass
class PaymentWallet(PaymentInfo):
    wallet_id: str

    def to_dict(self) -> dict:

        return optional_dict(
            **super().to_dict(), 
            **{WALLET_PROPERTY[self.type.value]:self.wallet_id},
        )

    @staticmethod
    def from_dict(req: dict) -> 'PaymentWallet':
        payment_info = PaymentInfo.from_dict(req)
        return PaymentWallet(
            type=payment_info.type,
            token=payment_info.token,
            wallet_id=req[WALLET_PROPERTY[payment_info.type.value]],
        )


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