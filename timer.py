import time
import pygame
from tools import START_TIME, SCREEN_WIDTH, TIMER_EXIT


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
        timer_text = font.render(f"Time: {self.time_left}", True, (0, 255, 255))
        screen.blit(timer_text, (SCREEN_WIDTH - 110, 10))
