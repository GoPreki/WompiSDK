from typing import Optional, Union
from wompi.models.payment import Payment, PaymentWallet, PaymentCreditCard
from wompi.utils import optional_dict
from wompi.utils.requests import get, post

PAYMENTS_PATH = '/transactions'

CURRENCY = 'COP'


def create_payment(
    amount_in_cents: int,
    customer_email: str,
    acceptance_token: str,
    commerce_reference: str,
    customer_full_name: str,
    address_line_1: str,
    country: str,
    region: str,
    city: str,
    currency: str,
    customer_phone_number: str,
    payment_method: Union[PaymentCreditCard, PaymentWallet],
    saved_payment_method: bool = False,
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,
):
    if currency != CURRENCY:
        raise Exception('Selected currency not available')

    general_optional_params = optional_dict(redirect_url=redirect_url)

    shipping_optional_params = optional_dict(postal_code=postal_code,
                                             address_line_2=address_line_2)

    payment_source = {
        'payment_source_id': payment_method.token
    } if saved_payment_method else {}

    body = {
        'acceptance_token': acceptance_token,
        'amount_in_cents': amount_in_cents,
        'currency': currency,
        'customer_email': customer_email,
        'payment_method': payment_method.to_dict(),
        'reference': commerce_reference,
        'customer_data': {
            'phone_number': customer_phone_number,
            'full_name': customer_full_name,
        },
        'shipping_address': {
            'address_line_1': address_line_1,
            'country': country,
            'region': region,
            'city': city,
            'name': customer_full_name,
            'phone_number': customer_phone_number,
            **shipping_optional_params,
        },
        **payment_source,
        **general_optional_params,
    }

    return post(path=PAYMENTS_PATH, body=body, sensitive=saved_payment_method)


def get_payment(transaction_id: str) -> Payment:
    res = get(path='/transactions/{transaction_id}',
              path_params={'transaction_id': transaction_id})
    return Payment.from_dict(res)


def void_payment(transaction_id: str):
    return post(path='/transactions/{transaction_id}/void',
                path_params={'transaction_id': transaction_id})
