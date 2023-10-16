"""Mutex implementation storing locks in memory."""
from __future__ import annotations

import dataclasses
from collections.abc import AsyncGenerator, Callable, Hashable
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Generic, Protocol, Self, TypeVar, final, override

from leak_snek.interfaces.mutexes.aio.mutex import AsyncMutex

if TYPE_CHECKING:
    from types import TracebackType


class AsyncLockInterface(Protocol):
    """Interface representing any kind of lock supporting context manager interface."""

    async def __aenter__(self: Self) -> None:
        """Acquire the lock."""
        raise NotImplementedError

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        tb: TracebackType | None = None,
    ) -> None:
        """Release the lock."""
        raise NotImplementedError


T_contra = TypeVar("T_contra", contravariant=True, bound=Hashable)
L = TypeVar("L", bound=AsyncLockInterface)


@final
@dataclasses.dataclass
class AsyncMemoryMutex(AsyncMutex[T_contra], Generic[T_contra, L]):
    """Mutex storing locks for keys in memory."""

    local_lock: L
    lock_factory: Callable[[], L]
    key_locks: dict[T_contra, L] = dataclasses.field(default_factory=dict)

    @override
    @asynccontextmanager
    async def lock(self: Self, key: T_contra) -> AsyncGenerator[None, None]:
        """Lock the access to the given key."""
        async with self.local_lock:
            key_lock = self.key_locks.get(key)

            if key_lock is None:
                key_lock = self.lock_factory()

                self.key_locks[key] = key_lock

        async with key_lock:
            yield
