"""Module containing rate model."""
from __future__ import annotations

import dataclasses
import time
from typing import Self, final


@dataclasses.dataclass
@final
class Rate:
    """A model representing the current access rate.

    This data class encapsulates information about the current access rate
    in terms of the number of operations and the last update time. It provides
    a default initialization mechanism with zero operations and the current
    monotonic time.

    Attributes
    ----------
    operations (int): The number of operations for the current rate.
    updated_at (float): The timestamp when the rate was last updated,
                          represented in monotonic time.

    Methods
    -------
    default: Class method to provide a default (zero initialized) rate.
    """

    operations: int
    updated_at: float

    @classmethod
    def default(cls: type[Self]) -> Self:
        """Get the default (zero initialized) rate.

        Returns
        -------
        Rate: A default rate instance with zero operations and the current
                monotonic time as the last update time.
        """
        return cls(operations=0, updated_at=time.monotonic())
