import pygame
import schedule
from string import ascii_lowercase
from tools import SCREEN_WIDTH, SCREEN_HEIGHT

import sys


class GameOverMenu:
    def __init__(self, engine, score):
        self.engine = engine
        self.score = score
        self.running = False
        self.paint_white_rect = False
        self.input_name = True
        self.white_rect_coord = [10, 200]
        self.s = ''

    def show(self):
        self.running = True
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.engine.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        text = font.render(f"Game Over - Score: {self.score}", True, (255, 255, 255))
        self.engine.screen.blit(text, (10, 10))

        buttons = ["Restart", "Exit"]
        button_rects = []
        for i, btn_text in enumerate(buttons):
            btn_text_render = font.render(btn_text, True, (255, 255, 255))
            btn_rect = btn_text_render.get_rect(center=(10 + btn_text_render.get_width() // 2, 20 + 50 * (i + 1)))
            button_rects.append((btn_text_render, btn_rect))
            self.engine.screen.blit(btn_text_render, btn_rect)

        text = font.render("Введите имя (5 символов): ", True, "white")
        self.engine.screen.blit(text, (10, 150))

        text = font.render("Чтобы сохранить результат, нажмите Enter", True, "white")
        self.engine.screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, SCREEN_HEIGHT - text.get_height() - 10))

        with open("base/best.txt", 'r', encoding="utf8") as read_file:
            lines = read_file.readlines()

        for i, line in enumerate(lines):
            text = font.render(line.strip(), True, "white")
            self.engine.screen.blit(text, (SCREEN_WIDTH // 2, 10 + 50 * i))

        # with open("base/best.txt", 'r', encoding="utf8") as f:
        #     n = f.read().strip()
        #     text = font.render(f"best result: {n}", True, (255, 255, 255))
        #     self.engine.screen.blit(text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 50))

        job = schedule.every(1).second.do(self.print_white_rect)

        while self.running:
            schedule.run_pending()
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
                if event.type == pygame.MOUSEMOTION:
                    if button_rects[0][1].collidepoint(event.pos) or button_rects[1][1].collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.KEYDOWN and self.input_name:
                    if event.unicode in ascii_lowercase:
                        if len(self.s) < 5:
                            self.s += event.unicode
                            pygame.draw.rect(self.engine.screen, "black", (*self.white_rect_coord, 20, 50))
                            name = font.render(self.s, True, "white")
                            self.white_rect_coord[0] = 10 + name.get_width()
                            self.engine.screen.blit(name, (10, 200))
                    elif event.key == pygame.K_BACKSPACE:
                        if self.s:
                            self.s = self.s[:-1]
                            pygame.draw.rect(self.engine.screen, "black", (10, 200, 300, 60))
                            name = font.render(self.s, True, "white")
                            self.white_rect_coord[0] = 10 + name.get_width()
                            self.engine.screen.blit(name, (10, 200))

                    elif event.key == pygame.K_RETURN:
                        self.input_name = False
                        schedule.cancel_job(job)
                        self.paint_white_rect = False
                        pygame.draw.rect(self.engine.screen, "black", (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
                        text = font.render("Результат сохранен", True, "white")
                        self.engine.screen.blit(text,
                                                (SCREEN_WIDTH - text.get_width() - 10,
                                                 SCREEN_HEIGHT - text.get_height() - 10))
                        self.save_name()

            if self.paint_white_rect:
                pygame.draw.rect(self.engine.screen, "white", (*self.white_rect_coord, 20, 50))
            else:
                pygame.draw.rect(self.engine.screen, "black", (*self.white_rect_coord, 20, 50))

            pygame.display.flip()

    def print_white_rect(self):
        self.paint_white_rect = not self.paint_white_rect

    def save_name(self):
        with open("base/best.txt", 'r', encoding="utf8") as read_file:
            lines = read_file.readlines()
            arr = []
            for line in lines:
                s = line.split()
                s[0] = int(s[0])
                arr.append(s)
        arr.append([self.score, self.s])
        arr = sorted(arr, key=(lambda x: (-x[0], x[1])))[0:5]
        arr = list(map(lambda x: ' '.join([str(x[0]), x[1]]), arr))
        arr = '\n'.join(arr)
        with open("base/best.txt", 'w') as f:
            print(arr, file=f)

        with open("base/best.txt", 'r', encoding="utf8") as read_file:
            lines = read_file.readlines()

        pygame.draw.rect(self.engine.screen, "black", (SCREEN_WIDTH // 2, 10, SCREEN_WIDTH // 2, 400))

        font = pygame.font.Font(None, 50)
        for i, line in enumerate(lines):
            text = font.render(line.strip(), True, "white")
            self.engine.screen.blit(text, (SCREEN_WIDTH // 2, 10 + 50 * i))
