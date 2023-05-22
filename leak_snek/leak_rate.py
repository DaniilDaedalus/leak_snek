import dataclasses
import time
from typing import Self


@dataclasses.dataclass
class LeakRate:
    volume: int
    period: float

    def leak(self: Self, last_leak: float) -> int:
        now = time.monotonic()

        if last_leak > now:
            msg = "Last leak time can't be greater than now"
            raise ValueError(msg)

        return int((now - last_leak) / self.period * self.volume)
