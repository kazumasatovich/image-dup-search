def similarity_relation_matrix(matrix: list, r: int) -> list:
    n = len(matrix)
    relation_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] <= r:
                relation_matrix[i][j] = 1

    return relation_matrix


def print_relation_matrix(matrix: list, angles: list) -> None:
    n = len(matrix)
    row_lable = "   "

    for angle in angles:
        row_lable += str(angle).ljust(2)
    # Будет необходимо адаптировать вывод матрицы к трехзначным углам

    print(row_lable)

    for i in range(n):
        print(str(angles[i]).ljust(2), *matrix[i])
