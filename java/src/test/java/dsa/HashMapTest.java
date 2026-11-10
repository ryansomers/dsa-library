package dsa;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Test;

class HashMapTest {
    @Test
    void putGetAndOverwrite() {
        HashMap<String, Integer> m = new HashMap<>();
        m.put("a", 1);
        m.put("b", 2);
        m.put("a", 10);
        assertEquals(10, m.get("a"));
        assertEquals(2, m.get("b"));
        assertEquals(2, m.size());
    }

    @Test
    void getMissingReturnsDefault() {
        HashMap<String, Integer> m = new HashMap<>();
        assertNull(m.get("x"));
        assertEquals(-1, m.getOrDefault("x", -1));
    }

    @Test
    void removeReturnsValueAndMissingThrows() {
        HashMap<String, Integer> m = new HashMap<>();
        m.put("a", 1);
        assertEquals(1, m.remove("a"));
        assertFalse(m.containsKey("a"));
        assertEquals(0, m.size());
        assertThrows(NoSuchElementException.class, () -> m.remove("a"));
    }

    @Test
    void resizesPastLoadFactorAndKeepsAllKeys() {
        HashMap<Integer, Integer> m = new HashMap<>(4);
        for (int i = 0; i < 100; i++) {
            m.put(i, i * i);
        }
        assertTrue(m.capacity() >= 128);
        assertTrue((double) m.size() / m.capacity() <= 0.75);
        for (int i = 0; i < 100; i++) {
            assertEquals(i * i, m.get(i));
        }
        List<Integer> keys = new ArrayList<>(m.keys());
        keys.sort(null);
        assertEquals(100, keys.size());
        assertEquals(0, keys.get(0));
        assertEquals(99, keys.get(99));
    }

    @Test
    void negativeHashCodesAndCollisions() {
        // "Aa" and "BB" have the same hashCode (2112); Integer.MIN_VALUE hashes negative.
        HashMap<Object, String> m = new HashMap<>();
        m.put("Aa", "first");
        m.put("BB", "second");
        m.put(Integer.MIN_VALUE, "min");
        assertEquals("first", m.get("Aa"));
        assertEquals("second", m.get("BB"));
        assertEquals("min", m.get(Integer.MIN_VALUE));
        m.remove("Aa");
        assertEquals("second", m.get("BB"));
    }

    @Test
    void nullKeyIsSupported() {
        HashMap<String, Integer> m = new HashMap<>();
        m.put(null, 7);
        assertTrue(m.containsKey(null));
        assertEquals(7, m.get(null));
        assertEquals(7, m.remove(null));
    }

    @Test
    void matchesJavaUtilHashMapOnRandomOps() {
        Random rng = new Random(7);
        HashMap<Integer, Integer> m = new HashMap<>(1);
        java.util.HashMap<Integer, Integer> model = new java.util.HashMap<>();
        for (int i = 0; i < 5000; i++) {
            int k = rng.nextInt(50) - 25;
            int v = rng.nextInt();
            switch (rng.nextInt(3)) {
                case 0 -> {
                    m.put(k, v);
                    model.put(k, v);
                }
                case 1 -> {
                    if (model.containsKey(k)) {
                        assertEquals(model.remove(k), m.remove(k));
                    } else {
                        assertFalse(m.containsKey(k));
                    }
                }
                default -> assertEquals(model.get(k), m.get(k));
            }
            assertEquals(model.size(), m.size());
        }
    }
}
