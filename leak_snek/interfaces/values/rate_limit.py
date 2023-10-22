"""Rate limit value module."""
import dataclasses
from datetime import timedelta
from typing import final


@final
@dataclasses.dataclass
class RateLimit:
    """A model representing a rate limit.

    This data class describes a rate limit in terms of the number of operations
    allowed within a specific time period. It encapsulates the maximum count of
    operations and the duration (period) within which these operations can occur.

    Attributes:
    ----------
    - operations (int): The maximum number of operations allowed within the
                        specified time period.
    - period (timedelta): The duration within which the specified number of
                          operations can occur.

    Example:
    -------
    To represent a rate limit of 100 operations allowed within 1 hour:
    >>> rate_limit = RateLimit(operations=100, period=timedelta(hours=1))
    """

    operations: int
    period: timedelta
