"""Async mutex interface controlling the access to the stored rates."""
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol, Self, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncMutex(Protocol[T_contra]):
    """Async mutex for controlled access to stored rates based on keys.

    This protocol describes a mutex mechanism that provides controlled and
    synchronized access to stored rates. Implementers of this protocol should
    provide a context manager through the `lock` method to manage the access
    based on given keys. This ensures that the rate data remains consistent
    and safe from race conditions or other concurrent access issues.

    The Mutex protocol can be tailored to work with different types of keys
    using the contravariant type variable, `T_contra`.

    Typical usage:

    class ConcreteMutex(Mutex[str]):
        def lock(self, key: str) -> AbstractAsyncContextManager[Any]:
            # Implementation details here

    with ConcreteMutex().lock("some_key"):
        # Safely access and modify stored rates

    Methods
    -------
    - lock: A method returning a context manager for accessing stored rates
            for a given key.

    Type Parameters
    ---------------
    - T_contra: Represents the type of the key used for locking.
    """

    def lock(self: Self, key: T_contra) -> AbstractAsyncContextManager[Any]:
        """Obtain a context manager for safe access to stored rates for the specified key.

        This method should be implemented by concrete classes to return a context
        manager which, when used with a `with` statement, provides synchronized
        access to stored rates for the given key.

        Args:
        ----
        key (T_contra): The key (identifier) for which the mutex should be locked.

        Returns:
        -------
        AbstractAsyncContextManager[Any]: A context manager that controls access to
                                      stored rates for the given key.

        """
        raise NotImplementedError
