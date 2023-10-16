"""Fake limiter implementaton."""
import dataclasses
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.limiters.rate_limiter import RateLimiter

T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class FakeRateLimiter(RateLimiter[T_contra]):
    """Fake rate limiter implementation with control over limit exceeded state."""

    exceeded: bool

    @override
    def limit_exceeded(self: Self, key: T_contra) -> bool:  # - unused arg is ok in fake
        """Return static exceeded state ignoring the key."""
        return self.exceeded
