import imagehash


def print_as_matrix(matrix: list) -> None:
    for row in matrix:
        print(*row)


def hamming_dist(x: imagehash.ImageHash, y: imagehash.ImageHash) -> int:
    return int(x - y)


def build_matrix(hashes: list) -> list:
    n = len(hashes)

    matr = [[hamming_dist(hashes[i], hashes[j])] for i in range(n) for j in range(n)]

    return matr
