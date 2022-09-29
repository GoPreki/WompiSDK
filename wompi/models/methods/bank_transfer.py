from dataclasses import dataclass
from typing import Union
from wompi.models.methods import PaymentRequest, PaymentResponse
from wompi.utils import optional_dict


@dataclass
class BankTransfer:
    async_payment_url: Union[str, None]

    def to_dict(self) -> dict:
        return optional_dict(async_payment_url=self.async_payment_url)

    @staticmethod
    def from_dict(req: dict) -> 'BankTransfer':
        return BankTransfer(async_payment_url=req.get('async_payment_url'))


@dataclass
class BankTransferRequest(PaymentRequest):
    user_type: str
    user_legal_id_type: str
    user_legal_id: str
    financial_institution_code: str
    payment_description: str

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(),
            user_type=self.user_type,
            user_legal_id_type=self.user_legal_id_type,
            user_legal_id=self.user_legal_id,
            financial_institution_code=self.financial_institution_code,
            payment_description=self.payment_description,
        )

    @staticmethod
    def from_dict(req: dict) -> 'BankTransferRequest':
        payment_info = PaymentRequest.from_dict(req)
        return BankTransferRequest(
            type=payment_info.type,
            token=payment_info.token,
            financial_institution_code=req['financial_institution_code'],
            payment_description=req['payment_description'],
            user_legal_id=req['user_legal_id'],
            user_legal_id_type=req['user_legal_id_type'],
            user_type=req['user_type'],
        )


@dataclass
class BankTransferResponse(PaymentResponse):
    info: Union[BankTransfer, None]

    def to_dict(self) -> dict:
        return super().to_dict_info(info=self.info.to_dict() if self.info else None)

    @staticmethod
    def from_dict(res: dict) -> 'BankTransferResponse':
        payment = PaymentResponse.from_dict(res)
        return BankTransferResponse(
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
            info=BankTransfer.from_dict(res.get('payment_method', {}).get('extra', {})),
        )
