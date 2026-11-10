import pytest

from dsa.hash_map import HashMap


def test_put_get_and_overwrite():
    m: HashMap[str, int] = HashMap()
    m.put("a", 1)
    m.put("b", 2)
    m.put("a", 10)
    assert m.get("a") == 10
    assert m.get("b") == 2
    assert len(m) == 2


def test_get_missing_returns_default():
    m: HashMap[str, int] = HashMap()
    assert m.get("x") is None
    assert m.get("x", -1) == -1


def test_remove_returns_value_and_missing_raises_key_error():
    m: HashMap[str, int] = HashMap()
    m.put("a", 1)
    assert m.remove("a") == 1
    assert "a" not in m
    assert len(m) == 0
    with pytest.raises(KeyError):
        m.remove("a")


def test_resizes_past_load_factor_and_keeps_all_keys():
    m: HashMap[int, int] = HashMap(capacity=4)
    for i in range(100):
        m.put(i, i * i)
    assert m.capacity >= 128  # 100 / 0.75 > 64, so at least 128 buckets
    assert len(m) / m.capacity <= 0.75
    assert all(m.get(i) == i * i for i in range(100))
    assert sorted(m.keys()) == list(range(100))


def test_contains_and_colliding_keys():
    # In CPython hash(-1) == hash(-2) == -2, so these two keys always collide.
    m: HashMap[int, str] = HashMap()
    m.put(-1, "minus one")
    m.put(-2, "minus two")
    assert -1 in m and -2 in m
    assert m.get(-1) == "minus one"
    m.remove(-1)
    assert m.get(-2) == "minus two"


def test_none_value_is_distinguished_from_missing():
    m: HashMap[str, None] = HashMap()
    m.put("k", None)
    assert "k" in m
    assert "z" not in m


def test_dunder_access():
    m: HashMap[str, int] = HashMap()
    m["x"] = 5
    assert m["x"] == 5
    with pytest.raises(KeyError):
        _ = m["y"]
