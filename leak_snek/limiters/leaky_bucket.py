"""The implementation of the leaky bucket algorithm."""
import dataclasses
import time
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.limiters.rate_limiter import RateLimiter
from leak_snek.interfaces.storages.rate import Rate
from leak_snek.interfaces.storages.rate_store import RateStorage
from leak_snek.interfaces.values.rate_limit import RateLimit

T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class LeakyBucketLimiter(RateLimiter[T_contra]):
    """Leaky bucket rate limiting algorithm.

    Manages incoming requests using a 'bucket' with capacity and leak rate.
    Requests are added if space is available, otherwise, they're discarded or delayed.
    The bucket gradually empties to maintain a controlled output rate, preventing congestion and DDoS attacks.
    """

    rate_limit: RateLimit
    rate_storage: RateStorage[T_contra]

    @override
    def limit_exceeded(self: Self, key: T_contra) -> bool:
        rate = self.rate_storage.read(key)

        now = time.monotonic()

        leaked = int((now - rate.updated_at) / self.rate_limit.period.seconds * self.rate_limit.operations)

        new_operations = rate.operations + 1 - leaked

        if new_operations > self.rate_limit.operations:
            return True

        self.rate_storage.write(key=key, value=Rate(operations=max(new_operations, 0), updated_at=now))

        return False
