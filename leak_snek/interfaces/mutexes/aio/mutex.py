"""Async mutex interface controlling the access to the stored rates."""
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncMutex(Protocol[T_contra]):
    """Async mutex controlling the access to the stored rates by key."""

    def lock(self: Self, key: T_contra) -> AbstractAsyncContextManager[Any]:
        """Get async context manager allowing the access to stored rates."""
        raise NotImplementedError
