"""Module containing async rate limiter interface."""
from typing import Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncRateLimiter(Protocol[T_contra]):
    """Async interface for any kind of rate limiting algorithm."""

    async def limit_exceeded(self: Self, key: T_contra) -> bool:
        """Check if the limit for the given key is exceeded."""
        raise NotImplementedError
