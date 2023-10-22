"""Rate limit constructor module."""
from datetime import timedelta
from io import StringIO

from leak_snek.interfaces.values.rate_limit import RateLimit


def rl(rate_limit: str) -> RateLimit:
    """Parse a rate limit string and convert it into a RateLimit object.

    This function takes a rate limit string in the format "<operations>/[<period>]<unit>", where
    <operations> is the number of operations allowed, <period> is the time period during which these
    operations are allowed and <unit> is a mesurement unit for the period (`s`, `m`, `h`, `d` supported).
    The function parses this string and returns a RateLimit object with the corresponding values.

    Args:
    ----
    rate_limit: The rate limit string to be parsed.

    Returns:
    -------
    RateLimit: A RateLimit object containing the parsed rate limit values.

    Raises:
    ------
    ValueError: If the rate limit string is not in the expected format or contains
                invalid characters.

    Example:
    -------
    >>> rl("100/m")
    RateLimit(operations=100, period=datetime.timedelta(seconds=60))

    >>> rl(100/5m)
    RateLimit(operations=100, period=datetime.timedelta(seconds=300))

    >>> rl(100/1.5h)
    RateLimit(operations=100, period=datetime.timedelta(seconds=5400))
    """
    period_unit_lookup = {
        "s": timedelta(seconds=1),
        "m": timedelta(minutes=1),
        "h": timedelta(hours=1),
        "d": timedelta(days=1),
    }

    operations = ""
    period = ""
    period_unit = timedelta()

    buffer = StringIO(rate_limit)

    while character := buffer.read(1):
        if character == "/":
            break

        if not character.isdigit():
            offset = buffer.tell() - 1
            msg = f"\n    {rate_limit} - Unknown character at position {offset}\n    {' ' * offset}^"
            raise ValueError(msg)

        operations += character
    else:
        msg = "Unexpected end of rate limit string."
        raise ValueError(msg)

    dot_count = 0

    while character := buffer.read(1):
        if character == "." and period and dot_count < 1:
            dot_count += 1

            period += character
            continue

        if character.isdigit():
            period += character
            continue

        if character in period_unit_lookup:
            period_unit = period_unit_lookup[character]
            break

        offset = buffer.tell() - 1
        msg = f"\n    {rate_limit} - Unknown character at position {offset}\n    {' ' * offset}^"
        raise ValueError(msg)
    else:
        msg = "Unexpected end of rate limit string."
        raise ValueError(msg)

    if not period:
        period = "1"

    return RateLimit(operations=int(operations), period=period_unit * float(period))
