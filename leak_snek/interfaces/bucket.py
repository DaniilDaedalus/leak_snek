from typing import Protocol, Self


class LeakRateInterface(Protocol):
    def leak(self: Self, last_leak: float) -> int:
        raise NotImplementedError


class BucketInterface(Protocol):
    def overflows(self: Self, volume: int) -> bool:
        raise NotImplementedError
