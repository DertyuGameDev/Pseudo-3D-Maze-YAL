import random

from PIL import Image

SIZE = 30
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

    maze = create_maze(SIZE // 2, SIZE - 1, maze)
    for i in range(SIZE):
        maze[i] += [1]
    maze.append([1 for i in range(SIZE + 2)])
    maze[SIZE // 2][SIZE // 2] = 0
    return maze


def create_exit(maze):
    exit_row = random.randint(1, SIZE - 1)
    maze[exit_row][SIZE] = 0
    maze[exit_row][SIZE - 1] = 0


def maze_to_image(maze):
    wall_color = (0, 0, 0)
    path_color = (255, 255, 255)

    img = Image.new('RGB', (SIZE + 1, SIZE + 1))
    # print(maze)
    for x in range(SIZE + 1):
        for y in range(SIZE + 1):
            if maze[x][y] == 0:
                img.putpixel((y, x), path_color)  # Path
            else:
                img.putpixel((y, x), wall_color)  # Wall

    return img


def generathion_maze():
    maze = generation()
    create_exit(maze)
    image = maze_to_image(maze)
    image.save('maze.png')
    return maze
