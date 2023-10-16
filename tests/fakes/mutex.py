"""Fake mutex related interface implementations."""
from __future__ import annotations

import dataclasses
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Any, Self, TypeVar, final, override

from leak_snek.interfaces.mutexes.mutex import Mutex

if TYPE_CHECKING:
    from types import TracebackType


@final
@dataclasses.dataclass
class FakeLock(AbstractContextManager[Any]):
    """Fake lock implementations recording it's state."""

    locked: bool = False

    @override
    def __enter__(self: Self) -> None:
        """Set lock state to locked."""
        self.locked = True

    @override
    def __exit__(
        self: Self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        tb: TracebackType | None = None,
    ) -> None:
        """Set lock state to unlocked."""
        self.locked = False


T_contra = TypeVar("T_contra", contravariant=True)


@final
@dataclasses.dataclass
class FakeMutex(Mutex[T_contra]):
    """Fake mutex implementation working with fake locks."""

    key_locks: dict[T_contra, FakeLock] = dataclasses.field(default_factory=dict)

    @override
    def lock(self: Self, key: T_contra) -> AbstractContextManager[Any]:
        """Get fake lock not bound to the key."""
        lock = self.key_locks.get(key)

        if lock is None:
            lock = FakeLock()
            self.key_locks[key] = lock

        return lock
