from typing import Generic, Protocol, Self, TypeVar

T = TypeVar("T", contravariant=True)


class RateLimiterInterface(Protocol, Generic[T]):
    def limit_exceeded(self: Self, key: T) -> bool:
        raise NotImplementedError
