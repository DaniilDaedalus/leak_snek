import dataclasses
import time
from typing import Self

from leak_snek.interfaces.bucket import LeakRateInterface


@dataclasses.dataclass
class Bucket:
    capacity: int
    volume: int
    last_leak: float
    leak_rate: LeakRateInterface

    def overflows(self: Self, volume: int) -> bool:
        self.volume -= self.leak_rate.leak(self.last_leak)

        if self.volume < 0:
            self.volume = 0

        self.last_leak = time.monotonic()

        self.volume += volume

        if self.volume > self.capacity:
            self.volume = self.capacity
            return True

        return False
