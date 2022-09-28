from enum import Enum


class AvailablePaymentMethod(Enum):
    CARD = 'CARD'
    NEQUI = 'NEQUI'
    PSE = 'PSE'
    BANCOLOMBIA_COLLECT = 'BANCOLOMBIA_COLLECT'


WALLET_PROPERTY = {
    AvailablePaymentMethod.NEQUI.value: 'phone_number'
}
