from typing import List, Optional, Protocol, TypedDict
from wompi.models.entities.taxes import Tax
from wompi.models.methods.bank_transfer import BankTransferResponse


class CreateBankTransferPayment(Protocol):

    class Response(Protocol):

        def __call__(self,
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
                     redirect_url: Optional[str] = None) -> BankTransferResponse:
            ...

    def __call__(self,
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
                 redirect_url: Optional[str] = None) -> dict:
        ...


class Bank(TypedDict):
    financial_institution_code: str
    financial_institution_name: str


class ListAvailableTransferBanks(Protocol):

    def __call__(self) -> List[Bank]:
        ...
