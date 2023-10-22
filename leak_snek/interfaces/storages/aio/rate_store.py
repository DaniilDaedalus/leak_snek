"""Module containing async rate storage interface."""
from typing import Protocol, Self, TypeVar

from leak_snek.interfaces.values.rate import Rate

T_contra = TypeVar("T_contra", contravariant=True)


class AsyncRateStorage(Protocol[T_contra]):
    """Protocol defining async storage operations for access rate information.

    This protocol outlines the contract for storage systems that aim to store
    and manage access rate information. It defines two primary methods: `read`
    to fetch the rate for a given key, and `write` to store or update the rate
    for a given key.

    Implementers of this protocol can work with different types of keys based
    on the contravariant type variable, `T_contra`.

    Methods
    -------
    - read: Fetch the rate for a given key.
    - write: Store or update the rate for a given key.
    """

    async def read(self: Self, key: T_contra) -> Rate:
        """Fetch the rate for the specified key.

        Args:
        ----
        key (T_contra): The key for which the rate should be fetched.

        Returns:
        -------
        Rate: The access rate corresponding to the given key.
        """
        raise NotImplementedError

    async def write(self: Self, key: T_contra, value: Rate) -> None:
        """Store or update the rate for the specified key.

        Args:
        ----
        key (T_contra): The key for which the rate should be stored/updated.
        value (Rate): The access rate to be stored/updated.

        Returns:
        -------
        None
        """
        raise NotImplementedError
