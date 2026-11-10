import pytest

from dsa.avl_tree import AVLTree


@pytest.mark.parametrize(
    "order, case",
    [([3, 2, 1], "LL"), ([1, 2, 3], "RR"), ([3, 1, 2], "LR"), ([1, 3, 2], "RL")],
)
def test_each_rotation_case_yields_root_2_height_2(order, case):
    t = AVLTree(order)
    assert t.root is not None and t.root.key == 2, case
    assert t.height() == 2, case
    assert t.is_balanced()


def test_sorted_inserts_stay_logarithmic():
    t = AVLTree(range(1000))
    assert t.inorder() == list(range(1000))
    assert t.height() <= 15  # AVL bound: levels < 1.44 * log2(n + 2) ~ 14.4
    assert t.is_balanced()


def test_duplicates_ignored():
    t = AVLTree([5, 5, 5])
    assert len(t) == 1
    assert t.insert(5) is False


def test_contains():
    t = AVLTree([10, 20, 5])
    assert 10 in t and t.contains(5)
    assert not t.contains(7)


def test_delete_leaf_one_child_two_children():
    t = AVLTree([50, 30, 70, 20, 40, 60, 80, 35])
    assert t.delete(20)  # leaf
    assert t.delete(40)  # one child (35)
    assert t.delete(50)  # two children: successor 60 moves up
    assert t.inorder() == [30, 35, 60, 70, 80]
    assert len(t) == 5
    assert t.is_balanced()


def test_delete_missing_returns_false():
    t = AVLTree([1, 2, 3])
    assert t.delete(9) is False
    assert len(t) == 3


def test_delete_triggers_rebalance():
    t = AVLTree([2, 1, 3, 4])
    t.delete(1)  # root 2 becomes right-heavy by 2 -> rotate left
    assert t.root is not None and t.root.key == 3
    assert t.is_balanced()


def test_empty_tree():
    t: AVLTree[int] = AVLTree()
    assert t.height() == 0 and len(t) == 0 and t.inorder() == []
