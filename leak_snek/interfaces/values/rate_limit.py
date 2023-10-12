"""Rate limit value module."""
import dataclasses
from datetime import timedelta
from typing import final


@final
@dataclasses.dataclass
class RateLimit:
    """Model describing a limit of operations per time period."""

    operations: int
    period: timedelta
