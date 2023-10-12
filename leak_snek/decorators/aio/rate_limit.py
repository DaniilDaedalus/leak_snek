"""Async rate limiting decorator module."""
from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from leak_snek.interfaces.limiters.aio.rate_limiter import AsyncRateLimiter

T = TypeVar("T")
K = TypeVar("K")
P = ParamSpec("P")


def async_rate_limit(
    rate_limiter: AsyncRateLimiter[K],
    key: Callable[P, K],
    default: T,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Decorate the function, rate limiting it's execution using given rate limiter."""

    def decorator(function: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(function)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if await rate_limiter.limit_exceeded(key(*args, **kwargs)):
                return default

            return await function(*args, **kwargs)

        return wrapper

    return decorator
