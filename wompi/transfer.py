from typing import List, Optional
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.methods.transfer import TransferRequest, TransferResponse
from wompi.typing.transfer import CreateTransferPayment
from wompi.utils import optional_dict
from wompi.models.entities.taxes import Tax
from wompi.payments import create_payment
from wompi.utils.decorators import polling, request


@polling(CreateTransferPayment.Response, until=['payment_info.async_payment_url'])
@request(CreateTransferPayment, CreateTransferPayment.Response, cls=TransferResponse)
def create_transfer_payment(
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
    currency: str = 'COP',
    country: str = 'CO',
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,
) -> dict:

    collect_payment_method = optional_dict(type=AvailablePaymentMethod.BANCOLOMBIA_TRANSFER.value,
                                           sandbox_status='APPROVED',
                                           user_type='PERSON',
                                           payment_description='.')

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
        redirect_url=redirect_url,
        address_line_2=address_line_2,
        postal_code=postal_code,
        currency=currency,
        payment_method=TransferRequest.from_dict(collect_payment_method),
    )
