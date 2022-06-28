import requests
from urllib.parse import quote
from wompi.models.exception import WompiException


class Keys:
    X_PUBLIC_KEY = None
    X_PRIV_KEY = None
    EVENT_SECRET = None
    TEST: bool = True


def get_base_url():
    _prefix = 'production' if not Keys.TEST else 'sandbox'
    return f'https://{_prefix}.wompi.co/v1'


def form_headers(sensitive) -> dict:
    if not (Keys.X_PUBLIC_KEY or sensitive) or (sensitive and not Keys.X_PRIV_KEY):
        raise WompiException.from_dict({
            'type': 'INPUT_VALIDATION_ERROR',
            'messages': {
                'reference': ['Keys were not correctly initialized']
            }
        })

    auth_key = Keys.X_PRIV_KEY if sensitive else Keys.X_PUBLIC_KEY

    return {
        'Content-Type': 'application/json',
        'User-Agent': 'Preki API',
        'Authorization': f'Bearer {auth_key}',
    }


def post(path='', path_params={}, body=None, sensitive=False):
    for key, value in path_params.items():
        value = quote(value)
        path = path.replace(f'/{{{key}}}', f'/{value}')
    req = requests.post(url=f'{get_base_url()}{path}', json=body, headers=form_headers(sensitive))
    res = req.json()
    return res


def get(path='', path_params={}, query_params={}, sensitive=False):
    for key, value in path_params.items():
        value = quote(value)
        path = path.replace(f'/{{{key}}}', f'/{value}')

    req = requests.get(url=f'{get_base_url()}{path}', headers=form_headers(sensitive), params=query_params)
    res = req.json()
    return res
