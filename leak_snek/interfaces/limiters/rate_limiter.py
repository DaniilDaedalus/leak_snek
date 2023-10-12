"""Module containing the base interface for rate limiting algorithms."""
from typing import Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class RateLimiter(Protocol[T_contra]):
    """Interface for any kind of rate limiting algorithm."""

    def limit_exceeded(self: Self, key: T_contra) -> bool:
        """Check if the limit for the given key is exceeded."""
        raise NotImplementedError
