from dataclasses import dataclass
from enum import Enum
from typing import List, Any
from wompi.models.exception import WompiException
from wompi.utils import optional_dict
from wompi.utils.requests import Keys
import hashlib

class EventType(Enum):
    TRANSACTION_UPDATE = 'transaction.updated'
    NEQUI_TOKEN_UPDATE = 'nequi_token.updated'
    HTTP_EVENT_UPDATE = 'http_event_received'

@dataclass
class Signature:
    properties: List[str]
    checksum: str

    def to_dict(self) -> dict:
        return optional_dict(
            properties=[prop for prop in self.properties],
            checksum=self.checksum,
        )

    @staticmethod
    def from_dict(res: dict) -> 'Signature':
        return Signature(
            properties=res.get('properties', []),
            checksum=res.get('checksum'),
        )

@dataclass
class Event:
    event: EventType
    signature: Signature
    environment: str
    data: Any
    timestamp: int
    sent_at: str

    def validate(self) -> bool:
        concat_props = ''
        for prop in self.signature.properties:
            params = prop.split('.')
            info = self.data
            for param in params:
                info = info[param]
            concat_props += str(info)
        
        concat_props+=str(self.timestamp)
        if Keys.EVENT_SECRET is None:
            raise WompiException.from_dict({
                'type': 'INPUT_VALIDATION_ERROR',
                'messages': {
                    'reference': ['Keys were not correctly initialized']
                }
            })
           
        concat_props+=str(Keys.EVENT_SECRET)

        hashed_props = hashlib.sha256(concat_props.encode('utf-8')).hexdigest()
        
        return hashed_props == self.signature.checksum

    def to_dict(self) -> dict:
        return optional_dict(
            event=self.event.value,
            signature=self.signature.to_dict(),
            environment=self.environment,
            data=self.data,
            timestamp=self.timestamp,
            sent_at=self.sent_at,
        )

    @staticmethod
    def from_dict(res: dict) -> 'Event':
        return Event(
            event=EventType(res['event']),
            data=res.get('data'),
            environment=res['environment'],
            signature=Signature.from_dict(res['signature']),
            timestamp=res['timestamp'],
            sent_at=res['sent_at'],
        )
