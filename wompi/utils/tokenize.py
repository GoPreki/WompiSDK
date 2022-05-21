from wompi.utils.requests import get, post

def get_token_info(path, token):
    return get(path='/tokens/{path}/{token_id}', path_params={'path': path, 'token_id': token})

def create_token(path, info):
    return post(path=f'/tokens{path}', body=info)


def create_long_term_token(payment_type, acceptance_token, payment_token, customer_email):
    info = {
        'type': payment_type,
        'token': payment_token,
        'acceptance_token': acceptance_token,
        'customer_email': customer_email,
    }
    return post(path='/payment_sources', body=info, sensitive=True)
