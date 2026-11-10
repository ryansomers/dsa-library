from dsa.trie import Trie


def test_search_vs_prefix():
    t = Trie(["apple", "app", "apt", "bat"])
    assert t.search("app") and t.search("apple")
    assert not t.search("ap")
    assert t.starts_with("ap") and not t.starts_with("c")


def test_words_with_prefix_sorted():
    t = Trie(["apple", "app", "apt", "bat"])
    assert t.words_with_prefix("ap") == ["app", "apple", "apt"]
    assert t.words_with_prefix("z") == []
    assert t.words_with_prefix("") == ["app", "apple", "apt", "bat"]


def test_len_ignores_duplicates_and_empty_string():
    t = Trie(["a", "a"])
    assert len(t) == 1
    t.insert("")
    assert t.search("") and len(t) == 2
