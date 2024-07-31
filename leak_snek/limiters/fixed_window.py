"""The implementation of the fixed window algorithm."""

import dataclasses
import time
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.limiters.rate_limiter import RateLimiter
from leak_snek.interfaces.mutexes.mutex import Mutex
from leak_snek.interfaces.storages.rate_store import RateStorage
from leak_snek.interfaces.values.rate import Rate
from leak_snek.interfaces.values.rate_limit import RateLimit

T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class FixedWindowLimiter(RateLimiter[T_contra]):
    """A rate limiter implementing the fixed window algorithm.

    The fixed window algorithm

    Attributes
    ----------
        rate_limit (RateLimit): The limit configuration detailing how many operations are allowed in a given period.
        rate_storage (RateStorage[T_contra]): Storage mechanism to keep track of rate values.
        key_mutex (Mutex[T_contra]): Mutex to ensure thread-safety for the limiter.

    Methods
    -------
        limit_exceeded: Checks if the rate limit is exceeded for a given key.

    """

    rate_limit: RateLimit
    rate_storage: RateStorage[T_contra]
    key_mutex: Mutex[T_contra]

    @override
    def limit_exceeded(self: Self, key: T_contra) -> bool:
        """Check if the rate limit is exceeded for a given key.

        This method uses the fixed window algorithm to determine if a request
        for the given key should be allowed or rejected.

        Args:
        ----
        key (T_contra): The key to check the rate limit for.

        Returns:
        -------
        bool: True if the rate limit is exceeded, otherwise False.

        """
        with self.key_mutex.lock(key):
            rate = self.rate_storage.read(key)

            now = time.monotonic()

            if now - rate.updated_at < self.rate_limit.period.seconds:
                rate.operations += 1
                self.rate_storage.write(key=key, value=rate)
                return rate.operations > self.rate_limit.operations

            self.rate_storage.write(key=key, value=Rate(operations=1, updated_at=now))
            return False
