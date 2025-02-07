import pygame
from tools import *


class Field:
    def __init__(self, screen):
        self.screen = screen

    def draw_map(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                square = i * MAP_SIZE + j
                color = 'gray' if MAP[square] == '#' else 'black'
                pygame.draw.rect(self.screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
