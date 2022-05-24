from enum import Enum
from dataclasses import dataclass
from gettext import install
from typing import Optional, Union
from wompi.models.customer import Customer
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
    token: Optional[str]
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
            token=res.get('token'),
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
    shipping_address: Optional[Shipping]
    customer: Optional[Customer]
    id: str
    created_at: str
    amount_in_cents: int
    status: PaymentStatus
    reference: str
    customer_email: Optional[str]
    payment_method_type: AvailablePaymentMethod
    redirect_url: Optional[str]
    payment_link_id: Optional[str]
    currency: str
    status_message: Optional[str]

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
            currency=self.currency,
            shipping_address=self.shipping_address.to_dict() if self.shipping_address else None,
            customer=self.customer.to_dict() if self.customer else None,
            status_message=self.status_message,
        )

    @staticmethod
    def from_dict(res: dict) -> 'Payment':
        return Payment(
            id=res['id'],
            created_at=res['created_at'],
            amount_in_cents=res['amount_in_cents'],
            status=PaymentStatus(res['status']),
            reference=res['reference'],
            customer_email=res.get('customer_email'),
            payment_method_type=AvailablePaymentMethod(res['payment_method_type']),
            redirect_url=res.get('redirect_url'),
            payment_link_id=res.get('payment_link_id'),
            currency=res['currency'],
            shipping_address=Shipping.from_dict(res['shipping_address']) if res.get('shipping_address') else None,
            customer=Customer.from_dict(res['customer_data']) if res.get('customer_data') else None,
            status_message=res.get('status_message'),
        )


@dataclass
class CardPayment(Payment):
    payment_method: CreditCard
    installments: int

    def to_dict(self) -> dict:
        return {**super().to_dict(), 'payment_method': self.payment_method.to_dict()}

    @staticmethod
    def from_dict(res: dict) -> 'CardPayment':
        payment = Payment.from_dict(res)
        payment_method_info = res['payment_method']
        return CardPayment(
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
            customer=payment.customer,
            status_message=payment.status_message,
            wallet_info=Wallet.from_dict(res['payment_method'])
        )