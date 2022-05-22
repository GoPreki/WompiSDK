from enum import Enum

class AvailablePaymentMethod(Enum):
    CARD='CARD'
    NEQUI='NEQUI'


WALLET_PROPERTY = {
    AvailablePaymentMethod.NEQUI.value:'phone_number'
}