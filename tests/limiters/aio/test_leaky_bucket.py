"""Tests for async leaky bucket rate limiting algorithm."""
import time
from datetime import timedelta

from leak_snek.interfaces.values.rate import Rate
from leak_snek.interfaces.values.rate_limit import RateLimit
from leak_snek.limiters.aio.leaky_bucket import AsyncLeakyBucketLimiter
from tests.fakes.aio.mutex import FakeAsyncMutex
from tests.fakes.aio.storage import FakeAsyncStorage


async def test_leaky_bucket() -> None:
    """Test that async leaky bucket algorithm limits operations."""
    # Given: leaky bucket limiter allowing 1 operation per minute
    key = "test_key"
    limiter: AsyncLeakyBucketLimiter[str] = AsyncLeakyBucketLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(minutes=1)),
        rate_storage=FakeAsyncStorage(),
        key_mutex=FakeAsyncMutex(),
    )

    # When: limit exceeded is called two times consecutively
    # Then: first time limit is not exceeded and second time it is
    assert not await limiter.limit_exceeded(key)
    assert await limiter.limit_exceeded(key)


async def test_leaky_bucket_leak() -> None:
    """Test that async leaky bucket algorithm drains the bucket over time."""
    # Given: leaky bucket limiter allowing 2 operations per minute
    #   and two operations were made 30 seconds ago
    key = "test_key"
    storage: FakeAsyncStorage[str] = FakeAsyncStorage()
    limiter: AsyncLeakyBucketLimiter[str] = AsyncLeakyBucketLimiter(
        rate_limit=RateLimit(operations=2, period=timedelta(minutes=1)),
        rate_storage=storage,
        key_mutex=FakeAsyncMutex(),
    )

    await storage.write(key, Rate(operations=2, updated_at=time.monotonic() - 30))

    # When: limit exceeded is called two times consecutively
    # Then: only one operation is allowed b/c the bucket was drained for 1 operation
    assert not await limiter.limit_exceeded(key)
    assert await limiter.limit_exceeded(key)
