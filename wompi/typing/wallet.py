from typing import List, Optional, Protocol
from wompi.models.entities.taxes import Tax

from wompi.models.methods.wallet import WalletResponse, WalletToken


class CreateWalletToken(Protocol):

    class Response(Protocol):

        def __call__(
            self,
            type: str,
            wallet_id: str,
        ) -> WalletToken:
            ...

    def __call__(
        self,
        type: str,
        wallet_id: str,
    ) -> dict:
        ...


class GetWalletTokenInfo(Protocol):

    class Response(Protocol):

        def __call__(self, type: str, token: str) -> WalletToken:
            ...

    def __call__(self, type: str, token: str) -> dict:
        ...


class CreateWalletPayment(Protocol):

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
            wallet_id: str,
            payment_token: Optional[str] = None,
            currency: str = 'COP',
            type: str = 'NEQUI',
            saved_payment_method: bool = False,
            country: str = 'CO',
            address_line_2: Optional[str] = None,
            postal_code: Optional[str] = None,
            redirect_url: Optional[str] = None,
        ) -> WalletResponse:
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
        wallet_id: str,
        payment_token: Optional[str] = None,
        currency: str = 'COP',
        type: str = 'NEQUI',
        saved_payment_method: bool = False,
        country: str = 'CO',
        address_line_2: Optional[str] = None,
        postal_code: Optional[str] = None,
        redirect_url: Optional[str] = None,
    ) -> dict:
        ...
