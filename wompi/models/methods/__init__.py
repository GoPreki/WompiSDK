from enum import Enum
from typing import Optional, Union
from dataclasses import dataclass
from wompi.models.entities.customer import Customer
from wompi.models.entities.shipping import Shipping
from wompi.models.utils import Dictionable
from wompi.utils import optional_dict


class AvailablePaymentMethod(Enum):
    CARD = 'CARD'
    NEQUI = 'NEQUI'
    PSE = 'PSE'
    BANCOLOMBIA_COLLECT = 'BANCOLOMBIA_COLLECT'
    BANCOLOMBIA_TRANSFER = 'BANCOLOMBIA_TRANSFER'


class PaymentStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'
    VOIDED = 'VOIDED'
    ERROR = 'ERROR'


@dataclass
class PaymentRequest:
    type: AvailablePaymentMethod

    def to_dict(self) -> dict:
        return optional_dict(type=self.type.value)

    @staticmethod
    def from_dict(res: dict) -> 'PaymentRequest':
        return PaymentRequest(type=AvailablePaymentMethod(res['type']))


@dataclass
class PaymentResponse(Dictionable):
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
    def from_dict(res: dict) -> 'PaymentResponse':
        return PaymentResponse(
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

    def to_dict_info(self, info: Union[dict, None]) -> dict:
        return {**self.to_dict(), 'payment_method': info}
