from typing import List, Optional
from wompi.models.exception import WompiException
from wompi.models.payment import AvailablePaymentMethod, CardPayment, PaymentCreditCard
from wompi.models.taxes import Tax
from wompi.models.token import CardToken
from wompi.payments import create_payment
from wompi.utils.tokenize import create_token, create_long_term_token

CARDS_PATH = '/cards'


def create_card_token(
    card_number: str,
    cvc: str,
    exp_month: str,
    exp_year: str,
    card_holder: str,
):
    body = {
        'number': card_number,
        'cvc': cvc,
        'exp_month': exp_month,
        'exp_year': exp_year,
        'card_holder': card_holder,
    }

    credit_card_token = create_token(path=CARDS_PATH, info=body)

    if credit_card_token.get('error'):
        raise WompiException.from_dict(credit_card_token['error'])

    return CardToken.from_dict(credit_card_token)


def create_card_long_term_token(customer_email, payment_token,
                                acceptance_token):
    return create_long_term_token(
        payment_type=AvailablePaymentMethod.CARD.value,
        acceptance_token=acceptance_token,
        payment_token=payment_token,
        customer_email=customer_email,
    )


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
) -> CardPayment:

    card_payment_method = {
        'token': payment_token,
        'installments': installments,
        'type': AvailablePaymentMethod.CARD.value
    }

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
        saved_payment_method=saved_payment_method,
        redirect_url=redirect_url,
        address_line_2=address_line_2,
        postal_code=postal_code,
        currency=currency,
        payment_method=PaymentCreditCard.from_dict(card_payment_method))

    if payment.get('error'):
        raise WompiException.from_dict(payment['error'])

    return CardPayment.from_dict(payment['data'])
