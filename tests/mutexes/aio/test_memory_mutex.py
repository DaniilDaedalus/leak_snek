"""Test async memory mutex."""
from leak_snek.mutexes.aio.memory_mutex import AsyncMemoryMutex
from tests.fakes.aio.mutex import FakeAsyncLock


async def test_async_memory_mutex() -> None:
    """Test that async memory lock locks the keys."""
    # Given:
    test_key = "test_key"
    key_lock = FakeAsyncLock()
    memory_mutex = AsyncMemoryMutex[str, FakeAsyncLock](local_lock=FakeAsyncLock(), lock_factory=lambda: key_lock)

    # When: mutex lock context manager is entered
    async with memory_mutex.lock(test_key):
        # Then: the key is locked
        assert key_lock.locked

    # Then: and unlocked after exiting the lock context manager
    assert not key_lock.locked
