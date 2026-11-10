"""Classic dynamic-programming problems.

Each function states its time and space complexity. Where a full 2-D table is not
needed, the table is rolled down to one or two rows to save space.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def fibonacci(n: int) -> int:
    """n-th Fibonacci number with F(0)=0, F(1)=1, bottom-up.

    Time O(n), space O(1): only the last two values are needed.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def coin_change(coins: Sequence[int], amount: int) -> int:
    """Fewest coins summing to ``amount`` (unlimited supply), or -1 if impossible.

    best[a] = 1 + min(best[a - c]) over coins c <= a.
    Time O(amount * len(coins)), space O(amount).
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    impossible = amount + 1  # more coins than any real answer could use
    best = [0] + [impossible] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if 0 < c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == impossible else best[amount]


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """Max total value of items fitting in ``capacity``, each item used at most once.

    One row indexed by capacity, filled from high capacity down to low: going
    downward means best[c - w] still holds the value *without* the current item,
    which is what stops an item being taken twice.
    Time O(n * capacity), space O(capacity).
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must be the same length")
    best = [0] * (capacity + 1)
    for w, v in zip(weights, values, strict=True):
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def longest_common_subsequence(a: Sequence[Any], b: Sequence[Any]) -> int:
    """Length of the longest common subsequence of ``a`` and ``b``.

    L[i][j] = L[i-1][j-1] + 1 if a[i-1] == b[j-1], else max(L[i-1][j], L[i][j-1]).
    Time O(len(a) * len(b)), space O(len(b)) with two rolling rows.
    """
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def edit_distance(a: Sequence[Any], b: Sequence[Any]) -> int:
    """Levenshtein distance: fewest single-element inserts, deletes or substitutions
    turning ``a`` into ``b``.

    Time O(len(a) * len(b)), space O(len(b)) with two rolling rows.
    """
    prev = list(range(len(b) + 1))  # turning "" into b[:j] takes j inserts
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)  # turning a[:i] into "" takes i deletes
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(
                    prev[j],  # delete a[i-1]
                    cur[j - 1],  # insert b[j-1]
                    prev[j - 1],  # substitute
                )
        prev = cur
    return prev[-1]


def _lower_bound(xs: list[Any], target: Any) -> int:
    """First index i with xs[i] >= target in sorted ``xs`` (len(xs) if none). O(log n)."""
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def longest_increasing_subsequence(nums: Sequence[Any]) -> int:
    """Length of the longest strictly increasing subsequence.

    Patience-sorting idea: tails[k] is the smallest possible last value of an
    increasing subsequence of length k + 1. tails stays sorted, so each new value
    either extends it or replaces the first tail >= itself (binary search).
    Time O(n log n), space O(n).
    """
    tails: list[Any] = []
    for x in nums:
        i = _lower_bound(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
