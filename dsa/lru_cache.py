"""Least-recently-used cache with O(1) get and put.

Two structures work together:
- a hash map (this library's HashMap) from key to linked-list node, for O(1) lookup;
- a doubly linked list ordered by recency, for O(1) move-to-front and evict-oldest.

Sentinel head/tail nodes mean insert and unlink never special-case an empty list.
Most recent sits right after ``head``; the eviction victim sits right before ``tail``.

Complexity: get/put O(1) average; space O(capacity).
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Any, Generic, TypeVar

from dsa.hash_map import HashMap

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: _Node = self
        self.next: _Node = self


class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map: HashMap[K, _Node] = HashMap()
        self._head = _Node()
        self._tail = _Node()
        self._head.next, self._tail.prev = self._tail, self._head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: K) -> V | None:
        """Value for ``key`` (marking it most recent), or None if absent."""
        node = self._map.get(key)
        if node is None:
            return None
        self._unlink(node)
        self._push_front(node)
        value: V = node.value
        return value

    def put(self, key: K, value: V) -> None:
        """Insert or update ``key``; evicts the least recent entry when full."""
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._map) == self.capacity:
            oldest = self._tail.prev
            self._unlink(oldest)
            self._map.remove(oldest.key)
        node = _Node(key, value)
        self._map.put(key, node)
        self._push_front(node)

    def keys(self) -> list[K]:
        """Keys from most to least recently used."""
        out: list[K] = []
        node = self._head.next
        while node is not self._tail:
            out.append(node.key)
            node = node.next
        return out

    def __contains__(self, key: object) -> bool:
        return key in self._map

    def __len__(self) -> int:
        return len(self._map)
