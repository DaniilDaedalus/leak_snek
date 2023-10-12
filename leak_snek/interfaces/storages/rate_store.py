"""Module containing the base interface for the access rate storing."""
from typing import Protocol, Self, TypeVar

from leak_snek.interfaces.storages.rate import Rate

T_contra = TypeVar("T_contra", contravariant=True)


class RateStorage(Protocol[T_contra]):
    """Storage holding the information about the current access rate."""

    def read(self: Self, key: T_contra) -> Rate:
        """Get rate for given key."""
        raise NotImplementedError

    def write(self: Self, key: T_contra, value: Rate) -> None:
        """Write rate for given key."""
        raise NotImplementedError
