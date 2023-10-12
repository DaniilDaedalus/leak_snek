"""Test rl shortcut."""
from datetime import timedelta

import pytest

from leak_snek.interfaces.values.rate_limit import RateLimit
from leak_snek.shortcuts.rate_limit import rl


@pytest.mark.parametrize(
    ("rate_limit", "expected"),
    [
        ("1/s", RateLimit(operations=1, period=timedelta(seconds=1))),
        ("1/m", RateLimit(operations=1, period=timedelta(minutes=1))),
        ("1/h", RateLimit(operations=1, period=timedelta(hours=1))),
        ("1/d", RateLimit(operations=1, period=timedelta(days=1))),
        ("1/1.5m", RateLimit(operations=1, period=timedelta(minutes=1.5))),
    ],
)
def test_rl(rate_limit: str, expected: RateLimit) -> None:
    """Test that rl properly parses rate limits."""
    # Given:
    # When: rl is called with valid rate limit string
    # Then: corresponding rate limit object is returned
    assert rl(rate_limit) == expected


@pytest.mark.parametrize(
    ("rate_limit", "message_regex"),
    [
        ("", "Unexpected end of rate limit string."),
        ("/", "Unexpected end of rate limit string."),
        ("1", "Unexpected end of rate limit string."),
        ("1/", "Unexpected end of rate limit string."),
        ("1m", "Unknown character at position"),
        ("1/y", "Unknown character at position"),
    ],
)
def test_rl_fail(rate_limit: str, message_regex: str) -> None:
    """Test that rl raises exceptions for invalid rate limit strings."""
    # Given:
    # When: rl is called with an invalid rate limit string
    # Then: corresponding exception is raised
    with pytest.raises(ValueError, match=message_regex):
        rl(rate_limit)
