import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Получение информации о дисплее
info_object = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info_object.current_w, info_object.current_h
HALF_HEIGHT = SCREEN_HEIGHT // 2

# Настройка полноэкранного режима
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Raycasting Maze Game with Mini-Map")

# Скрыть курсор и захватить его
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (110, 110, 110)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Настройки карты
MAP_WIDTH = 10
MAP_HEIGHT = 10
TILE_SIZE = 64  # Размер каждой ячейки карты

# Настройки мини-карты
MINIMAP_SCALE = 0.2  # Масштаб мини-карты относительно оригинальной карты
MINIMAP_TILE_SIZE = int(TILE_SIZE * MINIMAP_SCALE)
MINIMAP_WIDTH = MAP_WIDTH * MINIMAP_TILE_SIZE
MINIMAP_HEIGHT = MAP_HEIGHT * MINIMAP_TILE_SIZE
MINIMAP_PADDING = 10  # Отступ от верхнего и левого края экрана

# Настройки игрока
FOV = math.pi / 3  # Угол обзора (60 градусов)
HALF_FOV = FOV / 2
NUM_RAYS = SCREEN_WIDTH // 9  # Количество лучей зависит от ширины экрана
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = (SCREEN_WIDTH / 2) / math.tan(HALF_FOV)
PROJ_COEFF = DIST * TILE_SIZE
SCALE = SCREEN_WIDTH // NUM_RAYS

# Определение лабиринта (1 = стена, 0 = пусто)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Часы для контроля частоты кадров
clock = pygame.time.Clock()


# Класс игрока
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 2
        self.rot_speed = 0.003  # Скорость вращения, уменьшена для плавности

    def movement(self, delta_angle):
        self.angle += delta_angle
        self.angle %= math.tau  # Ограничение угла от 0 до 2π

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dx += self.speed * cos_a
            dy += self.speed * sin_a
        if keys[pygame.K_s]:
            dx -= self.speed * cos_a
            dy -= self.speed * sin_a
        if keys[pygame.K_a]:
            dx += self.speed * sin_a
            dy -= self.speed * cos_a
        if keys[pygame.K_d]:
            dx -= self.speed * sin_a
            dy += self.speed * cos_a

        # Проверка столкновений
        if not game_map[int((self.y + dy) // TILE_SIZE)][int((self.x + dx) // TILE_SIZE)]:
            self.x += dx
            self.y += dy


# Функция лучевого трассирования
def ray_casting(player_pos, player_angle):
    rays = []
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        current_angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)

        for depth in range(0, MAX_DEPTH, 2):
            target_x = player_pos[0] + depth * cos_a
            target_y = player_pos[1] + depth * sin_a

            # Проверка выхода за пределы карты
            if target_x < 0 or target_x >= MAP_WIDTH * TILE_SIZE or target_y < 0 or target_y >= MAP_HEIGHT * TILE_SIZE:
                depth = MAX_DEPTH
                break

            # Проверка столкновения с стеной
            if game_map[int(target_y // TILE_SIZE)][int(target_x // TILE_SIZE)]:
                break

        # Корректировка расстояния для предотвращения эффекта "рыбий глаз"
        depth *= math.cos(player_angle - current_angle)
        # Вычисление высоты стены
        if depth == 0:
            depth = 0.0001  # Предотвращение деления на ноль
        proj_height = PROJ_COEFF / depth

        # Определение цвета стены в зависимости от расстояния
        color_intensity = 255 / (1 + depth * depth * 0.0001)
        color = (color_intensity, color_intensity, color_intensity)

        rays.append((depth, proj_height, color))
    return rays


# Функция отрисовки мини-карты
def draw_minimap(player):
    # Отрисовка фона мини-карты
    minimap_surface = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
    minimap_surface.fill(BLACK)

    # Отрисовка стен на мини-карте
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * MINIMAP_TILE_SIZE, y * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE)
            if game_map[y][x]:
                pygame.draw.rect(minimap_surface, DARKGRAY, rect)
            else:
                pygame.draw.rect(minimap_surface, BLACK, rect)
            pygame.draw.rect(minimap_surface, DARKGRAY, rect, 1)  # Сетка мини-карты

    # Отрисовка игрока на мини-карте
    player_map_x = player.x / TILE_SIZE * MINIMAP_SCALE
    player_map_y = player.y / TILE_SIZE * MINIMAP_SCALE
    pygame.draw.circle(minimap_surface, GREEN, (int(player_map_x), int(player_map_y)), 5)

    # Отрисовка направления взгляда игрока на мини-карте
    end_x = player_map_x + math.cos(player.angle) * 10
    end_y = player_map_y + math.sin(player.angle) * 10
    pygame.draw.line(minimap_surface, YELLOW, (player_map_x, player_map_y), (end_x, end_y), 2)

    # Отображение мини-карты на основном экране
    screen.blit(minimap_surface, (MINIMAP_PADDING, MINIMAP_PADDING))


# Рендеринг 3D вида с использованием лучевого трассирования
def render_3d(rays):
    for ray, (depth, proj_height, color) in enumerate(rays):
        # Вычисление высоты столбца на экране
        column_height = proj_height

        # Определение цвета в зависимости от глубины
        shade = 255 / (1 + depth * depth * 0.0001)
        color = (shade, shade, shade)

        # Рисование вертикального столбца
        pygame.draw.rect(screen, color,
                         (ray * SCALE, HALF_HEIGHT - column_height // 2, SCALE, column_height))


# Главный игровой цикл
def main():
    player = Player(3 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2, 0)
    running = True

    # Центр экрана для мыши
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    pygame.mouse.set_pos((center_x, center_y))

    while running:
        delta_angle = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Выход из полноэкранного режима по нажатию ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Получение движения мыши
        mouse_dx, _ = pygame.mouse.get_rel()
        sensitivity = 0.002  # Чувствительность вращения
        delta_angle = mouse_dx * sensitivity

        player.movement(delta_angle)

        # Заполнение экрана черным цветом
        screen.fill(BLACK)

        # Выполнение лучевого трассирования и рендеринг 3D сцены
        rays = ray_casting((player.x, player.y), player.angle)
        render_3d(rays)

        # Отрисовка мини-карты
        draw_minimap(player)

        pygame.display.flip()
        clock.tick(60)  # Ограничение до 60 FPS

        # Сброс положения мыши в центр экрана
        pygame.mouse.set_pos((center_x, center_y))

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
