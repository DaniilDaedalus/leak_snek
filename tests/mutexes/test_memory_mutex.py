"""Test memory mutex."""
from leak_snek.mutexes.memory_mutex import MemoryMutex
from tests.fakes.mutex import FakeLock


def test_memory_mutex() -> None:
    """Test that memory lock locks the keys."""
    # Given:
    test_key = "test_key"
    key_lock = FakeLock()
    memory_mutex = MemoryMutex[str, FakeLock](local_lock=FakeLock(), lock_factory=lambda: key_lock)

    # When: mutex lock context manager is entered
    with memory_mutex.lock(test_key):
        # Then: the key is locked
        assert key_lock.locked

    # Then: and unlocked after exiting the lock context manager
    assert not key_lock.locked
