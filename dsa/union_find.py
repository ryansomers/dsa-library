"""Disjoint-set union (union-find) with path compression and union by rank.

Together the two optimizations make each operation O(alpha(n)) amortized, where
alpha is the inverse Ackermann function (at most 4 for any practical n).
Space O(n).
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    def __init__(self, items: Iterable[T] = ()) -> None:
        self._parent: dict[T, T] = {}
        self._rank: dict[T, int] = {}
        self._components = 0
        for item in items:
            self.add(item)

    def add(self, item: T) -> None:
        """Create a singleton set for ``item`` (no-op if it already exists)."""
        if item not in self._parent:
            self._parent[item] = item
            self._rank[item] = 0
            self._components += 1

    def find(self, item: T) -> T:
        """Return the representative of ``item``'s set. Unknown items raise KeyError."""
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        # Path compression: point every node on the walk straight at the root.
        while self._parent[item] != root:
            self._parent[item], item = root, self._parent[item]
        return root

    def union(self, a: T, b: T) -> bool:
        """Merge the sets of ``a`` and ``b``. Returns False if already together."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by rank: hang the shallower tree under the deeper one.
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        self._components -= 1
        return True

    def connected(self, a: T, b: T) -> bool:
        return self.find(a) == self.find(b)

    @property
    def components(self) -> int:
        return self._components

    def __len__(self) -> int:
        return len(self._parent)
