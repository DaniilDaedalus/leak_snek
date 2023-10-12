"""Test async rate limit decorator."""
import dataclasses
from collections.abc import Awaitable
from typing import Self

from leak_snek.decorators.aio.rate_limit import async_rate_limit
from tests.fakes.aio.limiter import FakeAsyncRateLimiter


@dataclasses.dataclass
class FakeAsyncFunction:
    """Fake async function implementation recording calls to itself."""

    called: bool = False

    def __call__(self: Self) -> Awaitable[None]:
        """Set called state to True."""

        async def inner() -> None:
            self.called = True

        return inner()


async def test_rate_limit() -> None:
    """Test that decorated async function is called when limit is not exceeded."""
    # Given: rate limiter in not exceeded state
    rate_limiter = FakeAsyncRateLimiter[str](exceeded=False)
    decorator = async_rate_limit(rate_limiter, lambda: "key", None)
    function = FakeAsyncFunction()

    decorated = decorator(function)

    # When: function decorated with not exceeded limiter is called
    await decorated()

    # Then: the function is called
    assert function.called


async def test_rate_limit_exceeded() -> None:
    """Test that decorated async function is not called when limit is exceeded."""
    # Given: rate limiter in exceeded state
    rate_limiter = FakeAsyncRateLimiter[str](exceeded=True)
    decorator = async_rate_limit(rate_limiter, lambda: "key", None)
    function = FakeAsyncFunction()

    decorated = decorator(function)

    # When: function decorated with exceeded limiter is called
    await decorated()

    # Then: the function is not called
    assert not function.called
