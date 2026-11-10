"""Directed weighted graph: topological sort, strongly connected components and
maximum flow.

Complexity (V vertices, E edges):
    topological_sort (Kahn) O(V + E) plus O(V log V) for the sorted ready queue;
    strongly_connected_components (Tarjan) O(V + E);
    max_flow (Edmonds-Karp) O(V * E^2); space O(V + E).
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from typing import Any

from dsa.heap import MinHeap

Vertex = Any  # hashable and comparable with `<`


class CycleError(ValueError):
    """Raised by topological_sort when the graph has a cycle."""


class DirectedGraph:
    def __init__(self) -> None:
        self._adj: dict[Vertex, dict[Vertex, float]] = {}

    def add_vertex(self, v: Vertex) -> None:
        self._adj.setdefault(v, {})

    def add_edge(self, u: Vertex, v: Vertex, weight: float = 1.0) -> None:
        """Add edge u -> v. For max_flow the weight is the edge's capacity."""
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight

    def vertices(self) -> list[Vertex]:
        return sorted(self._adj)

    def successors(self, v: Vertex) -> list[Vertex]:
        return sorted(self._adj[v])

    def __len__(self) -> int:
        return len(self._adj)

    def topological_sort(self) -> list[Vertex]:
        """Kahn's algorithm: repeatedly output a vertex with no remaining incoming
        edges. If some vertices are never freed, they sit on a cycle.

        A min-heap is used as the ready queue so ties break by smallest vertex,
        which makes the order deterministic.

        Raises:
            CycleError: if the graph is not a DAG.
        """
        indegree = {v: 0 for v in self._adj}
        for u in self._adj:
            for v in self._adj[u]:
                indegree[v] += 1
        ready = MinHeap.heapify(v for v, d in indegree.items() if d == 0)
        order: list[Vertex] = []
        while ready:
            u = ready.pop()
            order.append(u)
            for v in self._adj[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    ready.push(v)
        if len(order) != len(self._adj):
            raise CycleError("graph has a cycle; no topological order exists")
        return order

    def strongly_connected_components(self) -> list[list[Vertex]]:
        """Tarjan's algorithm, written iteratively so deep graphs cannot overflow
        Python's recursion limit.

        One DFS assigns each vertex a discovery index and a low-link: the smallest
        index reachable from its DFS subtree using at most one back edge to a vertex
        still on the stack. A vertex whose low-link equals its own index is the root
        of an SCC, and that SCC is everything above it on the stack.

        Each component is sorted and the list of components is sorted, so the
        result is deterministic.
        """
        index: dict[Vertex, int] = {}
        low: dict[Vertex, int] = {}
        on_stack: set[Vertex] = set()
        stack: list[Vertex] = []
        components: list[list[Vertex]] = []
        counter = 0
        # Explicit call stack. Each frame is (vertex, iterator over its
        # successors): the iterator remembers where we were, which a recursive
        # call would do for us.
        work: list[tuple[Vertex, Iterator[Vertex]]] = []

        def visit(v: Vertex) -> None:
            nonlocal counter
            index[v] = low[v] = counter
            counter += 1
            stack.append(v)
            on_stack.add(v)
            work.append((v, iter(self.successors(v))))

        for root in self.vertices():
            if root in index:
                continue
            visit(root)
            while work:
                v, successors = work[-1]
                w = next(successors, None)
                if w is not None:
                    if w not in index:
                        visit(w)  # "recurse" into w
                    elif w in on_stack:
                        low[v] = min(low[v], index[w])
                    continue
                # All successors of v done: "return" from v.
                work.pop()
                if work:
                    parent = work[-1][0]
                    low[parent] = min(low[parent], low[v])
                if low[v] == index[v]:
                    component: list[Vertex] = []
                    while True:
                        x = stack.pop()
                        on_stack.discard(x)
                        component.append(x)
                        if x == v:
                            break
                    components.append(sorted(component))
        return sorted(components)

    def max_flow(self, source: Vertex, sink: Vertex) -> float:
        """Maximum source-to-sink flow, treating edge weights as capacities.

        Edmonds-Karp: Ford-Fulkerson where each augmenting path is found with BFS
        (fewest edges). Using shortest paths bounds the number of augmentations at
        O(V * E), giving O(V * E^2) overall regardless of capacity values.

        The residual graph holds remaining capacity on each edge plus a reverse
        edge carrying the flow already sent, which lets later paths "undo" an
        earlier poor choice.
        """
        if source == sink:
            raise ValueError("source and sink must differ")
        residual: dict[Vertex, dict[Vertex, float]] = {v: {} for v in self._adj}
        for u in self._adj:
            for v, cap in self._adj[u].items():
                residual[u][v] = residual[u].get(v, 0.0) + cap
                residual[v].setdefault(u, 0.0)
        if source not in residual or sink not in residual:
            return 0.0

        total = 0.0
        while True:
            # BFS for the shortest augmenting path in the residual graph.
            parent: dict[Vertex, Vertex] = {source: source}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for v, cap in residual[u].items():
                    if cap > 0 and v not in parent:
                        parent[v] = u
                        queue.append(v)
            if sink not in parent:
                return total
            # Bottleneck = smallest residual capacity along the path.
            bottleneck = float("inf")
            v = sink
            while v != source:
                u = parent[v]
                bottleneck = min(bottleneck, residual[u][v])
                v = u
            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= bottleneck
                residual[v][u] += bottleneck
                v = u
            total += bottleneck
