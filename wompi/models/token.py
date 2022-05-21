from enum import Enum
from dataclasses import dataclass
from wompi.models.card import CreditCard
from wompi.models.wallet import WALLET_PROPERTY
from wompi.utils import optional_dict

class PaymentSource(Enum):
    AVAILABLE = 'AVAILABLE'
    PENDING = 'PENDING'

class TokenStatus(Enum):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'

class Token:
    status:	TokenStatus
    def to_dict(self) -> dict:
        return optional_dict(
            status=self.status.value,
        )
    
    @staticmethod
    def from_dict(res:dict) -> 'Token':
        return Token(
            status=TokenStatus(res['status']),
        )

@dataclass
class CardToken(Token):
   
    data: CreditCard

    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(), 
            data=self.data.to_dict() if self.ticket else None
        )

    @staticmethod
    def from_dict(res: dict) -> 'CardToken':
        token = Token.from_dict(res)
        return CardToken(
            status=token.status,
            data=CreditCard.from_dict(res['data'])
        )

@dataclass
class WalletToken(Token):
    id: str
    wallet_id: str
    name: str
    def to_dict(self) -> dict:
        return optional_dict(
            **super().to_dict(), 
            id=self.id,
            **{WALLET_PROPERTY.get(self.name, 'phone_number'):self.wallet_id},
            name=self.name
        )

    @staticmethod
    def from_dict(res: dict) -> 'WalletToken':
        token = Token.from_dict(res)
        return WalletToken(
            id=res['id'],
            status=token.status,
            wallet_id=res[WALLET_PROPERTY.get(res['name'], 'phone_number')],
            name=res['name']
        )
