from typing import List, Literal, Optional, Protocol

from wompi.models.entities.taxes import Tax
from wompi.models.methods.transfer import TransferResponse
from wompi.models.utils import SandboxStatus


class CreateTransferPayment(Protocol):

    class Response(Protocol):

        def __call__(
            self,
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
        ) -> TransferResponse:
            ...

    def __call__(
        self,
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
        ...
