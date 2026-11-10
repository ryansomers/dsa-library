"""Prefix tree (trie) for strings.

Each node maps a character to a child node; a flag marks nodes where a word ends.
Complexity (L = word/prefix length, k = number of matching words, M = total
characters in those words): insert/search/starts_with O(L);
words_with_prefix O(L + M + k log k) including the final sort; space O(total characters).
"""

from __future__ import annotations


class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self, words: list[str] | None = None) -> None:
        self._root = _TrieNode()
        self._size = 0
        for w in words or []:
            self.insert(w)

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        if not node.is_word:
            node.is_word = True
            self._size += 1

    def _walk(self, prefix: str) -> _TrieNode | None:
        node = self._root
        for ch in prefix:
            nxt = node.children.get(ch)
            if nxt is None:
                return None
            node = nxt
        return node

    def search(self, word: str) -> bool:
        """True if ``word`` was inserted as a whole word."""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """True if any inserted word begins with ``prefix``."""
        return self._walk(prefix) is not None

    def words_with_prefix(self, prefix: str) -> list[str]:
        """All inserted words beginning with ``prefix``, sorted."""
        start = self._walk(prefix)
        if start is None:
            return []
        out: list[str] = []
        stack: list[tuple[_TrieNode, str]] = [(start, prefix)]
        while stack:
            node, word = stack.pop()
            if node.is_word:
                out.append(word)
            for ch, child in node.children.items():
                stack.append((child, word + ch))
        return sorted(out)

    def __len__(self) -> int:
        return self._size
