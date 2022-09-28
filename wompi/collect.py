from time import sleep
from typing import List, Optional, cast
from wompi.models.payment import CollectPayment, PaymentCollect
from wompi.models.exception import WompiException
from wompi.models.payment_methods import AvailablePaymentMethod
from wompi.utils import optional_dict
from wompi.models.taxes import Tax
from wompi.payments import create_payment, get_payment


def _create_collect_payment(
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

    payment = create_payment(
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
        payment_method=PaymentCollect.from_dict(collect_payment_method),
    )

    if payment.get('error'):
        raise WompiException.from_dict(payment['error'])

    return payment['data']


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
) -> CollectPayment:
    res = _create_collect_payment(
        amount_in_cents=amount_in_cents,
        taxes=taxes,
        customer_email=customer_email,
        acceptance_token=acceptance_token,
        commerce_reference=commerce_reference,
        customer_full_name=customer_full_name,
        address_line_1=address_line_1,
        region=region,
        city=city,
        customer_phone_number=customer_phone_number,
        currency=currency,
        country=country,
        address_line_2=address_line_2,
        postal_code=postal_code,
        redirect_url=redirect_url,
    )

    transaction = CollectPayment.from_dict(res)
    while not transaction.business_agreement_code:
        sleep(1)
        payment = cast(CollectPayment, get_payment(res['id']))
        transaction.business_agreement_code = payment.business_agreement_code
        transaction.payment_intention_identifier = payment.payment_intention_identifier

    return transaction
