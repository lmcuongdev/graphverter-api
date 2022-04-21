from typing import Iterable

from memcache import Client


class MemcacheClient(Client):
    def __init__(self, *args, **kwargs):
        self._prefix_key = kwargs.pop('prefix_key', '')
        super().__init__(*args, **kwargs)

    def _make_key(self, key):
        return self._prefix_key + key

    def set(self, key, *args, **kwargs):
        return super().set(self._make_key(key), *args, **kwargs)

    def get(self, key):
        return super().get(self._make_key(key))

    def delete(self, key, *args, **kwargs):
        return super().delete(self._make_key(key), *args, **kwargs)

    def delete_multi(self, keys: Iterable[str], *args, **kwargs):
        return super().delete_multi(keys, *args, key_prefix=self._prefix_key, **kwargs)
