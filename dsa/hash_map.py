"""Hash map with separate chaining, built on plain lists (no dict or set).

Each bucket is a list of ``[key, value]`` pairs. A key lives in bucket
``hash(key) % capacity``. When the load factor (size / capacity) passes 0.75 the
table doubles and every pair is re-bucketed, which keeps chains short.

Complexity: put/get/remove/contains O(1) average, O(n) worst case (all keys in one
bucket); a resize is O(n) but happens rarely enough that put is O(1) amortized.
keys() is O(n + capacity). Space O(n + capacity).
"""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from typing import Any, Generic, TypeVar, overload

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
D = TypeVar("D")

_MAX_LOAD = 0.75


class HashMap(Generic[K, V]):
    def __init__(self, capacity: int = 8) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._buckets: list[list[list[Any]]] = [[] for _ in range(capacity)]
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    def _bucket(self, key: object) -> list[list[Any]]:
        return self._buckets[hash(key) % len(self._buckets)]

    def _find(self, key: object) -> list[Any] | None:
        """Return the [key, value] pair for ``key``, or None. Lets callers tell a
        stored None value apart from a missing key."""
        for pair in self._bucket(key):
            if pair[0] == key:
                return pair
        return None

    def put(self, key: K, value: V) -> None:
        """Insert or overwrite ``key``. O(1) amortized."""
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size / len(self._buckets) > _MAX_LOAD:
            self._resize(2 * len(self._buckets))

    @overload
    def get(self, key: K) -> V | None: ...
    @overload
    def get(self, key: K, default: D) -> V | D: ...
    def get(self, key: K, default: Any = None) -> Any:
        """Return the value for ``key``, or ``default`` if absent. O(1) average."""
        pair = self._find(key)
        return default if pair is None else pair[1]

    def remove(self, key: K) -> V:
        """Delete ``key`` and return its value. O(1) average.

        Raises:
            KeyError: if ``key`` is not present.
        """
        bucket = self._bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Order inside a bucket does not matter, so swap-with-last makes
                # the delete O(1) instead of shifting the tail of the list.
                bucket[i] = bucket[-1]
                bucket.pop()
                self._size -= 1
                value: V = v
                return value
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        return self._find(key) is not None

    def __getitem__(self, key: K) -> V:
        pair = self._find(key)
        if pair is None:
            raise KeyError(key)
        value: V = pair[1]
        return value

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def keys(self) -> list[K]:
        """All keys, in bucket order (not insertion order). O(n + capacity)."""
        return [pair[0] for bucket in self._buckets for pair in bucket]

    def items(self) -> list[tuple[K, V]]:
        return [(pair[0], pair[1]) for bucket in self._buckets for pair in bucket]

    def __iter__(self) -> Iterator[K]:
        return iter(self.keys())

    def __len__(self) -> int:
        return self._size

    def _resize(self, new_capacity: int) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(new_capacity)]
        for bucket in old:
            for pair in bucket:
                self._buckets[hash(pair[0]) % new_capacity].append(pair)
