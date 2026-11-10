package dsa;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Test;

class MinHeapTest {
    private static <T extends Comparable<T>> List<T> drain(MinHeap<T> h) {
        List<T> out = new ArrayList<>();
        while (!h.isEmpty()) {
            out.add(h.pop());
        }
        return out;
    }

    @Test
    void pushPopReturnsSortedOrder() {
        MinHeap<Integer> h = new MinHeap<>();
        for (int x : new int[] {5, 3, 8, 1, 9, 2}) {
            h.push(x);
        }
        assertEquals(List.of(1, 2, 3, 5, 8, 9), drain(h));
    }

    @Test
    void popEmptyThrows() {
        assertThrows(NoSuchElementException.class, () -> new MinHeap<Integer>().pop());
    }

    @Test
    void peekDoesNotRemove() {
        MinHeap<Integer> h = MinHeap.heapify(List.of(4, 2, 7));
        assertEquals(2, h.peek());
        assertEquals(3, h.size());
    }

    @Test
    void heapifyBuildsValidHeap() {
        assertEquals(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9),
                drain(MinHeap.heapify(List.of(9, 8, 7, 6, 5, 4, 3, 2, 1))));
    }

    @Test
    void duplicatesAreKept() {
        assertEquals(List.of(1, 1, 2, 2), drain(MinHeap.heapify(List.of(2, 1, 2, 1))));
    }

    @Test
    void randomInputPopsSorted() {
        Random rng = new Random(42);
        List<Integer> xs = new ArrayList<>();
        MinHeap<Integer> h = new MinHeap<>();
        for (int i = 0; i < 1000; i++) {
            int x = rng.nextInt(100);
            xs.add(x);
            h.push(x);
        }
        xs.sort(null);
        assertEquals(xs, drain(h));
    }
}
