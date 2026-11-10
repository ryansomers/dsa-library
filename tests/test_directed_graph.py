import pytest

from dsa.directed_graph import CycleError, DirectedGraph


def make(edges) -> DirectedGraph:
    """Build from (u, v) or (u, v, capacity) tuples."""
    g = DirectedGraph()
    for e in edges:
        g.add_edge(*e)
    return g


def test_topological_sort_respects_edges():
    g = make([("shirt", "tie"), ("tie", "jacket"), ("pants", "shoes"),
              ("pants", "belt"), ("belt", "jacket"), ("shirt", "belt")])
    order = g.topological_sort()
    pos = {v: i for i, v in enumerate(order)}
    for u in g.vertices():
        for v in g.successors(u):
            assert pos[u] < pos[v]
    assert order == ["pants", "shirt", "belt", "shoes", "tie", "jacket"]


def test_topological_sort_detects_cycle():
    with pytest.raises(CycleError):
        make([(1, 2), (2, 3), (3, 1)]).topological_sort()


def test_tarjan_scc():
    g = make([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4), (7, 6)])
    assert g.strongly_connected_components() == [[1, 2, 3], [4, 5, 6], [7]]


def test_tarjan_deep_chain_does_not_hit_recursion_limit():
    g = make([(i, i + 1) for i in range(5000)])
    assert len(g.strongly_connected_components()) == 5001


def test_max_flow_clrs_example():
    # CLRS Figure 26.1 network; max flow 23.
    g = make([("s", "v1", 16), ("s", "v2", 13), ("v1", "v3", 12), ("v2", "v1", 4),
              ("v2", "v4", 14), ("v3", "v2", 9), ("v3", "t", 20), ("v4", "v3", 7),
              ("v4", "t", 4)])
    assert g.max_flow("s", "t") == 23


def test_max_flow_needs_reverse_edge():
    # BFS first augments along s-x-y-t, which blocks both s-p-y and x-q-t. The
    # only way to reach flow 2 is the path s-p-y-x-q-t, which pushes flow
    # backwards along x->y through the residual reverse edge.
    g = make([("s", "x", 1), ("s", "p", 1), ("x", "y", 1), ("x", "q", 1),
              ("p", "y", 1), ("y", "t", 1), ("q", "t", 1)])
    assert g.max_flow("s", "t") == 2


def test_max_flow_disconnected_is_zero():
    g = make([("s", "a", 5), ("b", "t", 5)])
    assert g.max_flow("s", "t") == 0
