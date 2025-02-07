import time

import pygame
import sys
import math
import AlgorithmMaze
from start_screen import paint_screen

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
MAP_SIZE = AlgorithmMaze.SIZE + 1
TILE_SIZE = SCREEN_WIDTH // 10 // MAP_SIZE
START_TIME = 20
MAP = []
for i in AlgorithmMaze.generathion_maze():
    MAP += i
strx = 0
stry = 0
for k in range(len(MAP)):
    if MAP[k] == 0:
        strx = k // MAP_SIZE
        stry = k % MAP_SIZE
        break

NEXT_LEVEL = pygame.USEREVENT + 1
TIMER_EXIT = pygame.USEREVENT + 2


class Timer:
    def __init__(self):
        self.time_left = START_TIME
        self.start_time = time.time()
        self.running = True
        self.pause_start_time = 0  # Время начала паузы

    def pause(self):
        if self.running:
            self.pause_start_time = time.time()  # Запоминаем время начала паузы
            self.running = False

    def resume(self):
        if not self.running:
            pause_duration = time.time() - self.pause_start_time  # Вычисляем длительность паузы
            self.start_time += pause_duration  # Корректируем start_time на длительность паузы
            self.running = True

    def reset(self):
        self.time_left = START_TIME
        self.start_time = time.time()
        self.running = True

    def update(self):
        if self.running:
            self.time_left = max(0, START_TIME - int(time.time() - self.start_time))
            if self.time_left == 0:
                pygame.event.post(pygame.event.Event(TIMER_EXIT))

    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {self.time_left}", True, (255, 255, 255))
        screen.blit(timer_text, (SCREEN_WIDTH - 110, 10))


class PauseMenu:
    def __init__(self, engine):
        self.engine = engine
        self.running = False

    def show(self):
        self.running = True
        while self.running:
            self.engine.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 50)

            text = font.render("Paused", True, (255, 255, 255))
            self.engine.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

            buttons = ["Continue", "Restart", "Exit"]
            button_rects = []
            for i, btn_text in enumerate(buttons):
                btn_text_render = font.render(btn_text, True, (255, 255, 255))
                btn_rect = btn_text_render.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 100))
                button_rects.append((btn_text_render, btn_rect))
                self.engine.screen.blit(btn_text_render, btn_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rects[0][1].collidepoint(event.pos):  # Continue
                        self.running = False
                        self.engine.paused = False
                        pygame.mouse.set_visible(False)
                        return
                    elif button_rects[1][1].collidepoint(event.pos):  # Restart
                        self.engine.restart()
                        return
                    elif button_rects[2][1].collidepoint(event.pos):  # Exit
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.engine.paused = False
                    pygame.mouse.set_visible(False)
                    self.engine.timer.resume()
                    return


class GameOverMenu:
    def __init__(self, engine, score):
        self.engine = engine
        self.score = score
        self.running = False

    def show(self):
        self.running = True
        pygame.mouse.set_visible(True)
        while self.running:
            self.engine.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 50)

            text = font.render(f"Game Over - Score: {self.score}", True, (255, 255, 255))
            self.engine.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

            buttons = ["Restart", "Exit"]
            button_rects = []
            for i, btn_text in enumerate(buttons):
                btn_text_render = font.render(btn_text, True, (255, 255, 255))
                btn_rect = btn_text_render.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 100))
                button_rects.append((btn_text_render, btn_rect))
                self.engine.screen.blit(btn_text_render, btn_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rects[0][1].collidepoint(event.pos):  # Restart
                        self.engine.restart()
                        pygame.mouse.set_visible(False)
                        return
                    elif button_rects[1][1].collidepoint(event.pos):  # Exit
                        pygame.quit()
                        sys.exit()


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
        if MAP[square] == -1:
            pygame.event.post(pygame.event.Event(NEXT_LEVEL))
        return not (MAP[square] == 0 or MAP[square] == -1)
    return False


class Player:
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    CASTED_RAYS = 300
    DELTA_ANGLE = FOV / CASTED_RAYS
    STEP_ANGLE = FOV / CASTED_RAYS
    MAX_DEPTH = 300

    def __init__(self):
        self.player_x = strx * TILE_SIZE + 3
        self.player_y = stry * TILE_SIZE + 3
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
                        shade = 255 / (1 + depth * depth * 4 * 0.001)

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
                            shade_surface.fill(shade_factor)
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
                pygame.draw.line(screen, 'yellow', (self.player_x, self.player_y), (target_x, target_y))

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
                if MAP[square] == 0:
                    color = 'gray'
                elif MAP[square] == -1:
                    color = 'yellow'
                else:
                    color = 'black'
                pygame.draw.rect(self.screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        self.timer = Timer()
        self.paused = False
        self.player = Player()
        self.field = Field(self.screen)
        self.pause_menu = PauseMenu(self)
        self.game_over_menu = None
        # Load wall textures
        self.textures = {
            -1: pygame.image.load('data/yellow.jpg').convert(),
        }

    def restart(self):
        pygame.event.set_grab(True)
        global MAP, strx, stry
        MAP = []
        for i in AlgorithmMaze.generathion_maze():
            MAP += i
        strx = stry = 0
        for k in range(len(MAP)):
            if MAP[k] == 0:
                strx, stry = k // MAP_SIZE, k % MAP_SIZE
                break
        self.player.player_x = strx * TILE_SIZE + 3
        self.player.player_y = stry * TILE_SIZE + 3
        self.timer.reset()
        pygame.mouse.set_visible(False)
        self.paused = False
        self.loop()

    def loop(self):
        global MAP, strx, stry
        pygame.mouse.set_visible(True)
        paint_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.mouse.set_visible(False)
        self.score = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == NEXT_LEVEL:
                    MAP = []
                    for i in AlgorithmMaze.generathion_maze():
                        MAP += i
                    strx = 0
                    stry = 0
                    for k in range(len(MAP)):
                        if MAP[k] == 0:
                            strx = k // MAP_SIZE
                            stry = k % MAP_SIZE
                            break
                    self.field.draw_map()
                    self.score += 1
                    self.player.player_x = strx * TILE_SIZE + 3
                    self.player.player_y = stry * TILE_SIZE + 3
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        pygame.mouse.set_visible(self.paused)
                        if self.paused:
                            self.timer.pause()  # Ставим таймер на паузу
                            self.pause_menu.show()
                        else:
                            self.timer.resume()  # Возобновляем таймер
                if event.type == TIMER_EXIT:
                    with open('base/best.txt', 'r') as fl:
                        s = int(fl.read())
                    with open('base/best.txt', 'w') as fl1:
                        if self.score > s:
                            fl1.write(str(self.score))
                        else:
                            fl1.write(str(s))
                    self.game_over_menu = GameOverMenu(self, self.score)
                    self.game_over_menu.show()
                    return

            if not self.paused:
                self.timer.update()
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
            self.timer.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    e = Engine()
    e.loop()
