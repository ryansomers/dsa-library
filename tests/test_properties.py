"""Property-based tests: compare each structure to a trusted model on random input."""

import math

from hypothesis import given, settings
from hypothesis import strategies as st

from dsa.avl_tree import AVLTree
from dsa.dp import edit_distance, longest_increasing_subsequence
from dsa.graph import Graph
from dsa.hash_map import HashMap
from dsa.heap import MinHeap
from dsa.trie import Trie
from dsa.union_find import UnionFind

ints = st.integers(min_value=-1000, max_value=1000)


@given(st.lists(ints), st.lists(ints))
def test_avl_matches_sorted_set_and_stays_balanced(inserts, deletes):
    t = AVLTree(inserts)
    assert t.inorder() == sorted(set(inserts))
    assert t.is_balanced()
    for k in deletes:
        t.delete(k)
    expected = sorted(set(inserts) - set(deletes))
    assert t.inorder() == expected
    assert len(t) == len(expected)
    assert t.is_balanced()


@given(st.lists(ints))
def test_heap_pops_in_sorted_order(xs):
    h: MinHeap[int] = MinHeap()
    for x in xs:
        h.push(x)
    assert [h.pop() for _ in range(len(xs))] == sorted(xs)
    h2 = MinHeap.heapify(xs)
    assert [h2.pop() for _ in range(len(xs))] == sorted(xs)


# A random script of operations, replayed against both HashMap and dict.
ops = st.lists(
    st.tuples(st.sampled_from(["put", "remove", "get"]), st.integers(-20, 20), ints)
)


@given(ops)
def test_hash_map_matches_dict_model(script):
    m: HashMap[int, int] = HashMap(capacity=1)
    model: dict[int, int] = {}
    for op, k, v in script:
        if op == "put":
            m.put(k, v)
            model[k] = v
        elif op == "remove":
            if k in model:
                assert m.remove(k) == model.pop(k)
            else:
                assert k not in m
        else:
            assert m.get(k) == model.get(k)
        assert len(m) == len(model)
    assert sorted(m.items()) == sorted(model.items())


def bellman_ford(n: int, edges: list[tuple[int, int, int]], src: int) -> list[float]:
    """Brute-force reference: relax every edge n - 1 times."""
    dist = [math.inf] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            for a, b in ((u, v), (v, u)):  # undirected
                if dist[a] + w < dist[b]:
                    dist[b] = dist[a] + w
    return dist


@st.composite
def random_graphs(draw):
    n = draw(st.integers(1, 12))
    edge = st.tuples(st.integers(0, n - 1), st.integers(0, n - 1), st.integers(0, 50))
    raw = draw(st.lists(edge, max_size=40))
    # Keep the last weight per vertex pair, as Graph.add_edge overwrites.
    by_pair = {}
    for u, v, w in raw:
        if u != v:
            by_pair[(min(u, v), max(u, v))] = w
    return n, [(u, v, w) for (u, v), w in by_pair.items()]


@settings(max_examples=200)
@given(random_graphs())
def test_dijkstra_matches_bellman_ford(graph):
    n, edges = graph
    g = Graph()
    for v in range(n):
        g.add_vertex(v)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    dist, _ = g.dijkstra(0)
    expected = bellman_ford(n, edges, 0)
    for v in range(n):
        assert dist.get(v, math.inf) == expected[v]
        path = g.shortest_path(0, v)
        if expected[v] == math.inf:
            assert path == []
        else:
            weights = {(a, b): w for a, b, w in edges} | {(b, a): w for a, b, w in edges}
            assert sum(weights[p] for p in zip(path, path[1:], strict=False)) == expected[v]


@given(random_graphs())
def test_mst_spans_each_component(graph):
    n, edges = graph
    g = Graph()
    for v in range(n):
        g.add_vertex(v)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    total, chosen = g.minimum_spanning_tree()
    uf = UnionFind(range(n))
    for u, v, _ in edges:
        uf.union(u, v)
    assert len(chosen) == n - uf.components  # spanning forest edge count
    assert total == sum(w for w, _, _ in chosen)
    assert total == prim_forest_weight(n, edges)


def prim_forest_weight(n: int, edges: list[tuple[int, int, int]]) -> int:
    """Simple O(V * E) Prim reference: grow each tree by its cheapest crossing edge."""
    seen: set[int] = set()
    total = 0
    for start in range(n):
        if start in seen:
            continue
        seen.add(start)
        # Earlier trees are complete, so every crossing edge touches this tree.
        while True:
            cands = [(w, u, v) for u, v, w in edges if (u in seen) != (v in seen)]
            if not cands:
                break
            w, u, v = min(cands)
            seen.add(v if u in seen else u)
            total += w
    return total


def lis_quadratic(xs: list[int]) -> int:
    best = [1] * len(xs)
    for i in range(len(xs)):
        for j in range(i):
            if xs[j] < xs[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


@given(st.lists(st.integers(-50, 50), max_size=60))
def test_lis_matches_quadratic_dp(xs):
    assert longest_increasing_subsequence(xs) == lis_quadratic(xs)


@given(st.text("abc", max_size=8), st.text("abc", max_size=8))
def test_edit_distance_is_symmetric_and_bounded(a, b):
    d = edit_distance(a, b)
    assert d == edit_distance(b, a)
    assert abs(len(a) - len(b)) <= d <= max(len(a), len(b))


@given(st.lists(st.text("ab", max_size=5)), st.text("ab", max_size=3))
def test_trie_prefix_matches_filter(words, prefix):
    t = Trie(words)
    assert t.words_with_prefix(prefix) == sorted({w for w in words if w.startswith(prefix)})
