import pygame
from tools import SCREEN_WIDTH, SCREEN_HEIGHT

import sys


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

            with open("base/best.txt", 'r', encoding="utf8") as f:
                n = f.read().strip()
                text = font.render(f"best result: {n}", True, (255, 255, 255))
                self.engine.screen.blit(text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 50))

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
