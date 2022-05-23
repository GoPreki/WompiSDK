from dataclasses import dataclass
from typing import Optional
from wompi.utils import optional_dict

@dataclass
class CreditCard:
    card_holder: Optional[str]
    expiration_month: Optional[str]
    expiration_year: Optional[str]
    last4: str
    id: Optional[str]
    brand: str
    bin: Optional[str]
    name: str
    created_at: Optional[str]
    expires_at: Optional[str]
    type: str = 'CARD'

    def to_dict(self) -> dict:
        return optional_dict(
            card_holder=self.card_holder,
            exp_month=self.expiration_month,
            exp_year=self.expiration_year,
            last_four=self.last4,
            id=self.id,
            brand=self.brand,
            bin=self.bin,
            name=self.name,
            created_at=self.created_at,
            expires_at=self.expires_at,
            type=self.type,
        )

    @staticmethod
    def from_dict(req: dict) -> 'CreditCard':
        return CreditCard(
            card_holder=req.get('card_holder'),
            expiration_month=req.get('exp_month'),
            expiration_year=req.get('exp_year'),
            last4=req['last_four'],
            brand=req['brand'],
            bin=req.get('bin'),
            id=req.get('id'),
            name=req['name'],
            created_at=req.get('created_at'),
            expires_at=req.get('expires_at')
        )