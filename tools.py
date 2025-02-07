import pygame
import AlgorithmMaze

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200

MAP_SIZE = AlgorithmMaze.SIZE + 1
TILE_SIZE = SCREEN_WIDTH // 10 // MAP_SIZE
START_TIME = 60

NEXT_LEVEL = pygame.USEREVENT + 1
TIMER_EXIT = pygame.USEREVENT + 2
