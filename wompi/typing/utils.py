from typing import Protocol


class GetPayment(Protocol):

    def __call__(self, transaction_id: str) -> dict:
        ...
