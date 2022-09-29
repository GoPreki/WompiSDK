from typing import List, Optional
from wompi.models.exception import WompiException
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.methods.wallet import WALLET_PROPERTY, WalletResponse, WalletRequest, WalletToken
from wompi.models.entities.taxes import Tax
from wompi.payments import create_payment
from wompi.typing.wallet import CreateWalletPayment, CreateWalletToken, GetWalletTokenInfo
from wompi.decorators.requests import request
from wompi.utils.tokenize import create_token, create_long_term_token, get_token_info


@request(CreateWalletToken, CreateWalletToken.Response, cls=WalletToken)
def create_wallet_token(
    type: str,
    wallet_id: str,
) -> dict:
    _check_method(type=type)

    body = {
        WALLET_PROPERTY.get(type, 'phone_number'): wallet_id,
    }

    return create_token(path='/nequi', info=body)


def create_wallet_long_term_token(type, customer_email, payment_token, acceptance_token):
    _check_method(type=type)

    return create_long_term_token(
        payment_type=type,
        acceptance_token=acceptance_token,
        payment_token=payment_token,
        customer_email=customer_email,
    )


@request(GetWalletTokenInfo, GetWalletTokenInfo.Response, cls=WalletToken)
def get_wallet_token_info(type: str, token: str) -> dict:
    _check_method(type=type)

    return get_token_info(
        path='nequi',
        token=token,
    )


@request(CreateWalletPayment, CreateWalletPayment.Response, cls=WalletResponse)
def create_wallet_payment(
    amount_in_cents: int,
    taxes: List[Tax],
    customer_email: str,
    acceptance_token: str,
    commerce_reference: str,
    customer_full_name: str,
    address_line_1: str,
    region: str,
    city: str,
    customer_phone_number: str,
    wallet_id: str,
    payment_token: Optional[str] = None,
    currency: str = 'COP',
    type: str = 'NEQUI',
    saved_payment_method: bool = False,
    country: str = 'CO',
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,
) -> dict:
    _check_method(type=type)

    return create_payment(
        amount_in_cents=amount_in_cents,
        taxes=taxes,
        customer_email=customer_email,
        acceptance_token=acceptance_token,
        commerce_reference=commerce_reference,
        customer_full_name=customer_full_name,
        address_line_1=address_line_1,
        country=country,
        region=region,
        city=city,
        customer_phone_number=customer_phone_number,
        saved_payment_method=saved_payment_method,
        redirect_url=redirect_url,
        address_line_2=address_line_2,
        postal_code=postal_code,
        currency=currency,
        payment_method=WalletRequest(
            type=AvailablePaymentMethod.NEQUI,
            token=payment_token,
            wallet_id=wallet_id,
        ),
    )


def _check_method(type: str):
    if type != AvailablePaymentMethod.NEQUI.value:
        raise WompiException.from_dict({
            'type': 'INPUT_VALIDATION_ERROR',
            'messages': {
                'reference': ['Wallet payment method not available']
            }
        })
