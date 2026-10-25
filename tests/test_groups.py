from collections import Counter

from dup_search.groups import groups_search
from dup_search.similarity_relation import similarity_relation_matrix

DIST_GROUPS_CHAIN_OF_NUMBERS = [
    [0, 4, 12, 16, 20, 22],
    [4, 0, 8, 12, 16, 18],
    [12, 8, 0, 4, 8, 12],
    [16, 12, 4, 0, 6, 10],
    [20, 16, 8, 6, 0, 6],
    [22, 18, 12, 10, 6, 0],
]

DIST_GROUPS_WITH_SCATTERED_NUMBERS = [
    [0, 14, 4, 14, 20, 22],
    [14, 0, 14, 6, 6, 6],
    [4, 14, 0, 14, 14, 12],
    [14, 6, 14, 0, 6, 6],
    [20, 6, 14, 6, 0, 6],
    [22, 6, 12, 6, 6, 0],
]


def compare_partitions(list1: list, list2: list) -> bool:
    set1 = Counter(frozenset(group) for group in list1)
    set2 = Counter(frozenset(group) for group in list2)

    return set1 == set2


def test_groups_search_r_6_gives_correct_groups_set_in_order() -> None:
    assert compare_partitions(
        groups_search(similarity_relation_matrix(DIST_GROUPS_CHAIN_OF_NUMBERS, 6)),
        [[0, 1], [2, 3, 4, 5]],
    )


def test_groups_search_r_6_gives_correct_groups_set_not_in_order() -> None:
    assert compare_partitions(
        groups_search(
            similarity_relation_matrix(DIST_GROUPS_WITH_SCATTERED_NUMBERS, 6)
        ),
        [[0, 2], [1, 3, 4, 5]],
    )
