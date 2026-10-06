import imagehash


def print_as_matrix(matrix: list) -> None:
    for row in matrix:
        print(*row)


def hamming_dist(x: imagehash.ImageHash, y: imagehash.ImageHash) -> int:
    return int(x - y)


def build_hash_matrix(hashes: list) -> list:
    n = len(hashes)

    matr = [[1] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            matr[i][j] = hamming_dist(hashes[i], hashes[j])

    return matr
