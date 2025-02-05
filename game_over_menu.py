import pygame
from tools import SCREEN_WIDTH

import sys


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
