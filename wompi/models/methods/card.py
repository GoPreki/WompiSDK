from dataclasses import dataclass
from typing import Optional
from wompi.models.methods import PaymentRequest, PaymentResponse
from wompi.models.token import Token
from wompi.utils import optional_dict


@dataclass
class CreditCard:
    card_holder: Optional[str]
    expiration_month: Optional[str]
    expiration_year: Optional[str]
    last4: str
    id: Optional[str]
    brand: str
    bin: Optional[str]
    name: str
    created_at: Optional[str]
    expires_at: Optional[str]
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
        return CreditCard(card_holder=req.get('card_holder'),
                          expiration_month=req.get('exp_month'),
                          expiration_year=req.get('exp_year'),
                          last4=req['last_four'],
                          brand=req['brand'],
                          bin=req.get('bin'),
                          id=req.get('id'),
                          name=req['name'],
                          created_at=req.get('created_at'),
                          expires_at=req.get('expires_at'))


@dataclass
class CardToken(Token):
    data: CreditCard

    def to_dict(self) -> dict:
        return optional_dict(**super().to_dict(), data=self.data.to_dict() if self.data else None)

    @staticmethod
    def from_dict(res: dict) -> 'CardToken':
        token = Token.from_dict(res)
        return CardToken(status=token.status, data=CreditCard.from_dict(res['data']))


@dataclass
class CreditCardRequest(PaymentRequest):
    installments: int

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(),
            installments=self.installments,
        )

    @staticmethod
    def from_dict(req: dict) -> 'CreditCardRequest':
        payment_info = PaymentRequest.from_dict(req)
        return CreditCardRequest(
            token=payment_info.token,
            type=payment_info.type,
            installments=req.get('installments', 1),
        )


@dataclass
class CardResponse(PaymentResponse):
    payment_method: CreditCard
    installments: int

    def to_dict(self) -> dict:
        return super().to_dict_info(info=self.payment_method.to_dict())

    @staticmethod
    def from_dict(res: dict) -> 'CardResponse':
        payment = PaymentResponse.from_dict(res)
        payment_method_info = res['payment_method']
        return CardResponse(
            payment_method=CreditCard.from_dict(payment_method_info['extra']),
            installments=int(payment_method_info['installments']),
            shipping_address=payment.shipping_address,
            id=payment.id,
            created_at=payment.created_at,
            amount_in_cents=payment.amount_in_cents,
            status=payment.status,
            reference=payment.reference,
            customer_email=payment.customer_email,
            payment_method_type=payment.payment_method_type,
            redirect_url=payment.redirect_url,
            payment_link_id=payment.payment_link_id,
            currency=payment.currency,
            customer=payment.customer,
            status_message=payment.status_message,
        )
