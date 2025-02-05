import pygame
from tools import TILE_SIZE, MAP_SIZE, MAP, NEXT_LEVEL


def check_collision(new_x, new_y):
    col = int(new_x / TILE_SIZE)
    row = int(new_y / TILE_SIZE)

    if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
        square = row * MAP_SIZE + col
        if MAP[square] == -1:
            pygame.event.post(pygame.event.Event(NEXT_LEVEL))
        return not (MAP[square] == 0 or MAP[square] == -1)
    return False
