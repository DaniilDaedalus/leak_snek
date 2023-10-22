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
    """Mutex implementation that stores locks for specific keys in memory.

    `MemoryMutex` manages locks based on provided keys. It ensures that critical sections of code associated with
    specific keys can be accessed in a thread-safe manner. This is especially useful for operations that require
    exclusive access to resources identified by unique keys.

    Attributes
    ----------
    local_lock (L): A local lock that protects the internal state of the `MemoryMutex`, ensuring
                    thread-safe operations when managing key-specific locks.
    lock_factory (Callable[[], L]): A factory function that creates a new lock instance whenever needed.
    key_locks (dict[T_contra, L]): A dictionary mapping unique keys to their corresponding locks.

    Methods
    -------
    lock: Provides a context manager to lock access to a specific key, ensuring exclusive access to the
          critical section of code associated with that key.
    """

    local_lock: L
    lock_factory: Callable[[], L]
    key_locks: dict[T_contra, L] = dataclasses.field(default_factory=dict)

    @override
    @contextmanager
    def lock(self: Self, key: T_contra) -> Generator[None, None, None]:
        """Lock the access to the given key, ensuring exclusive access to the associated critical section.

        This method provides a context manager that can be used with a `with` statement. When entering the
        context, the access to the provided key is locked, and when exiting the context, the lock is released.

        Args:
        ----
        key (T_contra): The key for which exclusive access is required.

        Yields:
        ------
        None: Yields once the lock for the given key is acquired.
              The actual critical section of code should be placed inside the `with` block.
        """
        with self.local_lock:
            key_lock = self.key_locks.get(key)

            if key_lock is None:
                key_lock = self.lock_factory()

                self.key_locks[key] = key_lock

        with key_lock:
            yield
