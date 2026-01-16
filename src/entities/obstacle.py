import pygame
from settings import OBSTACLE_SIZE, BLACK


class Obstacle:
    def __init__(self, x, surface_y):
        self.width, self.height = OBSTACLE_SIZE
        self.x = x
        self.y = surface_y - self.height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def off_screen(self):
        return self.rect.right < 0
