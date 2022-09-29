from typing import Any, Callable, TypeVar, cast
from functools import wraps
from wompi.models.exception import WompiException
from typing import Type

A = TypeVar('A', bound=Callable[..., Any])


def _capture_error(res: dict, extract_data: bool = True):
    if res.get('error'):
        raise WompiException.from_dict(res['error'])

    return res['data'] if extract_data else res


def capture_error(_: Type[A], extract_data: bool = True):

    def decorator(fun: A) -> A:

        @wraps(fun)
        def wrapper(*args, **kwargs):
            return _capture_error(fun(*args, **kwargs), extract_data=extract_data)

        return cast(A, wrapper)

    return decorator
