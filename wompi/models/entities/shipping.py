from typing import Optional
from dataclasses import dataclass
from wompi.utils import optional_dict


@dataclass
class Shipping:
    address_line_1:	str
    address_line_2:	Optional[str]
    country: str  # CO
    state: str
    city: str
    name: Optional[str]
    phone_number: str  # 573109999999
    postal_code: Optional[str]

    def to_dict(self) -> dict:
        return optional_dict(
            address_line_1=self.address_line_1,
            address_line_2=self.address_line_2,
            country=self.country,
            region=self.state,
            city=self.city,
            name=self.name,
            phone_number=self.phone_number,
            postal_code=self.postal_code
        )

    @staticmethod
    def from_dict(res: dict) -> 'Shipping':
        return Shipping(
            address_line_1=res['address_line_1'],
            address_line_2=res.get('address_line_2'),
            country=res['country'],
            state=res['region'],
            city=res['city'],
            name=res.get('name'),
            phone_number=res['phone_number'],
            postal_code=res.get('postal_code')
        )
