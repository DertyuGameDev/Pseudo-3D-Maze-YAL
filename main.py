import pygame
import sys
import math

from field import Field
from tools import *


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
        return MAP[square] == '#'
    return False


class Player:
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    CASTED_RAYS = 150
    STEP_ANGLE = FOV / CASTED_RAYS
    MAX_DEPTH = 600

    def __init__(self):
        self.player_x = SCREEN_WIDTH // 4
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0
        self.speed = 3
        self.sprite = PlayerSprite(12, self.player_x, self.player_y)

    def normal_vector(self, screen, distance):
        pygame.draw.line(screen, 'yellow', (self.player_x, self.player_y),
                         (self.player_x + math.cos(self.player_angle) * distance,
                          self.player_y + math.sin(self.player_angle) * distance))

    def rayCast(self, screen):
        start_angle = self.player_angle - Player.HALF_FOV
        for ray in range(Player.CASTED_RAYS):
            for depth in range(Player.MAX_DEPTH):
                target_x = self.player_x + math.cos(start_angle) * depth
                target_y = self.player_y + math.sin(start_angle) * depth

                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)
                if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
                    square = row * MAP_SIZE + col

                    if MAP[square] == '#':
                        color = 255 / (1 + depth * depth * 0.0001)
                        wall_height = 21000 / (depth + 0.0001)
                        wall_top = (SCREEN_HEIGHT // 2) - (wall_height // 2)
                        pygame.draw.rect(screen, (color, color, color), (
                            ray * (SCREEN_WIDTH // Player.CASTED_RAYS) + SCREEN_WIDTH // 2, wall_top,
                            SCREEN_WIDTH // Player.CASTED_RAYS,
                            wall_height))

                        break

            start_angle += Player.STEP_ANGLE

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


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mouse.set_visible(False)  # Hide the mouse cursor
        self.grab = True
        pygame.event.set_grab(True)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.field = Field(self.screen)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(not pygame.mouse.get_visible())
                    self.grab = not self.grab
                    pygame.event.set_grab(self.grab)
            # Get mouse movement
            if self.grab:
                mouse_x, mouse_y = pygame.mouse.get_rel()
                self.player.player_angle += mouse_x * 0.001

                self.screen.fill('gray', pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT // 2))
                self.screen.fill('blue', pygame.Rect(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT // 2))
                self.field.draw_map()
                self.player.rayCast(self.screen)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.player.move(-1, left=True)
                if keys[pygame.K_d]:
                    self.player.move(1, right=True)
                if keys[pygame.K_w]:
                    self.player.move(1)
                if keys[pygame.K_s]:
                    self.player.move(-1)

            self.player.render(self.screen)
            self.player.normal_vector(self.screen, 35)
            pygame.display.flip()
            self.clock.tick(60)


e = Engine()
e.loop()
