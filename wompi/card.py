from typing import List, Optional
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.entities.taxes import Tax
from wompi.models.methods.card import CardResponse, CardToken, CreditCardRequest
from wompi.payments import create_payment
from wompi.typing.card import CreateCardPayment, CreateCardToken, VoidPayment
from wompi.decorators.errors import capture_error
from wompi.decorators.requests import request
from wompi.utils.requests import post
from wompi.utils.tokenize import create_token, create_long_term_token


@request(CreateCardPayment, CreateCardPayment.Response, cls=CardResponse)
def create_card_payment(
    amount_in_cents: int,
    taxes: List[Tax],
    customer_email: str,
    payment_token: str,
    acceptance_token: str,
    commerce_reference: str,
    customer_full_name: str,
    address_line_1: str,
    region: str,
    city: str,
    customer_phone_number: str,
    currency: str = 'COP',
    installments: int = 1,
    saved_payment_method: bool = False,
    country: str = 'CO',
    address_line_2: Optional[str] = None,
    postal_code: Optional[str] = None,
    redirect_url: Optional[str] = None,
) -> dict:
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
        payment_method=CreditCardRequest(
            type=AvailablePaymentMethod.CARD,
            installments=installments,
            token=payment_token,
        ),
    )


@request(CreateCardToken, CreateCardToken.Response, cls=CardToken, extract_data=False)
def create_card_token(
    card_number: str,
    cvc: str,
    exp_month: str,
    exp_year: str,
    card_holder: str,
) -> dict:
    body = {
        'number': card_number,
        'cvc': cvc,
        'exp_month': exp_month,
        'exp_year': exp_year,
        'card_holder': card_holder,
    }

    return create_token(path='/cards', info=body)


def create_card_long_term_token(customer_email, payment_token, acceptance_token) -> dict:
    return create_long_term_token(
        payment_type=AvailablePaymentMethod.CARD.value,
        acceptance_token=acceptance_token,
        payment_token=payment_token,
        customer_email=customer_email,
    )


@capture_error(VoidPayment, extract_data=False)
def void_payment(transaction_id: str):
    return post(path='/transactions/{transaction_id}/void',
                path_params={'transaction_id': transaction_id},
                sensitive=True)
