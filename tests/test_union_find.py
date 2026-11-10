from dsa.union_find import UnionFind


def test_union_and_find():
    uf = UnionFind(range(5))
    assert uf.components == 5
    assert uf.union(0, 1) and uf.union(3, 4)
    assert uf.connected(0, 1) and not uf.connected(1, 3)
    assert uf.components == 3


def test_union_same_set_returns_false():
    uf = UnionFind("ab")
    uf.union("a", "b")
    assert uf.union("b", "a") is False
    assert uf.components == 1


def test_path_compression_flattens_chain():
    uf = UnionFind(range(6))
    for i in range(5):
        uf.union(i, i + 1)
    root = uf.find(5)
    assert all(uf._parent[i] == root for i in range(6))
