from wompi.utils.requests import Keys


def init(public_key, private_key, event_secret, test: bool):
    Keys.X_PUBLIC_KEY = public_key
    Keys.X_PRIV_KEY = private_key
    Keys.EVENT_SECRET = event_secret
    Keys.TEST = test
