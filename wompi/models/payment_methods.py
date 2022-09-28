from enum import Enum


class AvailablePaymentMethod(Enum):
    CARD = 'CARD'
    NEQUI = 'NEQUI'
    PSE = 'PSE'


WALLET_PROPERTY = {
    AvailablePaymentMethod.NEQUI.value: 'phone_number'
}
