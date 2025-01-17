import pygame
import sys
import math
import AlgorithmMaze

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
MAP_SIZE = AlgorithmMaze.SIZE
TILE_SIZE = SCREEN_WIDTH // 10 // MAP_SIZE
MAP = []
for i in AlgorithmMaze.generation():
    MAP += i


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("green"), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, x, y):
        self.rect.center = (x, y)


def check_collision(new_x, new_y):
    col = int(new_x / TILE_SIZE)
    row = int(new_y / TILE_SIZE)

    if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
        square = row * MAP_SIZE + col
        return not (MAP[square] == 0)
    return False


class Player:
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    CASTED_RAYS = 200
    DELTA_ANGLE = FOV / CASTED_RAYS
    STEP_ANGLE = FOV / CASTED_RAYS
    MAX_DEPTH = 800

    def __init__(self):
        self.player_x = SCREEN_WIDTH // 10 - TILE_SIZE * MAP_SIZE // 2
        self.player_y = SCREEN_HEIGHT // 10
        self.player_angle = 0
        self.speed = 1
        self.sprite = PlayerSprite(TILE_SIZE // 10, self.player_x, self.player_y)
        self.projection_plane_distance = (SCREEN_WIDTH / 2) / math.tan(self.HALF_FOV)

    def normal_vector(self, screen, distance):
        pygame.draw.line(screen, 'yellow', (self.player_x, self.player_y),
                         (self.player_x + math.cos(self.player_angle) * distance,
                          self.player_y + math.sin(self.player_angle) * distance))

    def rayCast(self, screen, textures):
        start_angle = self.player_angle - Player.HALF_FOV
        for ray in range(Player.CASTED_RAYS):
            ray_angle = start_angle + ray * Player.STEP_ANGLE
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            for depth in range(1, Player.MAX_DEPTH):
                target_x = self.player_x + cos_a * depth
                target_y = self.player_y + sin_a * depth

                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)
                if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
                    square = row * MAP_SIZE + col
                    wall_type = MAP[square]

                    if wall_type != 0:
                        perpendicular_distance = depth * math.cos(ray_angle - self.player_angle)
                        if perpendicular_distance > 0:
                            wall_height = (TILE_SIZE * self.projection_plane_distance) / perpendicular_distance
                        else:
                            wall_height = SCREEN_HEIGHT

                        # Применяем затенение на основе расстояния
                        shade = 255 / (1 + depth * depth * 0.001)

                        # Определяем цвет стены или текстуру
                        color = (shade, shade, shade)
                        texture = textures.get(wall_type, None)
                        if texture:
                            # Рассчитываем отображение текстуры
                            hit_x = target_x % TILE_SIZE
                            texture_width, texture_height = texture.get_size()
                            texture_column = int(hit_x / TILE_SIZE * texture_width)
                            texture_strip = texture.subsurface(
                                (texture_column, 0, 1, texture_height)
                            )
                            scaled_strip = pygame.transform.scale(texture_strip, (
                                SCREEN_WIDTH // Player.CASTED_RAYS, int(wall_height)))

                            shade_surface = pygame.Surface(scaled_strip.get_size()).convert_alpha()
                            shade_factor = shade / 255  # Нормализуем значение
                            shade_surface.fill((shade_factor * 255, shade_factor * 255, shade_factor * 255))
                            scaled_strip.blit(shade_surface, (0, 0), special_flags=pygame.BLEND_MULT)
                            screen.blit(scaled_strip, (
                                ray * (SCREEN_WIDTH // Player.CASTED_RAYS),
                                (SCREEN_HEIGHT // 2) - (wall_height // 2)))
                        else:
                            pygame.draw.rect(screen, color, (
                                ray * (SCREEN_WIDTH // Player.CASTED_RAYS),
                                (SCREEN_HEIGHT // 2) - (wall_height // 2),
                                SCREEN_WIDTH // Player.CASTED_RAYS,
                                wall_height))
                        break

    def move(self, direction, right=False, left=False):
        pxa = self.player_angle
        pya = self.player_angle
        if left or right:
            pxa += math.radians(90)
            pya += math.radians(90)
        new_x = self.player_x + math.cos(pxa) * direction * self.speed
        new_y = self.player_y + math.sin(pya) * direction * self.speed
        if not check_collision(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

    def render(self, screen):
        self.sprite.update(self.player_x, self.player_y)
        screen.blit(self.sprite.image, self.sprite.rect)


class Field:
    def __init__(self, screen):
        self.screen = screen

    def draw_map(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                square = i * MAP_SIZE + j
                color = 'gray' if not (MAP[square] == 0) else 'black'
                pygame.draw.rect(self.screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mouse.set_visible(False)
        self.grab = True
        pygame.event.set_grab(True)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.field = Field(self.screen)

        # Load wall textures
        self.textures = {
            # 1: pygame.image.load('modern-new-painted-metal-surface.jpg').convert(),
            # 2: pygame.image.load('IMG_5283.PNG').convert(),
        }

    def loop(self):
        self.field.draw_map()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(not pygame.mouse.get_visible())
                    self.grab = not self.grab
                    pygame.event.set_grab(self.grab)
            if self.grab:
                mouse_x, mouse_y = pygame.mouse.get_rel()
                self.player.player_angle += mouse_x * 0.001

                self.screen.fill('gray', pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH,
                                                     SCREEN_HEIGHT // 2))
                self.screen.fill('blue', pygame.Rect(0, 0, SCREEN_WIDTH,
                                                     SCREEN_HEIGHT // 2))
                self.player.rayCast(self.screen, self.textures)
                self.field.draw_map()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.player.move(-1, left=True)
                if keys[pygame.K_d]:
                    self.player.move(1, right=True)
                if keys[pygame.K_w]:
                    self.player.move(1)
                if keys[pygame.K_s]:
                    self.player.move(-1)
                if keys[pygame.K_UP]:
                    print(self.player.FOV)
                    Player.FOV += math.radians(1)
                    Player.FOV = min(3.141592653589793 / 2, Player.FOV)
                    Player.CASTED_RAYS += 10
                if keys[pygame.K_DOWN]:
                    print(self.player.FOV)
                    Player.FOV -= math.radians(1)
                Player.HALF_FOV = self.player.FOV / 2
                Player.STEP_ANGLE = self.player.FOV / self.player.CASTED_RAYS
            self.player.render(self.screen)
            self.player.normal_vector(self.screen, 35)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    e = Engine()
    e.loop()
