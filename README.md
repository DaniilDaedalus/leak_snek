# Leak Snek Rate Limiting

![leak snek logo](assets/logo.png)
[![coverage](https://codecov.io/gh/WinterCitizen/leak_snek/graph/badge.svg?token=HJ98830KGG)](https://codecov.io/gh/WinterCitizen/leak_snek)

Leak Snek is a Python library that provides a flexible and extensible implementation of rate limiting for your applications

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [License](#license)

## Features

- **Asynchronous and Synchronous Support**: The library provides support for both asynchronous and synchronous rate.
- **Flexible Rate Limiting Algorithms**: Define your custom rate limiting algorithms by implementing the `RateLimiter` and `AsyncRateLimiter` interfaces.
- **Rate Storage**: Manage rate information with the `RateStorage` and `AsyncRateStorage` interfaces.
- **Leaky Bucket Algorithm**: Included implementations of the Leaky Bucket Algorithm for both asynchronous and synchronous use cases.

## Getting Started

1. **Installation**:

   Install Leak Snek using pip:

   ```bash
   pip install leak_snek
   ```

2. **Usage**:

   You can use the provided classes and interfaces to implement rate limiting in your Python applications. Additionally, if you need the Leaky Bucket Algorithm, you can use the provided implementations.

   - Synchronous Leaky Bucket Algorithm:

     ```python
     from threading import Lock

     from leak_snek.limiters.leaky_bucket import LeakyBucketLimiter
     from leak_snek.mutexes.memory_mutex import MemoryMutex
     from leak_snek.shortcuts.rate_limit import rl
     from leak_snek.storages.memory_storage import MemoryStorage

     limiter = LeakyBucketLimiter[str](
         rate_limit=rl("10/m"),
         rate_storage=MemoryStorage(),
         key_mutex=MemoryMutex(
             local_lock=Lock(),
             lock_factory=lambda: Lock(),
         ),
     )

     if not limiter.limit_exceeded("my_key"):
         ... # Perform the operation
     ```

   - Asynchronous Leaky Bucket Algorithm:

     ```python
     from collections.abc import AsyncGenerator, Awaitable
     from contextlib import asynccontextmanager
     from typing import Any, Self, cast, override

     from redis.asyncio import Redis

     from leak_snek.interfaces.mutexes.aio.mutex import AsyncMutex
     from leak_snek.interfaces.storages.aio.rate_store import AsyncRateStorage
     from leak_snek.interfaces.values.rate import Rate
     from leak_snek.limiters.aio.leaky_bucket import AsyncLeakyBucketLimiter
     from leak_snek.shortcuts.rate_limit import rl


     @dataclasses.dataclass
     class RedisAsyncRateStorage(AsyncRateStorage[str]):
         redis: Redis

         async def read(self: Self, key: str) -> Rate:
             if not await self.redis.exists(key):
                 return Rate.default()

             rate_dict = await cast(Awaitable[dict[Any, Any]], self.redis.hgetall(name=key))

             return Rate(operations=int(rate_dict[b"operations"]), updated_at=float(rate_dict[b"updated_at"]))

         async def write(self: Self, key: str, value: Rate) -> None:
             await cast(
                 Awaitable[int],
                 self.redis.hset(name=key, mapping={"operations": value.operations, "updated_at": value.updated_at}),
             )


     @dataclasses.dataclass
     class RedisAsyncMutex(AsyncMutex[str]):
         redis: Redis

         @override
         @asynccontextmanager
         async def lock(self: Self, key: str) -> AsyncGenerator[None, None]:
             async with self.redis.lock(f"{key}_lock"):
                 yield


     async def main() -> None:
         async_limiter = AsyncLeakyBucketLimiter(
             rate_limit=rl("10/m"),
             rate_storage=RedisAsyncRateStorage(redis=Redis()),
             key_mutex=RedisAsyncMutex(redis=Redis()),
         )

         if not await async_limiter.limit_exceeded("my_key"):
             ...  # Perform the operation
          ```

In asynchronous example we implement our own async storage & mutex b/c leak_snek doesn't provide redis integration and it doesn't make much of a sense to implement asynchronous in-memory store.

## License

Leak Snek Rate Limiting is released under the MIT License. See the [LICENSE](LICENSE) file for details.

---
