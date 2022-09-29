from time import sleep
from functools import wraps
from typing import Any, Callable, List, Type, TypeVar, cast
from wompi.models.exception import WompiException
from wompi.models.methods import PaymentResponse
from wompi.models.utils import Dictionable
from wompi.payments import get_payment

A = TypeVar('A', bound=Callable[..., Any])
H = TypeVar('H', bound=Callable[..., dict])
T = TypeVar('T', bound=Dictionable)
T1 = TypeVar('T1', bound=Callable[..., Dictionable])
R = TypeVar('R', bound=PaymentResponse)
Q = TypeVar('Q', bound=Callable[..., PaymentResponse])


def polling(_: Type[Q], *, until: List[str], sleep_secs=1):
    def decorator(fun: Callable[..., R]):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            transaction = fun(*args, **kwargs)

            while not all(getattr(transaction, attr) for attr in until):
                sleep(sleep_secs)
                payment = get_payment(transaction.id)
                for attr in until:
                    setattr(transaction, attr, getattr(payment, attr))

            return transaction
        return wrapper
    return decorator


def _capture_error(res: dict):
    if res.get('error'):
        raise WompiException.from_dict(res['error'])

    return res['data']


def request(_: Type[H], __: Type[T1], *, cls: Type[T]) -> Callable[..., T1]:
    def decorator(fun: H) -> T1:
        @wraps(fun)
        def wrapper(*args, **kwargs):
            data = _capture_error(fun(*args, **kwargs))

            return cast(T, cls.from_dict(data))
        return cast(T1, wrapper)
    return decorator


def capture_error(_: Type[A]):
    def decorator(fun: A) -> A:
        @wraps(fun)
        def wrapper(*args, **kwargs):
            return _capture_error(fun(*args, **kwargs))

        return cast(A, wrapper)
    return decorator
