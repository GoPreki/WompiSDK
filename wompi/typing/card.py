from typing import List, Optional, Protocol

from wompi.models.entities.taxes import Tax
from wompi.models.methods.card import CardResponse, CardToken


class CreateCardPayment(Protocol):

    class Response(Protocol):

        def __call__(
            self,
            session_id: str,
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
        ) -> CardResponse:
            ...

    def __call__(
        self,
        session_id: str,
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
        ...


class CreateCardToken(Protocol):

    class Response(Protocol):

        def __call__(
            self,
            card_number: str,
            cvc: str,
            exp_month: str,
            exp_year: str,
            card_holder: str,
        ) -> CardToken:
            ...

    def __call__(
        self,
        card_number: str,
        cvc: str,
        exp_month: str,
        exp_year: str,
        card_holder: str,
    ) -> dict:
        ...


class VoidPayment(Protocol):

    def __call__(self, transaction_id: str) -> None:
        ...
