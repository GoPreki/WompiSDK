from typing import Optional
from wompi.models.payment import AvailablePaymentMethod, WalletPayment
from wompi.models.token import WalletToken
from wompi.models.wallet import WALLET_PROPERTY, PaymentWallet
from wompi.payments import create_payment
from wompi.utils.tokenize import create_token, create_long_term_token, get_token_info

def create_wallet_token(
    type: str, 
    wallet_id: str,
):
    if type != AvailablePaymentMethod.NEQUI.value:
        raise Exception('Wallet payment method not available')

    body = {
       WALLET_PROPERTY.get(type, 'phone_number'): wallet_id,
    }

    wallet_token = create_token(path='/nequi', info=body)

    return WalletToken.from_dict(wallet_token)

def create_wallet_long_term_token(type, customer_email, payment_token, acceptance_token):
    if type != AvailablePaymentMethod.NEQUI.value:
        raise Exception('Wallet payment method not available')
    return create_long_term_token(
        payment_type=type, 
        acceptance_token=acceptance_token,
        payment_token=payment_token,
        customer_email=customer_email,
    )

def get_wallet_token_info(type, token):

    if type != AvailablePaymentMethod.NEQUI.value:
        raise Exception('Wallet payment method not available')

    wallet_token = get_token_info(
        path='/nequi',
        token=token,
    )

    return WalletToken.from_dict(wallet_token)
    

def create_wallet_payment(
    amount_in_cents: int,
    customer_email: str,
    payment_token: str,
    acceptance_token: str,
    commerce_reference: str,
    customer_full_name: str,
    address_line_1: str,
    region: str,
    city: str,
    customer_phone_number: str,
    wallet_id: str,
    type: str = 'NEQUI',
    saved_payment_method: bool = False,
    country: str = 'CO',
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,

) -> WalletPayment:

    if type != AvailablePaymentMethod.NEQUI.value:
        raise Exception('Wallet payment method not available')

    wallet_payment_method = {
        'token': payment_token,
        WALLET_PROPERTY.get(type, 'phone_number'): wallet_id,
        'type': AvailablePaymentMethod.NEQUI.value
    }

    payment = create_payment(
        amount_in_cents=amount_in_cents,
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
        payment_method=PaymentWallet.from_dict(wallet_payment_method)
    )

    return WalletPayment.from_dict(payment)
