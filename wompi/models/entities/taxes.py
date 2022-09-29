from enum import Enum
from dataclasses import dataclass


class TaxType(Enum):
    VAT = 'VAT'  # IVA
    CONSUMPTION = 'CONSUMPTION'  # Impuesto al Consumo


@dataclass
class Tax:
    type: TaxType
    amount_in_cents: float

    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'amount_in_cents': self.amount_in_cents,
        }
