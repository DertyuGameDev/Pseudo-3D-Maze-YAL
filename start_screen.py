import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def paint_screen(screen, width, height):
    image = load_image("title_screen.jpg")
    fon = pygame.transform.scale(image, (width, height))
    screen.blit(fon, (0, 0))

    intro_screen = ["Просто чиловая заставка", "Начать"]

    font = pygame.font.Font(None, 100)
    text_coord = 10
    pos_start_btn = (0, 0, 0, 0)

    for line in intro_screen:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 200
        if line == "Начать":
            intro_rect.x = 500
            pos_start_btn = intro_rect.x, intro_rect.y, intro_rect.width, intro_rect.height
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        text_coord += 50
    string_rendered = font.render("Выйти", 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 500
    intro_rect.x = 10
    pos_exit_btn = (intro_rect.x, intro_rect.y, intro_rect.width, intro_rect.height)
    screen.blit(string_rendered, intro_rect)

    chill_image = load_image("chill.png")
    chill_image = pygame.transform.scale(chill_image, (200, 200))
    screen.blit(chill_image, (width - 200, height - 200))

    pygame.display.flip()
    running = True

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
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


if __name__ == "__main__":
    pygame.init()
    size = width, height = 1200, 600
    screen = pygame.display.set_mode(size)

    paint_screen(screen, width, height)

    pygame.quit()
