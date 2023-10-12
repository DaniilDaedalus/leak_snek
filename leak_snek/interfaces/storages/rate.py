"""Module containing rate model."""
import dataclasses
import time
from typing import Self, final


@dataclasses.dataclass
@final
class Rate:
    """Model representing the current access rate."""

    operations: int
    updated_at: float

    @classmethod
    def default(cls: type[Self]) -> Self:
        """Get the default (zero initialized) rate."""
        return cls(operations=0, updated_at=time.monotonic())
