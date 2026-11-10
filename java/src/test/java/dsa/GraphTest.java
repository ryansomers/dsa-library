package dsa;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** Same graph as tests/test_graph.py, with A..F mapped to 0..5 and Z to 9. */
class GraphTest {
    private Graph g;

    @BeforeEach
    void build() {
        //   0 --1-- 1 --2-- 2
        //   |       |       |
        //   4       5       1
        //   |       |       |
        //   3 --3-- 4 --1-- 5      plus isolated vertex 9
        g = new Graph();
        int[][] edges = {{0, 1, 1}, {1, 2, 2}, {0, 3, 4}, {1, 4, 5}, {2, 5, 1}, {3, 4, 3}, {4, 5, 1}};
        for (int[] e : edges) {
            g.addEdge(e[0], e[1], e[2]);
        }
        g.addVertex(9);
    }

    @Test
    void bfsOrder() {
        assertEquals(List.of(0, 1, 3, 2, 4, 5), g.bfs(0));
    }

    @Test
    void dijkstraDistances() {
        assertEquals(Map.of(0, 0.0, 1, 1.0, 2, 3.0, 3, 4.0, 4, 5.0, 5, 4.0), g.dijkstra(0));
    }

    @Test
    void unreachableVertexHasNoDistance() {
        assertFalse(g.dijkstra(0).containsKey(9));
        assertEquals(List.of(9), g.bfs(9));
    }

    @Test
    void readdingEdgeOverwritesWeight() {
        g.addEdge(0, 4, 2);
        g.addEdge(0, 4, 1);
        assertEquals(1.0, g.dijkstra(0).get(4));
        assertEquals(3, g.neighbors(0).size());
    }

    @Test
    void negativeWeightRejected() {
        assertThrows(IllegalArgumentException.class, () -> g.addEdge(0, 1, -1));
    }
}
