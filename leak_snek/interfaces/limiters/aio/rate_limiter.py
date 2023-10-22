"""Module containing async rate limiter interface."""
from typing import Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncRateLimiter(Protocol[T_contra]):
    """Async protocol for rate limiting algorithms.

    This interface should be implemented by classes that aim to provide
    rate limiting capabilities based on various algorithms or strategies.
    The main focus is to determine whether a certain "key" has exceeded
    its limit or not.

    Type Params
    -----------
    T_contra: A contravariant type variable which denotes the type of
                key for rate limiting checks.

    Methods
    -------
    limit_exceeded: Should be implemented by concrete classes to check
                      if the rate limit for a given key is exceeded.

    """

    async def limit_exceeded(self: Self, key: T_contra) -> bool:
        """Determine if the rate limit for a specific key has been exceeded.

        Concrete implementations should provide logic to determine
        if a rate limit corresponding to the provided key is exceeded or not.

        Args:
        ----
        key (T_contra): The key (identifier) for which the rate limit
                          check needs to be performed.

        Returns:
        -------
        - bool: True if the limit for the given key is exceeded, False otherwise.
        """
        raise NotImplementedError
