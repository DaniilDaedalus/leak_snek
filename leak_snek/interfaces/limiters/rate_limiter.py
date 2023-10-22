"""Module containing the base interface for rate limiting algorithms."""
from typing import Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class RateLimiter(Protocol[T_contra]):
    """Protocol for rate limiting algorithms.

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

    def limit_exceeded(self: Self, key: T_contra) -> bool:
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
