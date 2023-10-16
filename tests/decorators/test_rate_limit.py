"""Test rate limit decorator."""
import dataclasses
from typing import Self, final

from leak_snek.decorators.rate_limit import rate_limit
from tests.fakes.limiter import FakeRateLimiter


@final
@dataclasses.dataclass
class FakeFunction:
    """Fake function implementation recording calls to itself."""

    called: bool = False

    def __call__(self: Self) -> None:
        """Set called state to True."""
        self.called = True


def test_rate_limit() -> None:
    """Test that decorated function is called when limit is not exceeded."""
    # Given: rate limiter in not exceeded state
    rate_limiter = FakeRateLimiter[str](exceeded=False)
    decorator = rate_limit(rate_limiter, lambda: "key", None)
    function = FakeFunction()

    decorated = decorator(function)

    # When: function decorated with not exceeded limiter is called
    decorated()

    # Then: the function is called
    assert function.called


def test_rate_limit_exceeded() -> None:
    """Test that decorated function is not called when limit is exceeded."""
    # Given: rate limiter in exceeded state
    rate_limiter = FakeRateLimiter[str](exceeded=True)
    decorator = rate_limit(rate_limiter, lambda: "key", None)
    function = FakeFunction()

    decorated = decorator(function)

    # When: function decorated with exceeded limiter is called
    decorated()

    # Then: the function is not called
    assert not function.called
