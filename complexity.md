# Complexity reference

n = number of items, V = vertices, E = edges, d = max vertex degree, L = string length.
"Amortized" means averaged over a sequence of operations; "average" assumes a good hash.

| Structure / algorithm | Operation | Time | Space |
|---|---|---|---|
| MinHeap | push | O(log n) | O(1) extra |
| MinHeap | pop | O(log n) | O(1) extra |
| MinHeap | peek | O(1) | O(1) |
| MinHeap | heapify | O(n) | O(n) |
| HashMap | put | O(1) average, amortized over resizes; O(n) worst | O(n + capacity) total |
| HashMap | get / contains | O(1) average; O(n) worst | O(1) extra |
| HashMap | remove | O(1) average; O(n) worst | O(1) extra |
| HashMap | keys | O(n + capacity) | O(n) |
| AVLTree | insert | O(log n) | O(log n) recursion |
| AVLTree | delete | O(log n) | O(log n) recursion |
| AVLTree | contains | O(log n) | O(1) |
| AVLTree | inorder | O(n) | O(n) output, O(log n) stack |
| AVLTree | height | O(1) | O(1) |
| AVLTree | is_balanced | O(n) | O(log n) recursion |
| UnionFind | find / union / connected | O(α(n)) amortized | O(n) total |
| Trie | insert / search / starts_with | O(L) | O(L) new nodes for insert |
| Trie | words_with_prefix | O(L + M + k log k) for k matches with M total characters | O(M) |
| LRUCache | get / put | O(1) average | O(capacity) total |
| Graph | add_edge | O(1) average | O(1) |
| Graph | bfs / dfs | O(V + E log d) with sorted neighbors (O(V + E) unsorted) | O(V) |
| Graph | dijkstra | O((V + E) log V) | O(V + E) heap with stale entries |
| Graph | shortest_path | O((V + E) log V) | O(V) |
| Graph | minimum_spanning_tree (Kruskal) | O(E log E) | O(V + E) |
| DirectedGraph | topological_sort (Kahn) | O(V log V + E) with heap tie-breaking | O(V) |
| DirectedGraph | strongly_connected_components (Tarjan) | O(V + E log d) with sorted successors | O(V) |
| DirectedGraph | max_flow (Edmonds-Karp) | O(V E²) | O(V + E) |
| dp | fibonacci | O(n) | O(1) |
| dp | coin_change | O(amount · coins) | O(amount) |
| dp | knapsack_01 | O(n · capacity) | O(capacity) |
| dp | longest_common_subsequence | O(len(a) · len(b)) | O(len(b)) |
| dp | edit_distance | O(len(a) · len(b)) | O(len(b)) |
| dp | longest_increasing_subsequence | O(n log n) | O(n) |
