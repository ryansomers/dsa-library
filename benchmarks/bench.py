"""Time key operations across input sizes and plot them against their Big-O curve.

For each operation we time a batch of work at several sizes n (best of REPEATS
runs, to filter out scheduler noise), then fit a single constant c so that
c * f(n) best matches the measurements (least squares through the origin).
If the implementation really is O(f(n)), the dots should hug the dashed curve.

Run:  python benchmarks/bench.py        (writes benchmarks/plots/*.png and results.md)
"""

from __future__ import annotations

import math
import random
import string
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt  # noqa: E402

from dsa.avl_tree import AVLTree  # noqa: E402
from dsa.dp import edit_distance, longest_increasing_subsequence  # noqa: E402
from dsa.graph import Graph  # noqa: E402
from dsa.hash_map import HashMap  # noqa: E402
from dsa.heap import MinHeap  # noqa: E402
from dsa.lru_cache import LRUCache  # noqa: E402
from dsa.trie import Trie  # noqa: E402

OUT = Path(__file__).parent / "plots"
REPEATS = 3
SEED = 42

# Colors from a CVD-checked reference palette: one series color plus neutral ink.
MEASURED = "#2a78d6"
EXPECTED = "#52514e"
SURFACE = "#fcfcfb"


@dataclass
class Bench:
    name: str  # also the PNG file stem
    title: str
    complexity: str  # label for the expected curve
    curve: Callable[[int], float]
    setup: Callable[[int], object]  # builds input outside the timed region
    run: Callable[[object], object]
    sizes: list[int]


def nlogn(n: int) -> float:
    return n * math.log2(max(n, 2))


def rand_ints(n: int) -> list[int]:
    rng = random.Random(SEED + n)
    return [rng.randrange(10 * n) for _ in range(n)]


def heap_push_pop(xs: object) -> None:
    h: MinHeap[int] = MinHeap()
    for x in xs:
        h.push(x)
    while h:
        h.pop()


def hash_put_get(xs: object) -> None:
    m: HashMap[int, int] = HashMap()
    for x in xs:
        m.put(x, x)
    for x in xs:
        m.get(x)


def lru_ops(xs: object) -> None:
    cache: LRUCache[int, int] = LRUCache(capacity=max(1, len(xs) // 4))
    for x in xs:
        if cache.get(x) is None:
            cache.put(x, x)


def random_graph(n: int) -> Graph:
    """Connected sparse graph: a random spanning path plus 3n random edges (E ~ 4V)."""
    rng = random.Random(SEED + n)
    g = Graph()
    order = list(range(n))
    rng.shuffle(order)
    for a, b in zip(order, order[1:], strict=False):
        g.add_edge(a, b, rng.randint(1, 100))
    for _ in range(3 * n):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            g.add_edge(u, v, rng.randint(1, 100))
    return g


def random_words(n: int) -> list[str]:
    rng = random.Random(SEED + n)
    return ["".join(rng.choices(string.ascii_lowercase[:8], k=8)) for _ in range(n)]


def random_string_pair(n: int) -> tuple[str, str]:
    rng = random.Random(SEED + n)
    return "".join(rng.choices("acgt", k=n)), "".join(rng.choices("acgt", k=n))


LINEAR_SIZES = [2_000, 4_000, 8_000, 16_000, 32_000, 64_000]
GRAPH_SIZES = [1_000, 2_000, 4_000, 8_000, 16_000]

BENCHES = [
    Bench("heap_push_pop", "MinHeap: n pushes + n pops", "c·n log n", nlogn,
          rand_ints, heap_push_pop, LINEAR_SIZES),
    Bench("heap_heapify", "MinHeap.heapify of n items", "c·n", float,
          rand_ints, MinHeap.heapify, LINEAR_SIZES),
    Bench("hash_map_put_get", "HashMap: n puts + n gets", "c·n", float,
          rand_ints, hash_put_get, LINEAR_SIZES),
    Bench("avl_insert", "AVLTree: n random inserts", "c·n log n", nlogn,
          rand_ints, AVLTree, LINEAR_SIZES),
    Bench("lru_cache_ops", "LRUCache: n get/put pairs", "c·n", float,
          rand_ints, lru_ops, LINEAR_SIZES),
    Bench("trie_insert", "Trie: insert n 8-letter words", "c·n", float,
          random_words, Trie, LINEAR_SIZES),
    Bench("dijkstra", "Dijkstra, V = n, E ~ 4n", "c·(V+E) log V",
          lambda n: 5 * n * math.log2(n), random_graph,
          lambda g: g.dijkstra(0), GRAPH_SIZES),
    Bench("kruskal_mst", "Kruskal MST, V = n, E ~ 4n", "c·E log E",
          lambda n: 4 * n * math.log2(4 * n), random_graph,
          lambda g: g.minimum_spanning_tree(), GRAPH_SIZES),
    Bench("lis", "Longest increasing subsequence", "c·n log n", nlogn,
          rand_ints, longest_increasing_subsequence, LINEAR_SIZES),
    Bench("edit_distance", "Edit distance, two length-n strings", "c·n²",
          lambda n: float(n * n), random_string_pair,
          lambda p: edit_distance(*p), [100, 200, 400, 600, 800, 1000]),
]


def time_it(bench: Bench, n: int) -> float:
    data = bench.setup(n)
    best = math.inf
    for _ in range(REPEATS):
        start = time.perf_counter()
        bench.run(data)
        best = min(best, time.perf_counter() - start)
    return best


def fit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Least-squares c for y = c * x, plus R^2 of that fit."""
    c = sum(x * y for x, y in zip(xs, ys, strict=True)) / sum(x * x for x in xs)
    mean = sum(ys) / len(ys)
    ss_res = sum((y - c * x) ** 2 for x, y in zip(xs, ys, strict=True))
    ss_tot = sum((y - mean) ** 2 for y in ys)
    return c, 1 - ss_res / ss_tot if ss_tot else 1.0


def plot(bench: Bench, ns: list[int], ts: list[float], c: float, r2: float) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    dense = [ns[0] + (ns[-1] - ns[0]) * i / 100 for i in range(101)]
    ax.plot(dense, [1000 * c * bench.curve(int(n)) for n in dense], "--",
            color=EXPECTED, linewidth=2, label=f"expected {bench.complexity} (fitted)")
    ax.plot(ns, [1000 * t for t in ts], "o", color=MEASURED, markersize=8,
            markeredgecolor=SURFACE, markeredgewidth=2, label="measured (best of 3)")
    ax.set_title(f"{bench.title}\nR² = {r2:.3f}", fontsize=11, color="#0b0b0b")
    ax.set_xlabel("n")
    ax.set_ylabel("time (ms)")
    ax.grid(True, color="#e4e3df", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f"{bench.name}.png", facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = ["| operation | expected | largest n | time at largest n (ms) | R² |",
            "|---|---|---|---|---|"]
    for bench in BENCHES:
        ts = [time_it(bench, n) for n in bench.sizes]
        c, r2 = fit([bench.curve(n) for n in bench.sizes], ts)
        plot(bench, bench.sizes, ts, c, r2)
        rows.append(f"| {bench.title} | {bench.complexity} | {bench.sizes[-1]:,} | "
                    f"{1000 * ts[-1]:.1f} | {r2:.3f} |")
        print(rows[-1], flush=True)
    (Path(__file__).parent / "results.md").write_text(
        "# Benchmark results\n\nGenerated by `python benchmarks/bench.py`. R² is how well "
        "a single fitted constant times the expected curve explains the measured times.\n\n"
        + "\n".join(rows) + "\n"
    )


if __name__ == "__main__":
    main()
