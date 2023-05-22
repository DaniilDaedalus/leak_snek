import dataclasses
from collections.abc import Hashable
from typing import Generic, Self, TypeVar

from leak_snek.bucket import Bucket
from leak_snek.interfaces.bucket import BucketInterface, LeakRateInterface

T = TypeVar("T", bound=Hashable)


@dataclasses.dataclass
class InMemoryStorage(Generic[T]):
    bucket_leak_rate: LeakRateInterface
    bucket_capacity: int
    _buckets: dict[T, BucketInterface] = dataclasses.field(default_factory=dict)

    def read(self: Self, key: T) -> BucketInterface:
        bucket = self._buckets.get(key)

        if bucket is None:
            return Bucket(capacity=self.bucket_capacity, volume=0, last_leak=0.0, leak_rate=self.bucket_leak_rate)

        return bucket

    def write(self: Self, key: T, bucket: BucketInterface) -> None:
        self._buckets[key] = bucket

