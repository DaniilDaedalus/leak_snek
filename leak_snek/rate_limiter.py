import dataclasses
from typing import Generic, Self, TypeVar

from leak_snek.interfaces.storage import StorageInterface

T = TypeVar("T", contravariant=True)


@dataclasses.dataclass
class RateLimiter(Generic[T]):
    storage: StorageInterface[T]

    def limit_exceeded(self: Self, key: T, operations: int) -> bool:
        bucket = self.storage.read(key)

        if bucket.overflows(operations):
            self.storage.write(key, bucket)
            return True

        self.storage.write(key, bucket)
        return False
