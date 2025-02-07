import pygame

from math import pi, cos, sin, asin, radians, degrees

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1800
MAP_SIZE = 8
MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '##     #'
    '#      #'
    '#      #'
    '########'
)

TILE_SIZE = 1200 // (2 * MAP_SIZE)


class Field:
    def __init__(self, screen):
        self.screen = screen

    def draw_map(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                square = i * MAP_SIZE + j
                color = 'gray' if MAP[square] == '#' else 'black'
                pygame.draw.rect(self.screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))


POINTS = []

for i in range(len(MAP)):
    if MAP[i] == '#':
        x = i % 8 * 10
        y = i // 8 * 10

        POINTS.append(((x, y, i), (x + 10, y, i), (x, y + 10, i), (x + 10, y + 10, i)))


class Player:
    def __init__(self):
        self.x = 50
        self.y = 50

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        if not (0 <= self.x <= 80) or not (0 <= self.y <= 80):
            self.x -= dx
            self.y -= dy

    def update(self, screen):
        pygame.draw.circle(screen, "yellow", (self.x * 7.5, self.y * 7.5), 5, width=5)


class Window:
    def __init__(self):
        self.FOV = pi / 3
        self.HALF_FOV = self.FOV / 2
        self.cur_angle = 0

    def draw(self, screen, player: "Player"):
        displayed_walls = []
        for points in POINTS:
            distance = []
            for p in points:
                d = ((p[0] - player.x) ** 2 + (p[1] - player.y) ** 2) ** 0.5
                dx = p[0] - player.x
                alpha = asin(dx / d)
                distance.append((d, alpha, p[2]))

            if (self.cur_angle - self.HALF_FOV <= distance[0][1] <= self.cur_angle + self.HALF_FOV or
                    self.cur_angle - self.HALF_FOV <= distance[1][1] <= self.cur_angle + self.HALF_FOV):
                displayed_walls.append((distance[0], distance[1], distance[0][2]))
            if (self.cur_angle - self.HALF_FOV <= distance[0][1] <= self.cur_angle + self.HALF_FOV or
                    self.cur_angle - self.HALF_FOV <= distance[2][1] <= self.cur_angle + self.HALF_FOV):
                displayed_walls.append((distance[0], distance[2], distance[0][2]))
            if (self.cur_angle - self.HALF_FOV <= distance[2][1] <= self.cur_angle + self.HALF_FOV or
                    self.cur_angle - self.HALF_FOV <= distance[3][1] <= self.cur_angle + self.HALF_FOV):
                displayed_walls.append((distance[2], distance[3], distance[2][2]))
            if (self.cur_angle - self.HALF_FOV <= distance[1][1] <= self.cur_angle + self.HALF_FOV or
                    self.cur_angle - self.HALF_FOV <= distance[3][1] <= self.cur_angle + self.HALF_FOV):
                displayed_walls.append((distance[1], distance[3], distance[1][2]))
            distance = []

        displayed_walls = sorted(displayed_walls, key=lambda x: -x[0][0])
        dx = min((min(displayed_walls, key=lambda x: x[0][1])[0][1]), min(displayed_walls, key=lambda x: x[1][1])[1][1])

        gaming_x = 1200 / radians(120)
        k = 1000
        for p1, p2, i in displayed_walls:
            color = 255 - p1[0] * 3
            x1 = gaming_x * (p1[1] - dx)
            x2 = gaming_x * (p2[1] - dx)
            dy1 = k / p1[0]
            dy2 = k / p2[0]

            pygame.draw.polygon(screen, (color, color, color), [(int(600 + x1), int(SCREEN_HEIGHT // 2 + dy1)),
                                                                (int(600 + x1), int(SCREEN_HEIGHT // 2 - dy1)),
                                                                (int(600 + x2), int(SCREEN_HEIGHT // 2 - dy2)),
                                                                (int(600 + x2), int(SCREEN_HEIGHT // 2 + dy2))])


if __name__ == "__main__":
    pygame.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)

    screen.fill("white")
    f = Field(screen)
    pygame.display.flip()

    p = Player()
    w = Window()
    w.draw(screen, p)
    running = True
    screen.fill('gray', pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                    SCREEN_HEIGHT // 2))
    screen.fill('blue', pygame.Rect(0, 0, SCREEN_WIDTH,
                                    SCREEN_HEIGHT // 2))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    p.move(0, -1)
                if event.key == pygame.K_a:
                    p.move(-1, 0)
                if event.key == pygame.K_s:
                    p.move(0, 1)
                if event.key == pygame.K_d:
                    p.move(1, 0)
                screen.fill('gray', pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                                SCREEN_HEIGHT // 2))
                screen.fill('blue', pygame.Rect(0, 0, SCREEN_WIDTH,
                                                SCREEN_HEIGHT // 2))
                w.draw(screen, p)
        f.draw_map()
        p.update(screen)
        pygame.display.flip()

    pygame.quit()
