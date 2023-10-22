"""Async implementation of the leaky bucket algorithm."""
import dataclasses
import time
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.limiters.aio.rate_limiter import AsyncRateLimiter
from leak_snek.interfaces.mutexes.aio.mutex import AsyncMutex
from leak_snek.interfaces.storages.aio.rate_store import AsyncRateStorage
from leak_snek.interfaces.values.rate import Rate
from leak_snek.interfaces.values.rate_limit import RateLimit

T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class AsyncLeakyBucketLimiter(AsyncRateLimiter[T_contra]):
    """Asynchronous rate limiter implementing the leaky bucket algorithm.

    The leaky bucket algorithm metaphorically visualizes traffic as water entering a bucket with a hole.
    The bucket has a specific capacity, and requests (water) can flow into the bucket at a predetermined rate.
    Once the bucket reaches its capacity, any further incoming requests overflow and are discarded.
    The hole (or "leak") at the bottom allows requests to flow out at a constant rate.

    This limiter is asynchronous, making it suitable for event-driven applications
    or environments where concurrency is important.
    If the bucket overflows, it indicates that too many requests are arriving too quickly,
    leading to the rejection or delay of some requests.

    Attributes
    ----------
        rate_limit (RateLimit): The configuration specifying how many operations are allowed within a given period.
        rate_storage (AsyncRateStorage[T_contra]): Asynchronous storage mechanism to monitor rate values.
        key_mutex (AsyncMutex[T_contra]): Asynchronous mutex to ensure thread-safety for the limiter.

    Methods
    -------
        limit_exceeded: Asynchronously checks if the rate limit is exceeded for a specific key.
    """

    rate_limit: RateLimit
    rate_storage: AsyncRateStorage[T_contra]
    key_mutex: AsyncMutex[T_contra]

    @override
    async def limit_exceeded(self: Self, key: T_contra) -> bool:
        """Asynchronously checks if the rate limit is exceeded for a given key.

        Using the leaky bucket algorithm, this method determines whether a request
        associated with the given key should be permitted or declined.

        Args:
        ----
        key (T_contra): The key for which the rate limit is checked.

        Returns:
        -------
        bool: True if the rate limit is surpassed, otherwise False.
        """
        async with self.key_mutex.lock(key):
            rate = await self.rate_storage.read(key)

            now = time.monotonic()

            leaked = int((now - rate.updated_at) / self.rate_limit.period.seconds * self.rate_limit.operations)

            new_operations = rate.operations + 1 - leaked

            if new_operations > self.rate_limit.operations:
                return True

            await self.rate_storage.write(key=key, value=Rate(operations=max(new_operations, 0), updated_at=now))

            return False
