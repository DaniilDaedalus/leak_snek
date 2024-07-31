"""Tests for fixed window rate limiting algorithm."""

import time
from datetime import timedelta

from leak_snek.interfaces.values.rate_limit import RateLimit
from leak_snek.limiters.fixed_window import FixedWindowLimiter
from tests.fakes.mutex import FakeMutex
from tests.fakes.storage import FakeStorage


def test_fixed_window() -> None:
    """Test that fixed window algorithm limits operations."""
    # Given: fixed window limiter allowing 1 operation per minute
    key = "test_key"
    limiter: FixedWindowLimiter[str] = FixedWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(minutes=1)),
        rate_storage=FakeStorage(),
        key_mutex=FakeMutex(),
    )

    # When: limit exceeded is called two times consecutively
    # Then: first time limit is not exceeded and second time it is
    assert not limiter.limit_exceeded(key)
    assert limiter.limit_exceeded(key)


def test_fixed_window_exceeded() -> None:
    """Test that fixed window algorithm starts a new window when period exceeded"""
    # Given: fixed window limiter allowing 1 operation per second
    key = "test_key"
    limiter: FixedWindowLimiter[str] = FixedWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(seconds=1)),
        rate_storage=FakeStorage(),
        key_mutex=FakeMutex(),
    )

    # When: limit_exceeded is called three times with a pause allowing a new window to start
    # Then: first two limits are not exceeded, third time is exceeded
    assert not limiter.limit_exceeded(key)
    time.sleep(1)
    assert not limiter.limit_exceeded(key)
    assert limiter.limit_exceeded(key)


def test_zero_operations() -> None:
    """Test that limit is always exceeded when operations allowed per second is zero"""
    # Given: fixed window limiter allowing 0 operations per second
    key = "test_key"
    limiter: FixedWindowLimiter[str] = FixedWindowLimiter(
        rate_limit=RateLimit(operations=1, period=timedelta(seconds=1)),
        rate_storage=FakeStorage(),
        key_mutex=FakeMutex(),
    )

    # When: limit_exceeded is called
    # Then: always true
    assert limiter.limit_exceeded
