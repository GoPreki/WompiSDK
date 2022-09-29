from typing import List, Optional
from wompi.models.methods.bank_transfer import BankTransferResponse, BankTransferRequest
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.entities.taxes import Tax
from wompi.payments import create_payment
from wompi.decorators.requests import polling, request
from wompi.decorators.errors import capture_error
from wompi.utils.requests import get
from wompi.typing.bank_transfer import CreateBankTransferPayment, ListAvailableTransferBanks


@capture_error(ListAvailableTransferBanks)
def list_available_transfer_banks():
    return get('/pse/financial_institutions')


@polling(CreateBankTransferPayment.Response, until=['info.async_payment_url'])
@request(CreateBankTransferPayment, CreateBankTransferPayment.Response, cls=BankTransferResponse)
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
        redirect_url=redirect_url,
        address_line_2=address_line_2,
        postal_code=postal_code,
        currency=currency,
        payment_method=BankTransferRequest(
            type=AvailablePaymentMethod.PSE,
            user_type=user_type,
            financial_institution_code=financial_institution_code,
            payment_description=payment_description,
            user_legal_id=user_legal_id,
            user_legal_id_type=user_legal_id_type,
        ),
    )
