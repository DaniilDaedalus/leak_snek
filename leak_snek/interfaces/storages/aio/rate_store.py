"""Module containing async rate storage interface."""
from typing import Protocol, Self, TypeVar

from leak_snek.interfaces.storages.rate import Rate

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncRateStorage(Protocol[T_contra]):
    """Async storage holding the information about the current access rate."""

    async def read(self: Self, key: T_contra) -> Rate:
        """Get rate for given key."""
        raise NotImplementedError

    async def write(self: Self, key: T_contra, value: Rate) -> None:
        """Write rate for given key."""
        raise NotImplementedError
