package dsa;

import java.util.ArrayList;
import java.util.Collection;
import java.util.NoSuchElementException;

/**
 * Binary min-heap stored in an {@link ArrayList}. Children of index i are at 2i+1 and 2i+2.
 *
 * <p>push O(log n), pop O(log n), peek O(1), heapify O(n), space O(n).
 */
public final class MinHeap<T extends Comparable<T>> {
    private final ArrayList<T> data = new ArrayList<>();

    /** Builds a heap from {@code items} in O(n) by sifting down internal nodes n/2-1..0. */
    public static <T extends Comparable<T>> MinHeap<T> heapify(Collection<? extends T> items) {
        MinHeap<T> heap = new MinHeap<>();
        heap.data.addAll(items);
        for (int i = heap.data.size() / 2 - 1; i >= 0; i--) {
            heap.siftDown(i);
        }
        return heap;
    }

    public void push(T item) {
        data.add(item);
        siftUp(data.size() - 1);
    }

    /** Removes and returns the smallest item; throws NoSuchElementException if empty. */
    public T pop() {
        if (data.isEmpty()) {
            throw new NoSuchElementException("pop from empty heap");
        }
        int last = data.size() - 1;
        swap(0, last);
        T smallest = data.remove(last);
        if (!data.isEmpty()) {
            siftDown(0);
        }
        return smallest;
    }

    public T peek() {
        if (data.isEmpty()) {
            throw new NoSuchElementException("peek from empty heap");
        }
        return data.get(0);
    }

    public int size() {
        return data.size();
    }

    public boolean isEmpty() {
        return data.isEmpty();
    }

    private boolean less(int i, int j) {
        return data.get(i).compareTo(data.get(j)) < 0;
    }

    private void swap(int i, int j) {
        T tmp = data.get(i);
        data.set(i, data.get(j));
        data.set(j, tmp);
    }

    private void siftUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (!less(i, parent)) {
                return;
            }
            swap(i, parent);
            i = parent;
        }
    }

    private void siftDown(int i) {
        int n = data.size();
        while (true) {
            int left = 2 * i + 1;
            int right = left + 1;
            int smallest = i;
            if (left < n && less(left, smallest)) {
                smallest = left;
            }
            if (right < n && less(right, smallest)) {
                smallest = right;
            }
            if (smallest == i) {
                return;
            }
            swap(i, smallest);
            i = smallest;
        }
    }
}
