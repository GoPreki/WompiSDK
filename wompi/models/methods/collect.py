from dataclasses import dataclass
from typing import Optional, Union
from wompi.models.methods import PaymentResponse, PaymentRequest
from wompi.utils import optional_dict


@dataclass
class Collect:
    business_agreement_code: Union[str, None]
    payment_intention_identifier: Union[str, None]

    def to_dict(self) -> dict:
        return optional_dict(
            business_agreement_code=self.business_agreement_code,
            payment_intention_identifier=self.payment_intention_identifier,
        )

    @staticmethod
    def from_dict(req: dict) -> 'Collect':
        return Collect(
            business_agreement_code=req.get('business_agreement_code'),
            payment_intention_identifier=req.get('payment_intention_identifier'),
        )


@dataclass
class CollectRequest(PaymentRequest):
    sandbox_status: Optional[str] = None

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(),
            sandbox_status=self.sandbox_status,
        )

    @staticmethod
    def from_dict(req: dict) -> 'CollectRequest':
        payment_info = PaymentRequest.from_dict(req)
        return CollectRequest(type=payment_info.type,
                              token=payment_info.token,
                              sandbox_status=req.get('sandbox_status'))


@dataclass
class CollectResponse(PaymentResponse):
    payment_info: Union[Collect, None]

    def to_dict(self) -> dict:
        return super().to_dict_info(info=self.payment_info.to_dict() if self.payment_info else None)

    @staticmethod
    def from_dict(res: dict) -> 'CollectResponse':
        payment = PaymentResponse.from_dict(res)
        return CollectResponse(
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
            payment_info=Collect.from_dict(res.get('payment_method', {}).get('extra', {})),
        )
