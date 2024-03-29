from typing import List, Optional, Protocol
from wompi.models.entities.taxes import Tax
from wompi.models.methods.collect import CollectResponse
from wompi.models.utils import SandboxStatus


class CreateCollectPayment(Protocol):

    class Response(Protocol):

        def __call__(
            self,
            session_id: str,
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
        ) -> CollectResponse:
            ...

    def __call__(
        self,
        session_id: str,
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
