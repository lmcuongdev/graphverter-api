import json
from contextlib import suppress
from typing import Callable, Optional, TypeVar

T = TypeVar('T')


def safe_load_json(
    json_string: str,
    *,
    default_factory: Callable[[], T] = None,
) -> Optional[T]:
    """
    Try to load a JSON object from a JSON string. If there is any exception,
    return ``None``, or ``default_factory()`` if ``default_factory`` is provided.
    """

    with suppress(Exception):
        loaded = json.loads(json_string)
        if loaded is not None:
            return loaded

    if default_factory is not None:
        return default_factory()

    return None
