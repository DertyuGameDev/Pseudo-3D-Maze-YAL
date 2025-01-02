import random

SIZE = 15

directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]


def is_valid_move(x, y, maze):
    return 0 <= x < SIZE and 0 <= y < SIZE and maze[x][y] in (1, 2, 3, 4, 5, 6)


def create_maze(x, y, maze):
    maze[x][y] = 0
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(nx, ny, maze):
            maze[x + dx // 2][y + dy // 2] = 0
            create_maze(nx, ny, maze)
    return maze


def generation():
    maze = [[random.randint(1, 2) for _ in range(SIZE)] for _ in range(SIZE)]
    a = create_maze(SIZE // 2, SIZE - 1, maze)
    a[SIZE // 2][SIZE // 2] = 0
    return a

