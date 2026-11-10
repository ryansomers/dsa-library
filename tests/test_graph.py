import pytest

from dsa.graph import Graph


@pytest.fixture
def g() -> Graph:
    #   A --1-- B --2-- C
    #   |       |       |
    #   4       5       1
    #   |       |       |
    #   D --3-- E --1-- F      plus an isolated vertex Z
    graph = Graph()
    for u, v, w in [
        ("A", "B", 1), ("B", "C", 2), ("A", "D", 4), ("B", "E", 5),
        ("C", "F", 1), ("D", "E", 3), ("E", "F", 1),
    ]:
        graph.add_edge(u, v, w)
    graph.add_vertex("Z")
    return graph


def test_bfs_order(g):
    assert g.bfs("A") == ["A", "B", "D", "C", "E", "F"]


def test_dfs_order(g):
    assert g.dfs("A") == ["A", "B", "C", "F", "E", "D"]


def test_dijkstra_distances(g):
    dist, _ = g.dijkstra("A")
    assert dist == {"A": 0, "B": 1, "C": 3, "D": 4, "E": 5, "F": 4}


def test_shortest_path(g):
    assert g.shortest_path("A", "E") == ["A", "B", "C", "F", "E"]
    assert g.shortest_path("A", "A") == ["A"]


def test_shortest_path_unreachable_is_empty(g):
    assert g.shortest_path("A", "Z") == []
    assert g.shortest_path("A", "missing") == []


def test_minimum_spanning_tree(g):
    total, edges = g.minimum_spanning_tree()
    assert total == 8  # A-B 1, C-F 1, E-F 1, B-C 2, D-E 3
    assert len(edges) == 5


def test_negative_weight_rejected():
    with pytest.raises(ValueError):
        Graph().add_edge(1, 2, -1)
