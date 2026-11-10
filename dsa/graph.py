"""Undirected weighted graph stored as an adjacency list.

Vertices can be any hashable, orderable value (ints, strings). BFS and DFS visit
neighbors in sorted order so traversals are deterministic and easy to test.

Complexity (V vertices, E edges):
    add_edge O(1); bfs/dfs O(V + E log d) with the per-vertex neighbor sort
    (d = max degree), plain traversal is O(V + E);
    dijkstra O((V + E) log V); minimum_spanning_tree (Kruskal) O(E log E);
    space O(V + E).
"""

from __future__ import annotations

from collections import deque
from typing import Any

from dsa.heap import MinHeap
from dsa.union_find import UnionFind

Vertex = Any  # hashable and comparable with `<`; kept loose for ints and strings
Edge = tuple[float, Vertex, Vertex]  # (weight, u, v)


class Graph:
    def __init__(self) -> None:
        self._adj: dict[Vertex, dict[Vertex, float]] = {}

    def add_vertex(self, v: Vertex) -> None:
        self._adj.setdefault(v, {})

    def add_edge(self, u: Vertex, v: Vertex, weight: float = 1.0) -> None:
        """Add an undirected edge; adding it again overwrites the weight."""
        if weight < 0:
            raise ValueError("negative weights are not supported (Dijkstra needs >= 0)")
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight
        self._adj[v][u] = weight

    def vertices(self) -> list[Vertex]:
        return sorted(self._adj)

    def neighbors(self, v: Vertex) -> list[tuple[Vertex, float]]:
        return sorted(self._adj[v].items())

    def edges(self) -> list[Edge]:
        """Each undirected edge once, as (weight, u, v) with u < v."""
        return [(w, u, v) for u in self._adj for v, w in self._adj[u].items() if u < v]

    def __contains__(self, v: Vertex) -> bool:
        return v in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def bfs(self, start: Vertex) -> list[Vertex]:
        """Vertices in breadth-first order from ``start`` (by hop count)."""
        seen = {start}
        order: list[Vertex] = []
        queue = deque([start])
        while queue:
            u = queue.popleft()
            order.append(u)
            for v, _ in self.neighbors(u):
                if v not in seen:
                    # Mark when enqueued, not when dequeued, so a vertex can't be
                    # queued twice by two different neighbors.
                    seen.add(v)
                    queue.append(v)
        return order

    def dfs(self, start: Vertex) -> list[Vertex]:
        """Vertices in depth-first preorder, matching the recursive version.

        Iterative with an explicit stack. Neighbors are pushed in reverse sorted
        order so the smallest one is popped (visited) first.
        """
        seen: set[Vertex] = set()
        order: list[Vertex] = []
        stack = [start]
        while stack:
            u = stack.pop()
            if u in seen:
                continue  # pushed more than once before we got to it
            seen.add(u)
            order.append(u)
            for v, _ in reversed(self.neighbors(u)):
                if v not in seen:
                    stack.append(v)
        return order

    def dijkstra(self, source: Vertex) -> tuple[dict[Vertex, float], dict[Vertex, Vertex]]:
        """Single-source shortest paths for non-negative weights.

        Returns ``(dist, prev)``: shortest distance to every reachable vertex, and
        each vertex's predecessor on its shortest path (for path reconstruction).

        The heap has no decrease-key, so an improved distance is pushed as a new
        entry and the old one is left behind. When a stale entry (its distance is
        worse than the best known) comes out of the heap we skip it.
        """
        dist: dict[Vertex, float] = {source: 0.0}
        prev: dict[Vertex, Vertex] = {}
        heap: MinHeap[tuple[float, Vertex]] = MinHeap()
        heap.push((0.0, source))
        while heap:
            d, u = heap.pop()
            if d > dist[u]:
                continue  # stale entry
            for v, w in self._adj[u].items():
                nd = d + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heap.push((nd, v))
        return dist, prev

    def shortest_path(self, source: Vertex, target: Vertex) -> list[Vertex]:
        """Vertices on a shortest path from ``source`` to ``target``; [] if unreachable."""
        if source not in self._adj or target not in self._adj:
            return []
        dist, prev = self.dijkstra(source)
        if target not in dist:
            return []
        path = [target]
        while path[-1] != source:
            path.append(prev[path[-1]])
        return path[::-1]

    def minimum_spanning_tree(self) -> tuple[float, list[Edge]]:
        """Kruskal's algorithm: take edges cheapest-first, skip any that would form a
        cycle (both ends already in the same union-find set).

        Returns ``(total_weight, edges)``. On a disconnected graph this is a minimum
        spanning forest.
        """
        uf = UnionFind(self._adj)
        total = 0.0
        chosen: list[Edge] = []
        for w, u, v in sorted(self.edges()):
            if uf.union(u, v):
                total += w
                chosen.append((w, u, v))
                if len(chosen) == len(self._adj) - 1:
                    break
        return total, chosen
