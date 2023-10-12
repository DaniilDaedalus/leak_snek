"""Fake async rate limiter implementaion."""
import dataclasses
from typing import Self, TypeVar

from leak_snek.interfaces.limiters.aio.rate_limiter import AsyncRateLimiter

T_contra = TypeVar("T_contra", contravariant=True)


@dataclasses.dataclass
class FakeAsyncRateLimiter(AsyncRateLimiter[T_contra]):
    """Fake rate limiter implementation with control over limit exceeded state."""

    exceeded: bool

    async def limit_exceeded(self: Self, key: T_contra) -> bool:  # noqa: ARG002 - unused arg is ok in fake
        """Return static exceeded state ignoring the key."""
        return self.exceeded
