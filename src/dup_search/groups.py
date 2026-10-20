def groups_search(matrix: list) -> list:
    n = len(matrix)
    groups = []
    visited = [False] * n

    def dfs(vertex: int, current_group: list) -> None:
        visited[vertex] = True
        current_group.append(vertex)

        for neighbor in range(n):
            if matrix[vertex][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, current_group)

    for i in range(n):
        if not visited[i]:
            new_group: list[int] = []
            dfs(i, new_group)
            groups.append(new_group)

    return groups
