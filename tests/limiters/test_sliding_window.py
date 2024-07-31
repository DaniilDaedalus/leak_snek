"""Tests for sliding window rate limiting algorithm."""

import time
from datetime import timedelta

from leak_snek.interfaces.values.rate import Rate
from leak_snek.interfaces.values.rate_limit import RateLimit
from leak_snek.limiters.sliding_window import SlidingWindowLimiter
from tests.fakes.mutex import FakeMutex
from tests.fakes.storage import FakeStorage


def test_sliding_window() -> None:
    """Test that sliding window algorithm limits operations."""
    # Given: sliding window limiter allowing 1 operation per minute
    key = "test_key"
    limiter: SlidingWindowLimiter[str] = SlidingWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(minutes=1)),
        rate_storage=FakeStorage(),
        key_mutex=FakeMutex(),
    )

    # When: limit exceeded is called two times consecutively
    # Then: first time limit is not exceeded and second time it is
    assert not limiter.limit_exceeded(key)
    assert limiter.limit_exceeded(key)


def test_sliding_window_elapsed_exceeds_period():
    # Given: sliding window limiter allowing 1 operation per second
    key = "test_key"
    storage: FakeStorage[str] = FakeStorage()
    limiter: SlidingWindowLimiter[str] = SlidingWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(seconds=1)),
        rate_storage=storage,
        key_mutex=FakeMutex(),
    )

    # When: limit_exceeded is called twice after the initial window expires
    # Then: limit will only be exceeded the second time
    storage.write(key, Rate(operations=0, updated_at=time.monotonic() - 2))
    assert not limiter.limit_exceeded(key)
    assert limiter.limit_exceeded(key)


def test_sliding_window_boundary() -> None:
    """Test that boundary condition cannot be exploited as in fixed window limiting."""
    # Given: sliding window limiter allowing 1 operation per second
    key = "test_key"
    storage: FakeStorage[str] = FakeStorage()
    limiter: SlidingWindowLimiter[str] = SlidingWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(seconds=1)),
        rate_storage=storage,
        key_mutex=FakeMutex(),
    )

    # When: limit_exceeded is called twice at the window boundary
    # Then: limit will be exceeded the second time despite being outside the boundary
    storage.write(key, Rate(operations=0, updated_at=time.monotonic() - 0.95))
    assert not limiter.limit_exceeded(key)
    time.sleep(0.1)
    assert limiter.limit_exceeded(key)
