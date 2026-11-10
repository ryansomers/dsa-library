import pytest

from dsa.dp import (
    coin_change,
    edit_distance,
    fibonacci,
    knapsack_01,
    longest_common_subsequence,
    longest_increasing_subsequence,
)


def test_fibonacci():
    assert [fibonacci(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fibonacci(90) == 2880067194370816120


def test_fibonacci_negative_raises():
    with pytest.raises(ValueError):
        fibonacci(-1)


def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([1, 3, 4], 6) == 2  # greedy would give 3 (4+1+1)


def test_knapsack_01():
    assert knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    assert knapsack_01([10], [100], 5) == 0
    assert knapsack_01([2], [3], 4) == 3  # item not reused


def test_lcs():
    assert longest_common_subsequence("ABCBDAB", "BDCABA") == 4
    assert longest_common_subsequence("abc", "") == 0


def test_edit_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "abc") == 3
    assert edit_distance("same", "same") == 0


def test_lis():
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence([7, 7, 7]) == 1  # strictly increasing
    assert longest_increasing_subsequence([]) == 0
