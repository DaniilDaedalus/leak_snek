"""The implementation of the leaky bucket algorithm."""
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
class LeakyBucketLimiter(RateLimiter[T_contra]):
    """A rate limiter implementing the leaky bucket algorithm.

    The leaky bucket algorithm views traffic as water entering a bucket with a hole.
    The bucket has a specific capacity, and water (or requests) can only flow into the bucket at a certain rate.
    Once the bucket is full, any further incoming water overflows and is discarded.
    The hole (or "leak") at the bottom lets the water out at a constant rate.

    This metaphorical bucket is used to control the rate at which requests are processed.
    If the bucket overflows, it indicates that too many requests are coming in too fast,
    and some of them need to be discarded or delayed.

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

        This method uses the leaky bucket algorithm to determine if a request
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

            leaked = int((now - rate.updated_at) / self.rate_limit.period.seconds * self.rate_limit.operations)

            new_operations = rate.operations + 1 - leaked

            if new_operations > self.rate_limit.operations:
                return True

            self.rate_storage.write(key=key, value=Rate(operations=max(new_operations, 0), updated_at=now))

            return False
