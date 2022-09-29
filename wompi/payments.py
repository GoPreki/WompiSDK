from typing import Any, Optional, Union, List, cast
from wompi.models.exception import WompiException
from wompi.models.methods.bank_transfer import BankTransferResponse, BankTransferRequest
from wompi.models.methods.card import CardResponse, CreditCardRequest
from wompi.models.methods.collect import CollectResponse, CollectRequest
from wompi.models.methods.transfer import TransferRequest, TransferResponse
from wompi.models.methods.wallet import WalletRequest, WalletResponse
from wompi.models.methods import PaymentResponse
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.entities.taxes import Tax
from wompi.typing.utils import GetPayment
from wompi.utils import optional_dict
from wompi.decorators.errors import capture_error
from wompi.utils.requests import get, post

CURRENCY = 'COP'
PAYMENT_TYPE = {
    AvailablePaymentMethod.CARD.value: CardResponse,
    AvailablePaymentMethod.NEQUI.value: WalletResponse,
    AvailablePaymentMethod.PSE.value: BankTransferResponse,
    AvailablePaymentMethod.BANCOLOMBIA_COLLECT.value: CollectResponse,
    AvailablePaymentMethod.BANCOLOMBIA_TRANSFER.value: TransferResponse,
}


def create_payment(
    amount_in_cents: int,
    taxes: List[Tax],
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
    payment_method: Union[CreditCardRequest, WalletRequest, BankTransferRequest, CollectRequest, TransferRequest],
    saved_payment_method: bool = False,
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,
):
    if currency != CURRENCY:
        raise WompiException.from_dict({
            'type': 'INPUT_VALIDATION_ERROR',
            'messages': {
                'reference': ['Selected currency not available']
            }
        })

    general_optional_params = optional_dict(redirect_url=redirect_url)
    shipping_optional_params = optional_dict(postal_code=postal_code, address_line_2=address_line_2)
    payment_source = {'payment_source_id': cast(Any, payment_method).token} if saved_payment_method else {}

    body = {
        'acceptance_token': acceptance_token,
        'amount_in_cents': amount_in_cents,
        'currency': currency,
        'taxes': [tax.to_dict() for tax in taxes],
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

    return post(path='/transactions', body=body, sensitive=saved_payment_method)


@capture_error(GetPayment)
def _get_payment(transaction_id: str) -> dict:
    return get(path='/transactions/{transaction_id}', path_params={'transaction_id': transaction_id})


def get_payment(transaction_id: str) -> PaymentResponse:
    data = _get_payment(transaction_id=transaction_id)
    response_class = PAYMENT_TYPE[data['payment_method_type']]
    return response_class.from_dict(data)
