import pytest

from dsa.lru_cache import LRUCache


def test_evicts_least_recently_used():
    c: LRUCache[int, str] = LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    assert c.get(1) == "a"  # 1 becomes most recent
    c.put(3, "c")  # evicts 2
    assert 2 not in c
    assert c.get(2) is None
    assert c.keys() == [3, 1]


def test_update_existing_moves_to_front_without_eviction():
    c: LRUCache[str, int] = LRUCache(2)
    c.put("x", 1)
    c.put("y", 2)
    c.put("x", 10)
    assert len(c) == 2
    assert c.get("x") == 10
    c.put("z", 3)  # evicts y, the least recent
    assert c.keys() == ["z", "x"]


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LRUCache(0)
