from typing import Generic, Protocol, Self, TypeVar

from leak_snek.interfaces.bucket import BucketInterface

T = TypeVar("T", contravariant=True)

class StorageInterface(Protocol, Generic[T]):
    def read(self: Self, key: T) -> BucketInterface:
        raise NotImplementedError

    def write(self: Self, key: T, bucket: BucketInterface) -> None:
        raise NotImplementedError
