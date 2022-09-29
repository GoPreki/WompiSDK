from typing import List, Optional
from wompi.models.methods.collect import CollectResponse, CollectRequest
from wompi.models.methods import AvailablePaymentMethod
from wompi.typing.collect import CreateCollectPayment
from wompi.utils import optional_dict
from wompi.models.entities.taxes import Tax
from wompi.payments import create_payment
from wompi.utils.decorators import polling, request


@polling(CreateCollectPayment.Response, until=['business_agreement_code', 'payment_intention_identifier'])
@request(CreateCollectPayment, CreateCollectPayment.Response, cls=CollectResponse)
def create_collect_payment(
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

    collect_payment_method = optional_dict(type=AvailablePaymentMethod.BANCOLOMBIA_COLLECT.value,
                                           sandbox_status='APPROVED')

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
        payment_method=CollectRequest.from_dict(collect_payment_method),
    )
