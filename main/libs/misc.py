import json
import re
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


def parse_path(path: str):
    """
    'data[0].items' => ['data', '[0]', 'items']
    'data.item.key' => ['data', 'item', 'key']
    """
    regex = r'\[\d+\]$'
    result = []
    for item in path.split('.'):
        matches = re.finditer(regex, item)
        try:
            match = next(matches)
            match_index = match.start()
            result.extend((item[:match_index], item[match_index:]))
        except StopIteration:
            # If this is not something like items[1]
            result.append(item)
    return result
