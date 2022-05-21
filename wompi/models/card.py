from dataclasses import dataclass
from wompi.models.payment import PaymentInfo
from wompi.utils import optional_dict


@dataclass
class PaymentCreditCard(PaymentInfo):

    installments: int

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(),
            installments=self.installments,
        )

    @staticmethod
    def from_dict(req: dict) -> 'PaymentCreditCard':
        payment_info = PaymentInfo.from_dict(req)
        return PaymentCreditCard(
            token=payment_info.token,
            type=payment_info.type, 
            installments=req.get('installments', 1),
        )


@dataclass
class CreditCard:
    card_holder: str
    expiration_month: str
    expiration_year: str
    last4: str
    id: str
    brand: str
    bin: str
    name: str
    created_at: str
    expires_at: str
    type: str = 'CARD'

    def to_dict(self) -> dict:
        return optional_dict(
            card_holder=self.card_holder,
            exp_month=self.expiration_month,
            exp_year=self.expiration_year,
            last_four=self.last4,
            id=self.id,
            brand=self.brand,
            bin=self.bin,
            name=self.name,
            created_at=self.created_at,
            expires_at=self.expires_at,
            type=self.type,
        )

    @staticmethod
    def from_dict(req: dict) -> 'CreditCard':
        return CreditCard(
            card_holder=req['card_holder'],
            expiration_month=req['exp_month'],
            expiration_year=req['exp_year'],
            last4=req['last_four'],
            brand=req['brand'],
            bin=req['bin'],
            id=req['id'],
            name=req['name'],
            created_at=req['created_at']
        )