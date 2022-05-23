# WompiSDK

Unofficial SDK for Wompi

Example of invocations and management of exceptions:

```
from wompi import init
from wompi.card import create_card_token, create_card_long_term_token, create_card_payment
from wompi.wallet import create_wallet_token, get_wallet_token_info, create_wallet_long_term_token, create_wallet_payment
from wompi.utils.tokenize import create_acceptance_token
from wompi.payments import get_payment, void_payment
from wompi.models.event import Event
from wompi.models.exception import WompiException

#Initializes SDK. Last param corresponds to environment==Sandbox
def do_init():
    init('<PUBLIC_KEY>', '<PRIVATE_KEY>', '<EVENTS_SECRET>', True)

#Creates a token with a credit card payment method
def test_token_create_card():
    result = create_card_token('4242424242424242', '767', '07', '29', 'Juan Felipe Ramos')
    #tok_test_17123_d6F2A55EC86BB86fA9616ed4495F8a8a
    print(result)

#Creates a token with a wallet payment method
def test_token_create_wallet():
    result = create_wallet_token('NEQUI', '3991111111')
    #nequi_test_zd6QnKW5k6M4fVyvTF82WNzqQC8tKMeu
    print(result)

#Creates a credit card payment source
def test_token_source_card():
    acceptance_token = create_acceptance_token()
    print(acceptance_token)
    result = create_card_long_term_token('pepinito@hotmail.com', 'tok_test_17123_d6F2A55EC86BB86fA9616ed4495F8a8a',
                                  acceptance_token['data']['presigned_acceptance']['acceptance_token'])
    #26495
    print(result)

#Creates a wallet payment source
def test_token_source_wallet():
    acceptance_token = create_acceptance_token()
    result = create_wallet_long_term_token('NEQUI', 'pepinito@hotmail.com', 'nequi_test_zd6QnKW5k6M4fVyvTF82WNzqQC8tKMeu',
                                  acceptance_token['data']['presigned_acceptance']['acceptance_token'])
    #26496
    print(result)

#Gets info from a token made with a wallet payment method
def test_get_token_wallet():
    result = get_wallet_token_info('NEQUI', 'nequi_test_zd6QnKW5k6M4fVyvTF82WNzqQC8tKMeu')
    #WalletToken(status=<TokenStatus.APPROVED: 'APPROVED'>, token='nequi_test_zd6QnKW5k6M4fVyvTF82WNzqQC8tKMeu', wallet_id='3991111111', name='NEQUI')
    print(result)

#Creates a transaction with a credit card token
def test_transaction_create_token_card():
    acceptance_token = create_acceptance_token()
    result = create_card_payment(
        amount_in_cents=3000000,
        customer_email='pepinito@hotmail.com',
        payment_token='tok_test_17123_d6F2A55EC86BB86fA9616ed4495F8a8a',
        acceptance_token=acceptance_token['data']['presigned_acceptance']['acceptance_token'],
        commerce_reference='PKO_TEST123318',
        customer_full_name='Juan Felipe Ramos',
        address_line_1='CL 75 # 110C 12',
        region='CUNDINAMARCA',
        city='BOGOTA',
        customer_phone_number='3991111111',
        installments=1,
    )
    #117123-1653268505-79024
    print(result)

#Creates a transaction with a wallet token
def test_transaction_create_token_wallet():
    acceptance_token = create_acceptance_token()
    result = create_wallet_payment(
        amount_in_cents=3000000,
        customer_email='pepinito@hotmail.com',
        payment_token='nequi_test_zd6QnKW5k6M4fVyvTF82WNzqQC8tKMeu',
        acceptance_token=acceptance_token['data']['presigned_acceptance']['acceptance_token'],
        commerce_reference='PKO_TEST12337',
        customer_full_name='Juan Felipe Ramos',
        address_line_1='CL 75 # 110C 12',
        region='CUNDINAMARCA',
        city='BOGOTA',
        customer_phone_number='3991111111',
        wallet_id='3991111111',
    )
    #117123-1653268662-46469
    print(result)

#Creates a transaction with a credit card payment source
def test_transaction_create_source_card():
    acceptance_token = create_acceptance_token()
    result = create_card_payment(
        amount_in_cents=3000000,
        customer_email='pepinito@hotmail.com',
        payment_token='26495',
        acceptance_token=acceptance_token['data']['presigned_acceptance']['acceptance_token'],
        commerce_reference='PKO_TEST123320',
        customer_full_name='Juan Felipe Ramo,s',
        address_line_1='CL 75 # 110C 12',
        region='CUNDINAMARCA',
        city='BOGOTA',
        customer_phone_number='3991111111',
        installments=2,
        saved_payment_method= True,
    )
    #117123-1653272574-10729
    print(result)

#Creates a transaction with a wallet payment source
def test_transaction_create_source_wallet():
    acceptance_token = create_acceptance_token()
    result = create_wallet_payment(
        amount_in_cents=3000000,
        customer_email='pepinito@hotmail.com',
        payment_token='26496',
        acceptance_token=acceptance_token['data']['presigned_acceptance']['acceptance_token'],
        commerce_reference='PKO_TEST12339',
        customer_full_name='Juan Felipe Ramos',
        address_line_1='CL 75 # 110C 12',
        region='CUNDINAMARCA',
        city='BOGOTA',
        customer_phone_number='3991111111',
        wallet_id='3991111111',
        saved_payment_method= True,
    )
    #117123-1653272683-79159
    print(result)

#Gets info from a transaction with a credit card token
def test_transaction_get_token_card():
    result = get_payment('117123-1653268505-79024')
    print(result)

#Gets info from a transaction with a wallet token
def test_transaction_get_token_wallet():
    result = get_payment('117123-1653268662-46469')
    print(result)

#Gets info from a transaction with a credit card payment source
def test_transaction_get_source_card():
    result = get_payment('117123-1653272574-10729')
    print(result)

#Gets info from a transaction with a wallet payment source
def test_transaction_get_source_wallet():
    result = get_payment('117123-1653272683-79159')
    print(result)

#Voids a transaction with a credit card token
def test_transaction_void_token_card():
    result = void_payment('117123-1653268505-79024')
    print(result)

#Voids a transaction with a wallet token (IMPOSSIBLE. Example of exception management)
def test_transaction_void_token_wallet():
    try:
        result = void_payment('117123-1653268662-46469')
        print(result)
    except WompiException as we:
        print(we.to_dict())

#Voids a transaction with a credit card payment source
def test_transaction_void_source_card():
    result = void_payment('117123-1653272574-10729')
    print(result)

#Voids a transaction with a wallet payment source (IMPOSSIBLE. Example of exception management)
def test_transaction_void_source_wallet():
    try:
        result = void_payment('117123-1653272683-79159')
        print(result)
    except WompiException as we:
        print(we.to_dict())


#Verifies signature of an incoming event
def verify_event():
    data = {
        "event": "http_event_received",
        "data": {
            "nequi_token": {
                "id": "nequi_test_SwsdbQLWpZLovYKv4EvxbSI7A1G8VPR3",
                "status": "APPROVED",
                "phone_number": "3991111111"
            }
        },
        "sent_at": "2022-05-22T03:19:06.756Z",
        "timestamp": 1653189546,
        "signature": {
            "checksum": "65a2a7fe05c2b042f34be5da588d23075c6260b871469545fc2022d24d71c26e",
            "properties": [
                "nequi_token.id",
                "nequi_token.status",
                "nequi_token.phone_number"
            ]
        },
        "environment": "test"
    }
    event = Event.from_dict(data)
    #True
    print(event.validate())
```
