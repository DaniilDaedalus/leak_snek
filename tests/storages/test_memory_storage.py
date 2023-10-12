"""Test memory storage."""
from time import monotonic

from leak_snek.interfaces.storages.rate import Rate
from leak_snek.storages.memory_storage import MemoryStorage


def test_memory_storage() -> None:
    """Test memory storage read/write."""
    # Given:
    key = "test_key"
    memory_storage = MemoryStorage[str]()

    rate = Rate(operations=1, updated_at=monotonic())

    # When: rate is written for the key
    memory_storage.write(key, rate)

    # Then: the same rate is returned for the same key
    assert memory_storage.read(key) == rate


def test_memory_storage_default() -> None:
    """Test that memory storage returns zero initialized rate for not stored key read."""
    # Given:
    memory_storage = MemoryStorage[str]()

    # When: not stored key is read from the storage
    rate = memory_storage.read("key")

    # Then: default zero initialized rate is returned
    assert rate.operations == 0
