from time import sleep
from leak_snek.leak_rate import LeakRate
from leak_snek.rate_limiter import RateLimiter
from leak_snek.storage import InMemoryStorage
from datetime import timedelta


leak_rate = LeakRate(volume=10, period=timedelta(seconds=1).seconds)
storage: InMemoryStorage[str] = InMemoryStorage(bucket_leak_rate=leak_rate, bucket_capacity=10)
rate_limiter = RateLimiter(storage=storage)

print(1, rate_limiter.limit_exceeded("asd", 1))

sleep(0.9)

for i in range(20):
    print(i + 2, rate_limiter.limit_exceeded("asd", 1))

