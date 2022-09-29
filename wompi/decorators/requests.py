from time import sleep
from functools import wraps
from typing import Callable, List, Type, TypeVar, cast
from wompi.models.methods import PaymentResponse
from wompi.models.utils import Dictionable
from wompi.payments import get_payment
from wompi.decorators.errors import _capture_error

H = TypeVar('H', bound=Callable[..., dict])
T = TypeVar('T', bound=Dictionable)
T1 = TypeVar('T1', bound=Callable[..., Dictionable])
R = TypeVar('R', bound=PaymentResponse)
Q = TypeVar('Q', bound=Callable[..., PaymentResponse])


def _get_nested_attr(obj, attr_path: str):
    attrs = attr_path.split('.')
    current = obj
    for attr in attrs:
        current = getattr(current, attr, None)
    return current


def _set_nested_attr(obj, attr_path: str, value):
    attrs = attr_path.split('.')
    last_attr = attrs.pop()
    current = obj
    for attr in attrs:
        current = getattr(current, attr, None)
    if current:
        setattr(current, last_attr, value)
    return current


def polling(_: Type[Q], *, until: List[str], sleep_secs=1):

    def decorator(fun: Callable[..., R]):

        @wraps(fun)
        def wrapper(*args, **kwargs):
            transaction = fun(*args, **kwargs)

            while not all(_get_nested_attr(transaction, attr) for attr in until):
                sleep(sleep_secs)
                payment = get_payment(transaction.id)
                for attr in until:
                    _set_nested_attr(transaction, attr, _get_nested_attr(payment, attr))

            return transaction

        return wrapper

    return decorator


def request(_: Type[H], __: Type[T1], *, cls: Type[T], extract_data: bool = True) -> Callable[..., T1]:

    def decorator(fun: H) -> T1:

        @wraps(fun)
        def wrapper(*args, **kwargs):
            data = _capture_error(fun(*args, **kwargs), extract_data=extract_data)

            return cast(T, cls.from_dict(data))

        return cast(T1, wrapper)

    return decorator
