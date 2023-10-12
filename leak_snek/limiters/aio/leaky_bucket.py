"""Async implementation of the leaky bucket algorithm."""
import dataclasses
import time
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.limiters.aio.rate_limiter import AsyncRateLimiter
from leak_snek.interfaces.storages.aio.rate_store import AsyncRateStorage
from leak_snek.interfaces.storages.rate import Rate
from leak_snek.interfaces.values.rate_limit import RateLimit

T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class AsyncLeakyBucketLimiter(AsyncRateLimiter[T_contra]):
    """Async leaky bucket rate limiting algorithm.

    Manages incoming requests using a 'bucket' with capacity and leak rate.
    Requests are added if space is available, otherwise, they're discarded or delayed.
    The bucket gradually empties to maintain a controlled output rate, preventing congestion and DDoS attacks.
    """

    rate_limit: RateLimit
    rate_storage: AsyncRateStorage[T_contra]

    @override
    async def limit_exceeded(self: Self, key: T_contra) -> bool:
        rate = await self.rate_storage.read(key)

        now = time.monotonic()

        leaked = int((now - rate.updated_at) / self.rate_limit.period.seconds * self.rate_limit.operations)

        new_operations = rate.operations + 1 - leaked

        if new_operations > self.rate_limit.operations:
            return True

        await self.rate_storage.write(key=key, value=Rate(operations=max(new_operations, 0), updated_at=now))

        return False
