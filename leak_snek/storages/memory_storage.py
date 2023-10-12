"""The implementation of in-memory rate storage."""
import dataclasses
from collections.abc import Hashable
from typing import Self, TypeVar, final

from leak_snek.interfaces.storages.rate import Rate
from leak_snek.interfaces.storages.rate_store import RateStorage

T_contra = TypeVar("T_contra", contravariant=True, bound=Hashable)


@final
@dataclasses.dataclass
class MemoryStorage(RateStorage[T_contra]):
    """Storage with rates stored in memory."""

    _rates: dict[T_contra, Rate] = dataclasses.field(default_factory=dict)

    def read(self: Self, key: T_contra) -> Rate:
        """Get rate for given key."""
        rate = self._rates.get(key)

        if rate is None:
            rate = Rate.default()
            self._rates[key] = rate

            return rate

        return rate

    def write(self: Self, key: T_contra, value: Rate) -> None:
        """Write rate for given key."""
        self._rates[key] = value
