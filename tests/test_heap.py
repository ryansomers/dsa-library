import pytest

from dsa.heap import MinHeap, heapify


def test_push_pop_returns_sorted_order():
    h: MinHeap[int] = MinHeap()
    for x in [5, 3, 8, 1, 9, 2]:
        h.push(x)
    assert [h.pop() for _ in range(len(h))] == [1, 2, 3, 5, 8, 9]


def test_pop_empty_raises_index_error():
    with pytest.raises(IndexError):
        MinHeap[int]().pop()


def test_peek_does_not_remove():
    h = heapify([4, 2, 7])
    assert h.peek() == 2
    assert len(h) == 3


def test_heapify_builds_valid_heap():
    h = MinHeap.heapify([9, 8, 7, 6, 5, 4, 3, 2, 1])
    assert [h.pop() for _ in range(9)] == list(range(1, 10))


def test_tuples_compare_by_priority_first():
    h = heapify([(3, "c"), (1, "a"), (2, "b")])
    assert h.pop() == (1, "a")
    assert h.peek() == (2, "b")


def test_duplicates_are_kept():
    h = heapify([2, 1, 2, 1])
    assert [h.pop() for _ in range(4)] == [1, 1, 2, 2]
