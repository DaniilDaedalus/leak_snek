"""Rate limiting decorator module."""
from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from leak_snek.interfaces.limiters.rate_limiter import RateLimiter

T = TypeVar("T")
K = TypeVar("K")
P = ParamSpec("P")


def rate_limit(
    rate_limiter: RateLimiter[K],
    key: Callable[P, K],
    default: T,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorate the function, rate limiting it's execution using given rate limiter."""

    def decorator(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if rate_limiter.limit_exceeded(key(*args, **kwargs)):
                return default

            return function(*args, **kwargs)

        return wrapper

    return decorator
