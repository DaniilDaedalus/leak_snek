"""Mutex implementation storing locks in memory."""
from __future__ import annotations

import dataclasses
from collections.abc import Callable, Generator, Hashable
from contextlib import AbstractContextManager, contextmanager
from typing import Any, Generic, Protocol, Self, TypeVar, final, override

from leak_snek.interfaces.mutexes.mutex import Mutex


class LockInterface(AbstractContextManager[Any], Protocol):
    """Interface representing any kind of lock supporting context manager interface."""


T_contra = TypeVar("T_contra", contravariant=True, bound=Hashable)
L = TypeVar("L", bound=LockInterface)


@final
@dataclasses.dataclass
class MemoryMutex(Mutex[T_contra], Generic[T_contra, L]):
    """Mutex storing locks for keys in memory."""

    local_lock: L
    lock_factory: Callable[[], L]
    key_locks: dict[T_contra, L] = dataclasses.field(default_factory=dict)

    @override
    @contextmanager
    def lock(self: Self, key: T_contra) -> Generator[None, None, None]:
        """Lock the access to the given key."""
        with self.local_lock:
            key_lock = self.key_locks.get(key)

            if key_lock is None:
                key_lock = self.lock_factory()

                self.key_locks[key] = key_lock

        with key_lock:
            yield
