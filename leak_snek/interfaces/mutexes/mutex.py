"""Mutex interface controlling the access to the stored rates."""
from contextlib import AbstractContextManager
from typing import Any, Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class Mutex(Protocol[T_contra]):
    """Mutex controlling the access to the stored rates by key."""

    def lock(self: Self, key: T_contra) -> AbstractContextManager[Any]:
        """Get context manager allowing the access to stored rates."""
        raise NotImplementedError
