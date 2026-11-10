"""Binary min-heap stored in a Python list.

The tree is implicit: the children of index ``i`` live at ``2i + 1`` and ``2i + 2``
and its parent at ``(i - 1) // 2``. Only ``<`` is used to compare items, so any
type that defines ``__lt__`` (ints, strings, tuples such as ``(priority, item)``)
works.

Complexity: push O(log n), pop O(log n), peek O(1), heapify O(n), space O(n).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Generic, Protocol, Self, TypeVar


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=SupportsLessThan)


class MinHeap(Generic[T]):
    """A min-priority queue: ``pop`` always returns the smallest item."""

    def __init__(self) -> None:
        self._data: list[T] = []

    @classmethod
    def heapify(cls, items: Iterable[T]) -> Self:
        """Build a heap from ``items`` in O(n).

        Sifting down every internal node from the last one (n//2 - 1) back to the
        root is linear, not O(n log n): most nodes sit near the bottom and only
        move a level or two.
        """
        heap = cls()
        heap._data = list(items)
        for i in range(len(heap._data) // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap

    def push(self, item: T) -> None:
        """Add ``item``. O(log n)."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the smallest item. O(log n).

        Raises:
            IndexError: if the heap is empty.
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        data = self._data
        # Move the last leaf to the root, then let it sink to its place.
        data[0], data[-1] = data[-1], data[0]
        smallest = data.pop()
        if data:
            self._sift_down(0)
        return smallest

    def peek(self) -> T:
        """Return the smallest item without removing it. O(1)."""
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def _sift_up(self, i: int) -> None:
        data = self._data
        while i > 0:
            parent = (i - 1) // 2
            if data[i] < data[parent]:
                data[i], data[parent] = data[parent], data[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        data = self._data
        n = len(data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and data[left] < data[smallest]:
                smallest = left
            if right < n and data[right] < data[smallest]:
                smallest = right
            if smallest == i:
                return
            data[i], data[smallest] = data[smallest], data[i]
            i = smallest


def heapify(items: Iterable[T]) -> MinHeap[T]:
    """Function form of :meth:`MinHeap.heapify`."""
    return MinHeap.heapify(items)
