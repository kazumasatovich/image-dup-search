import imagehash
import pytest

from dup_search.matrix import build_matrix


@pytest.fixture
def matrix() -> list:
    a = imagehash.hex_to_hash("ffffffffffffffff")
    b = imagehash.hex_to_hash("1239181932895171")
    c = imagehash.hex_to_hash("12391819ffffffff")
    return build_matrix([a, b, c])


def test_diagonal_is_zero(matrix: list) -> None:
    for i in range(len(matrix)):
        assert matrix[i][i] == 0


def test_matrix_is_symmetric(matrix: list) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            assert matrix[i][j] == matrix[j][i]
