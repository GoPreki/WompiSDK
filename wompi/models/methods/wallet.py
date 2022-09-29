from wompi.models.methods import PaymentResponse, PaymentRequest, AvailablePaymentMethod
from dataclasses import dataclass
from wompi.models.token import Token
from wompi.utils import optional_dict

WALLET_PROPERTY = {AvailablePaymentMethod.NEQUI.value: 'phone_number'}


@dataclass
class Wallet:
    type: AvailablePaymentMethod
    wallet_id: str

    def to_dict(self) -> dict:
        return optional_dict(
            type=self.type.value,
            **{WALLET_PROPERTY[self.type.value]: self.wallet_id},
        )

    @staticmethod
    def from_dict(req: dict) -> 'Wallet':
        return Wallet(
            type=AvailablePaymentMethod(req['type']),
            wallet_id=req[WALLET_PROPERTY[req['type']]],
        )


@dataclass
class WalletToken(Token):
    token: str
    wallet_id: str
    name: str

    def to_dict(self) -> dict:
        return optional_dict(**super().to_dict(),
                             token=self.token,
                             **{WALLET_PROPERTY.get(self.name, 'phone_number'): self.wallet_id},
                             name=self.name)

    @staticmethod
    def from_dict(res: dict) -> 'WalletToken':
        token = Token.from_dict(res)
        return WalletToken(
            token=res['id'],
            status=token.status,
            wallet_id=res[WALLET_PROPERTY.get(res.get('name', AvailablePaymentMethod.NEQUI.value), 'phone_number')],
            name=res.get('name', AvailablePaymentMethod.NEQUI.value),
        )


@dataclass
class WalletRequest(PaymentRequest):
    wallet_id: str

    def to_dict(self) -> dict:

        return optional_dict(
            **super().to_dict(),
            **{WALLET_PROPERTY[self.type.value]: self.wallet_id},
        )

    @staticmethod
    def from_dict(req: dict) -> 'WalletRequest':
        payment_info = PaymentRequest.from_dict(req)
        return WalletRequest(
            type=payment_info.type,
            token=payment_info.token,
            wallet_id=req[WALLET_PROPERTY[payment_info.type.value]],
        )


@dataclass
class WalletResponse(PaymentResponse):
    wallet_info: Wallet

    def to_dict(self) -> dict:
        return super().to_dict_info(info=self.wallet_info.to_dict())

    @staticmethod
    def from_dict(res: dict) -> 'WalletResponse':
        payment = PaymentResponse.from_dict(res)
        return WalletResponse(shipping_address=payment.shipping_address,
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
                              wallet_info=Wallet.from_dict(res['payment_method']))
