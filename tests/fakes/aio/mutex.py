"""Fake async mutex related interface implementations."""
from __future__ import annotations

import dataclasses
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Any, Self, TypeVar, final, override

from leak_snek.interfaces.mutexes.aio.mutex import AsyncMutex

if TYPE_CHECKING:
    from types import TracebackType


@final
@dataclasses.dataclass
class FakeAsyncLock(AbstractAsyncContextManager[Any]):
    """Fake async lock implementations recording it's state."""

    locked: bool = False

    @override
    async def __aenter__(self: Self) -> None:
        """Set lock state to locked."""
        self.locked = True

    @override
    async def __aexit__(
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
class FakeAsyncMutex(AsyncMutex[T_contra]):
    """Fake async mutex implementation working with fake locks."""

    key_locks: dict[T_contra, FakeAsyncLock] = dataclasses.field(default_factory=dict)

    @override
    def lock(self: Self, key: T_contra) -> AbstractAsyncContextManager[Any]:
        """Get fake lock not bound to the key."""
        lock = self.key_locks.get(key)

        if lock is None:
            lock = FakeAsyncLock()
            self.key_locks[key] = lock

        return lock
