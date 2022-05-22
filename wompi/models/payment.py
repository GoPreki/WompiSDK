from enum import Enum
from dataclasses import dataclass
from typing import Optional, Union
from wompi.models.payment_methods import AvailablePaymentMethod, WALLET_PROPERTY
from wompi.models.card import CreditCard
from wompi.models.shipping import Shipping
from wompi.models.wallet import Wallet
from wompi.utils import optional_dict

class PaymentStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'
    VOIDED = 'VOIDED'
    ERROR = 'ERROR'

@dataclass
class PaymentInfo:
    token: str
    type: AvailablePaymentMethod
    def to_dict(self) -> dict:
        return optional_dict(
            token=self.token,
            type=self.type.value,
        )

    @staticmethod
    def from_dict(res: dict) -> 'PaymentInfo':
        return PaymentInfo(
            type=AvailablePaymentMethod(res['type']),
            token=res['token'],
        )

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
class Payment:
    shipping_address: Shipping
    id: str
    created_at: str
    amount_in_cents: int
    status: PaymentStatus
    reference: str
    customer_email: str
    payment_method_type: AvailablePaymentMethod
    redirect_url: Optional[str]
    payment_link_id: Optional[str]
    currency: str

    def to_dict(self) -> dict:
        return optional_dict(
            id=self.id,
            created_at=self.created_at,
            amount_in_cents=self.amount_in_cents,
            status=self.status.value,
            reference=self.reference,
            customer_email=self.customer_email,
            payment_method_type=self.payment_method_type.value,
            redirect_url=self.redirect_url,
            payment_link_id=self.payment_link_id,
            currency=self.currency
        )

    @staticmethod
    def from_dict(res: dict) -> 'Payment':
        return Payment(
            id=res['id'],
            created_at=res['created_at'],
            amount_in_cents=res['amount_in_cents'],
            status=PaymentStatus(res['status']),
            reference=res['reference'],
            customer_email=res['customer_email'],
            payment_method_type=AvailablePaymentMethod(res['payment_method_type']),
            redirect_url=res.get('redirect_url'),
            payment_link_id=res.get('payment_link_id'),
            currency=res['currency']
        )


@dataclass
class CardPayment(Payment):
    payment_method: Union[CreditCard, PaymentCreditCard]

    def to_dict(self) -> dict:
        return {**super().to_dict(), 'payment_method': self.payment_method.to_dict()}

    @staticmethod
    def from_dict(res: dict) -> 'CardPayment':
        payment = Payment.from_dict(res)
        return CardPayment(
            payment_method=CreditCard.from_dict(res['payment_method']) if res.get('payment_source_id') else PaymentCreditCard.from_dict(res['payment_method']),
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
        )

@dataclass
class WalletPayment(Payment):
    wallet_info: Wallet

    def to_dict(self) -> dict:
        return {**super().to_dict(), 'payment_method': self.wallet_info.to_dict()}

    @staticmethod
    def from_dict(res: dict) -> 'WalletPayment':
        payment = Payment.from_dict(res)
        return WalletPayment(
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
            wallet_info=Wallet.from_dict(res['payment_method'])
        )