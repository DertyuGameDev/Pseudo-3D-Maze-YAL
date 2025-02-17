import pygame
import sys

from load_image import load_image
from dragon import *


def paint_screen(screen, width, height):
    image = load_image("title_screen.jpg")
    fon = pygame.transform.scale(image, (width, height))

    text_coord = 10
    pos_start_btn = (500, 130, 233, 68)
    pos_exit_btn = (10, 500, 217, 68)

    create_text(text_coord, screen)

    all_sprites = pygame.sprite.Group()

    chill_image = load_image("chill.png")
    chill_image = pygame.transform.scale(chill_image, (200, 200))

    chill_sprite = pygame.sprite.Sprite()
    chill_sprite.image = chill_image
    chill_sprite.rect = chill_sprite.image.get_rect()
    chill_sprite.mask = pygame.mask.from_surface(chill_sprite.image)
    all_sprites.add(chill_sprite)

    chill_sprite.rect.x = width - 200
    chill_sprite.rect.y = height - 200
    # screen.blit(chill_image, (width - 200, height - 200))
    all_sprites.draw(screen)

    pygame.display.flip()
    running = True

    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png", -1), 8, 2, 50, 50, all_sprites)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cur_x, cur_y = event.pos
                if (pos_start_btn[0] <= cur_x <= pos_start_btn[0] + pos_start_btn[2] and
                        pos_start_btn[1] <= cur_y <= pos_start_btn[1] + pos_start_btn[3]):
                    running = False
                if (pos_exit_btn[0] <= cur_x <= pos_exit_btn[0] + pos_exit_btn[2] and
                        pos_exit_btn[1] <= cur_y <= pos_exit_btn[1] + pos_exit_btn[3]):
                    sys.exit(0)
            if event.type == pygame.MOUSEMOTION:
                cur_x, cur_y = event.pos
                if (pos_start_btn[0] <= cur_x <= pos_start_btn[0] + pos_start_btn[2] and
                        pos_start_btn[1] <= cur_y <= pos_start_btn[1] + pos_start_btn[3]):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif (pos_exit_btn[0] <= cur_x <= pos_exit_btn[0] + pos_exit_btn[2] and
                      pos_exit_btn[1] <= cur_y <= pos_exit_btn[1] + pos_exit_btn[3]):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif chill_sprite.rect.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        all_sprites.update()
        screen.fill("black")
        screen.blit(fon, (0, 0))
        create_text(text_coord, screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(15)


def create_text(text_coord, screen):
    intro_screen = ["Просто чиловая заставка", "Начать"]

    font = pygame.font.Font(None, 100)

    for line in intro_screen:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 200
        if line == "Начать":
            intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_coord += 50
    string_rendered = font.render("Выйти", 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 500
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)


if __name__ == "__main__":
    pygame.init()
    size = width, height = 1200, 600
    screen = pygame.display.set_mode(size)

    paint_screen(screen, width, height)

    pygame.quit()
