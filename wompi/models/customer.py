from dataclasses import dataclass
from wompi.utils import optional_dict

@dataclass
class Customer:
    full_name: str
    phone_number: str #573109999999

    def to_dict(self) -> dict:
        return optional_dict(
            full_name=self.full_name,
            phone_number=self.phone_number,
        )

    @staticmethod
    def from_dict(res: dict) -> 'Customer':
        return Customer(
            full_name=res['full_name'],
            phone_number=res['phone_number'],
        )