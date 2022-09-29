from dataclasses import dataclass
from typing import Optional, Union
from wompi.models.methods import PaymentResponse, PaymentRequest
from wompi.utils import optional_dict


@dataclass
class Transfer:
    async_payment_url: Union[str, None]

    def to_dict(self) -> dict:
        return optional_dict(async_payment_url=self.async_payment_url,)

    @staticmethod
    def from_dict(req: dict) -> 'Transfer':
        return Transfer(async_payment_url=req.get('async_payment_url'),)


@dataclass
class TransferRequest(PaymentRequest):
    user_type: str
    payment_description: str
    sandbox_status: Optional[str] = None

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(),
            sandbox_status=self.sandbox_status,
            user_type=self.user_type,
            payment_description=self.payment_description,
        )

    @staticmethod
    def from_dict(req: dict) -> 'TransferRequest':
        payment_info = PaymentRequest.from_dict(req)
        return TransferRequest(type=payment_info.type,
                               token=payment_info.token,
                               sandbox_status=req.get('sandbox_status'),
                               user_type=req['user_type'],
                               payment_description=req['payment_description'])


@dataclass
class TransferResponse(PaymentResponse):
    payment_info: Union[Transfer, None]

    def to_dict(self) -> dict:
        return super().to_dict_info(info=self.payment_info.to_dict() if self.payment_info else None)

    @staticmethod
    def from_dict(res: dict) -> 'TransferResponse':
        payment = PaymentResponse.from_dict(res)
        return TransferResponse(
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
            payment_info=Transfer.from_dict(res.get('payment_method', {}).get('extra', {})),
        )
