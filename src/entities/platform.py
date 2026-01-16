import pygame
import random

from settings import (
    SCREEN_WIDTH,
    BLACK,
    PLATFORM_MIN_WIDTH,
    PLATFORM_MAX_WIDTH,
    PLATFORM_HEIGHT,
)


class Platform:
    def __init__(self, level_y):
        self.width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        self.height = PLATFORM_HEIGHT

        self.x = SCREEN_WIDTH
        self.y = level_y

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def off_screen(self):
        return self.rect.right < 0
