"""Self-balancing AVL binary search tree.

Invariant: at every node the heights of the left and right subtrees differ by at
most 1. That bounds the height at about 1.44 log2(n), so search, insert and delete
are O(log n) worst case. Each node caches its height; after an insert or delete we
walk back up the recursion, refresh heights and rotate wherever the balance factor
reaches +/-2.

Height convention: height counts levels, so an empty subtree has height 0 and a
leaf has height 1.

Complexity: insert/delete/contains O(log n); inorder O(n); height O(1);
is_balanced O(n); space O(n).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Generic, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Comparable)


class _Node(Generic[K]):
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: _Node[K] | None = None
        self.right: _Node[K] | None = None
        self.height = 1


class AVLTree(Generic[K]):
    def __init__(self, keys: Iterable[K] = ()) -> None:
        self.root: _Node[K] | None = None
        self._size = 0
        for key in keys:
            self.insert(key)

    # ---- helpers -----------------------------------------------------------

    @staticmethod
    def _h(node: _Node[K] | None) -> int:
        return node.height if node else 0

    def _update(self, node: _Node[K]) -> None:
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _balance(self, node: _Node[K] | None) -> int:
        """Left height minus right height. >1 means left-heavy, <-1 right-heavy."""
        return self._h(node.left) - self._h(node.right) if node else 0

    def _rotate_right(self, y: _Node[K]) -> _Node[K]:
        #       y            x
        #      / \          / \
        #     x   C   ->   A   y
        #    / \              / \
        #   A   B            B   C
        x = y.left
        assert x is not None
        y.left = x.right
        x.right = y
        self._update(y)  # y is now below x, so refresh it first
        self._update(x)
        return x

    def _rotate_left(self, x: _Node[K]) -> _Node[K]:
        # Mirror image of _rotate_right.
        y = x.right
        assert y is not None
        x.right = y.left
        y.left = x
        self._update(x)
        self._update(y)
        return y

    def _rebalance(self, node: _Node[K]) -> _Node[K]:
        """Restore the AVL invariant at ``node`` and return the subtree's new root."""
        self._update(node)
        bf = self._balance(node)
        if bf > 1:  # left-heavy
            assert node.left is not None
            if self._balance(node.left) < 0:  # LR: left child leans right
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)  # LL (or LR after the first rotation)
        if bf < -1:  # right-heavy
            assert node.right is not None
            if self._balance(node.right) > 0:  # RL: right child leans left
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)  # RR (or RL after the first rotation)
        return node

    # ---- public API --------------------------------------------------------

    def insert(self, key: K) -> bool:
        """Insert ``key``; duplicates are ignored. Returns True if it was added."""
        before = self._size
        self.root = self._insert(self.root, key)
        return self._size > before

    def _insert(self, node: _Node[K] | None, key: K) -> _Node[K]:
        if node is None:
            self._size += 1
            return _Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif node.key < key:
            node.right = self._insert(node.right, key)
        else:
            return node  # duplicate: nothing changed below, no rebalance needed
        return self._rebalance(node)

    def delete(self, key: K) -> bool:
        """Remove ``key``. Returns True if it was present."""
        before = self._size
        self.root = self._delete(self.root, key)
        return self._size < before

    def _delete(self, node: _Node[K] | None, key: K) -> _Node[K] | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif node.key < key:
            node.right = self._delete(node.right, key)
        else:
            # Zero or one child: splice the node out.
            if node.left is None or node.right is None:
                self._size -= 1
                return node.left or node.right
            # Two children: copy the in-order successor (smallest key in the right
            # subtree) into this node, then delete the successor from the right
            # subtree. The successor has no left child, so that delete hits the
            # easy case above. Every node on the path back up gets rebalanced,
            # because unlike insert a delete can need rotations at several levels.
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return self._rebalance(node)

    def contains(self, key: K) -> bool:
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return True
        return False

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def inorder(self) -> list[K]:
        """Keys in sorted order (iterative, so deep trees cannot hit the recursion limit)."""
        out: list[K] = []
        stack: list[_Node[K]] = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            out.append(node.key)
            node = node.right
        return out

    def height(self) -> int:
        """Number of levels: 0 if empty, 1 for a single node."""
        return self._h(self.root)

    def is_balanced(self) -> bool:
        """Check the AVL invariant and cached heights everywhere. O(n); for tests."""

        def check(node: _Node[K] | None) -> int | None:
            # Returns the true height, or None if anything below is wrong.
            if node is None:
                return 0
            lh, rh = check(node.left), check(node.right)
            if lh is None or rh is None or abs(lh - rh) > 1:
                return None
            h = 1 + max(lh, rh)
            return h if h == node.height else None

        return check(self.root) is not None

    def __len__(self) -> int:
        return self._size
