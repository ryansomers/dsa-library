package dsa;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;

/**
 * Hash map with separate chaining. Bucket index is {@code Math.floorMod(hashCode, capacity)}
 * (floorMod, unlike %, never goes negative for negative hash codes). The table doubles when
 * size/capacity exceeds 0.75. Null keys are allowed (they hash to 0).
 *
 * <p>put/get/remove/containsKey O(1) average, O(n) worst case; space O(n + capacity).
 */
public final class HashMap<K, V> {
    private static final double MAX_LOAD = 0.75;

    private static final class Entry<K, V> {
        final K key;
        V value;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    private LinkedList<Entry<K, V>>[] buckets;
    private int size;

    public HashMap() {
        this(8);
    }

    public HashMap(int capacity) {
        if (capacity < 1) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        buckets = newBuckets(capacity);
    }

    // Java cannot create a generic array directly; the cast is safe because the array never
    // escapes this class and only ever holds LinkedList<Entry<K, V>>.
    @SuppressWarnings("unchecked")
    private static <K, V> LinkedList<Entry<K, V>>[] newBuckets(int capacity) {
        LinkedList<Entry<K, V>>[] b = (LinkedList<Entry<K, V>>[]) new LinkedList<?>[capacity];
        for (int i = 0; i < capacity; i++) {
            b[i] = new LinkedList<>();
        }
        return b;
    }

    private static int indexFor(Object key, int capacity) {
        return Math.floorMod(Objects.hashCode(key), capacity);
    }

    private Entry<K, V> find(Object key) {
        for (Entry<K, V> e : buckets[indexFor(key, buckets.length)]) {
            if (Objects.equals(e.key, key)) { // null-safe equality
                return e;
            }
        }
        return null;
    }

    public void put(K key, V value) {
        Entry<K, V> e = find(key);
        if (e != null) {
            e.value = value;
            return;
        }
        buckets[indexFor(key, buckets.length)].add(new Entry<>(key, value));
        size++;
        if ((double) size / buckets.length > MAX_LOAD) {
            resize(2 * buckets.length);
        }
    }

    /** Value for {@code key}, or null if absent. */
    public V get(K key) {
        return getOrDefault(key, null);
    }

    public V getOrDefault(K key, V defaultValue) {
        Entry<K, V> e = find(key);
        return e == null ? defaultValue : e.value;
    }

    /** Removes {@code key} and returns its value; throws NoSuchElementException if absent. */
    public V remove(K key) {
        var it = buckets[indexFor(key, buckets.length)].iterator();
        while (it.hasNext()) {
            Entry<K, V> e = it.next();
            if (Objects.equals(e.key, key)) {
                it.remove();
                size--;
                return e.value;
            }
        }
        throw new NoSuchElementException("key not found: " + key);
    }

    public boolean containsKey(K key) {
        return find(key) != null;
    }

    public List<K> keys() {
        List<K> out = new ArrayList<>(size);
        for (LinkedList<Entry<K, V>> bucket : buckets) {
            for (Entry<K, V> e : bucket) {
                out.add(e.key);
            }
        }
        return out;
    }

    public int size() {
        return size;
    }

    public int capacity() {
        return buckets.length;
    }

    private void resize(int newCapacity) {
        LinkedList<Entry<K, V>>[] fresh = newBuckets(newCapacity);
        for (LinkedList<Entry<K, V>> bucket : buckets) {
            for (Entry<K, V> e : bucket) {
                fresh[indexFor(e.key, newCapacity)].add(e);
            }
        }
        buckets = fresh;
    }
}
