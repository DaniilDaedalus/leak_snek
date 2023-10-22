"""The implementation of in-memory rate storage."""
from __future__ import annotations

import dataclasses
from collections.abc import Hashable
from typing import Self, TypeVar, final, override

from leak_snek.interfaces.storages.rate_store import RateStorage
from leak_snek.interfaces.values.rate import Rate

T_contra = TypeVar("T_contra", contravariant=True, bound=Hashable)


@final
@dataclasses.dataclass
class MemoryStorage(RateStorage[T_contra]):
    """A storage implementation that keeps access rates in memory.

    `MemoryStorage` holds rates associated with specific keys directly in memory. This provides fast read and write
    operations but lacks persistence across system restarts or crashes. It is ideal for scenarios where rapid access
    is essential and the data does not need to be retained over the long term.

    Attributes
    ----------
        _rates (dict[T_contra, Rate]): An internal dictionary mapping unique keys to their respective access rates.

    Methods
    -------
        read: Retrieves the access rate for a given key.
        write: Sets the access rate for a specified key.
    """

    _rates: dict[T_contra, Rate] = dataclasses.field(default_factory=dict)

    @override
    def read(self: Self, key: T_contra) -> Rate:
        """Retrieve the access rate for the specified key.

        If the key does not exist in the storage, a default rate is set and returned.

        Args:
        ----
        key (T_contra): The key whose access rate needs to be fetched.

        Returns:
        -------
        Rate: The access rate associated with the given key.
        """
        rate = self._rates.get(key)

        if rate is None:
            rate = Rate.default()
            self._rates[key] = rate

            return rate

        return rate

    @override
    def write(self: Self, key: T_contra, value: Rate) -> None:
        """Set the access rate for a specified key.

        This method updates or inserts the access rate for the given key in the storage.

        Args:
        ----
        key (T_contra): The key whose access rate needs to be set or updated.
        value (Rate): The access rate to be set for the specified key.
        """
        self._rates[key] = value
