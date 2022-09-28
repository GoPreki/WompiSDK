from time import sleep
from typing import List, Optional, cast
from wompi.models.exception import WompiException
from wompi.models.payment import BankTransferPayment, PaymentBankTransfer
from wompi.models.payment_methods import AvailablePaymentMethod
from wompi.models.taxes import Tax
from wompi.payments import create_payment, get_payment
from wompi.utils import optional_dict
from wompi.utils.requests import get


def list_available_transfer_banks():
    res = get('/pse/financial_institutions')

    if res.get('error'):
        raise WompiException.from_dict(res['error'])

    return res['data']


def _create_bank_transfer_payment(
    financial_institution_code: str,
    user_type: int,
    user_legal_id_type: str,
    user_legal_id: str,
    payment_description: str,
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

    bank_transfer_payment_method = optional_dict(type=AvailablePaymentMethod.PSE.value)
    bank_transfer_payment_method['financial_institution_code'] = financial_institution_code
    bank_transfer_payment_method['user_type'] = user_type
    bank_transfer_payment_method['user_legal_id_type'] = user_legal_id_type
    bank_transfer_payment_method['user_legal_id'] = user_legal_id
    bank_transfer_payment_method['payment_description'] = payment_description

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
        payment_method=PaymentBankTransfer.from_dict(bank_transfer_payment_method),
    )

    if payment.get('error'):
        raise WompiException.from_dict(payment['error'])

    return payment['data']


def create_bank_transfer_payment(
    financial_institution_code: str,
    user_type: int,
    user_legal_id_type: str,
    user_legal_id: str,
    payment_description: str,
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
) -> BankTransferPayment:
    res = _create_bank_transfer_payment(
        financial_institution_code=financial_institution_code,
        user_type=user_type,
        user_legal_id_type=user_legal_id_type,
        user_legal_id=user_legal_id,
        payment_description=payment_description,
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

    transaction = BankTransferPayment.from_dict(res)
    while not transaction.url:
        sleep(1)
        transaction.url = cast(BankTransferPayment, get_payment(res['id'])).url

    return transaction
