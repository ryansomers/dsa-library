package dsa;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Undirected weighted graph over integer vertices, stored as an adjacency list. Neighbors are
 * visited in ascending order so traversals are deterministic (same as the Python version).
 *
 * <p>BFS O(V + E log d) with the per-vertex sort; Dijkstra O((V + E) log V); space O(V + E).
 */
public final class Graph {
    /** One directed half of an undirected edge, as stored in the adjacency list. */
    public record Edge(int to, double weight) {}

    /** Heap entry ordered by distance, then vertex. */
    private record Entry(double dist, int vertex) implements Comparable<Entry> {
        @Override
        public int compareTo(Entry o) {
            int c = Double.compare(dist, o.dist);
            return c != 0 ? c : Integer.compare(vertex, o.vertex);
        }
    }

    // Each neighbor list is kept sorted by vertex id on insert.
    private final Map<Integer, List<Edge>> adj = new TreeMap<>();

    public void addVertex(int v) {
        adj.computeIfAbsent(v, k -> new ArrayList<>());
    }

    public void addEdge(int u, int v, double weight) {
        if (weight < 0) {
            throw new IllegalArgumentException("negative weights are not supported");
        }
        addVertex(u);
        addVertex(v);
        link(u, v, weight);
        link(v, u, weight);
    }

    /** Adds or overwrites u -> v, keeping u's list sorted (re-adding an edge updates it). */
    private void link(int u, int v, double weight) {
        List<Edge> list = adj.get(u);
        list.removeIf(e -> e.to() == v);
        list.add(new Edge(v, weight));
        list.sort(Comparator.comparingInt(Edge::to));
    }

    public List<Edge> neighbors(int v) {
        return Collections.unmodifiableList(adj.getOrDefault(v, List.of()));
    }

    public List<Integer> bfs(int start) {
        List<Integer> order = new ArrayList<>();
        Set<Integer> seen = new HashSet<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        seen.add(start);
        queue.add(start);
        while (!queue.isEmpty()) {
            int u = queue.poll();
            order.add(u);
            for (Edge e : neighbors(u)) {
                if (seen.add(e.to())) { // add() returns false if already seen
                    queue.add(e.to());
                }
            }
        }
        return order;
    }

    /**
     * Shortest distances from {@code source} to every reachable vertex. Uses this library's
     * MinHeap with lazy deletion: improved distances are pushed again and stale entries are
     * skipped when popped.
     */
    public Map<Integer, Double> dijkstra(int source) {
        Map<Integer, Double> dist = new TreeMap<>();
        dist.put(source, 0.0);
        MinHeap<Entry> heap = new MinHeap<>();
        heap.push(new Entry(0.0, source));
        while (!heap.isEmpty()) {
            Entry cur = heap.pop();
            if (cur.dist() > dist.get(cur.vertex())) {
                continue; // stale entry
            }
            for (Edge e : neighbors(cur.vertex())) {
                double nd = cur.dist() + e.weight();
                Double known = dist.get(e.to());
                if (known == null || nd < known) {
                    dist.put(e.to(), nd);
                    heap.push(new Entry(nd, e.to()));
                }
            }
        }
        return dist;
    }
}
