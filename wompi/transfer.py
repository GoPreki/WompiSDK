from typing import List, Literal, Optional
from wompi.models.methods import AvailablePaymentMethod
from wompi.models.methods.transfer import TransferRequest, TransferResponse
from wompi.models.utils import SandboxStatus
from wompi.typing.transfer import CreateTransferPayment
from wompi.models.entities.taxes import Tax
from wompi.payments import create_payment
from wompi.decorators.requests import polling, request


@polling(CreateTransferPayment.Response, until=['payment_info.async_payment_url'])
@request(CreateTransferPayment, CreateTransferPayment.Response, cls=TransferResponse)
def create_transfer_payment(
    session_id: str,
    user_type: Literal['PERSON'],
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
    sandbox_status: SandboxStatus = None,
) -> dict:
    return create_payment(
        session_id=session_id,
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
        payment_method=TransferRequest(type=AvailablePaymentMethod.BANCOLOMBIA_TRANSFER,
                                       sandbox_status=sandbox_status,
                                       user_type=user_type,
                                       payment_description=commerce_reference),
    )
