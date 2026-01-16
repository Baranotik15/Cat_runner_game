import pygame
from settings import SCREEN_WIDTH, GROUND_Y, OBSTACLE_SIZE, BLACK, OBSTACLE_SPEED


class Obstacle:
    def __init__(self):
        self.width, self.height = OBSTACLE_SIZE
        self.x = SCREEN_WIDTH
        self.y = GROUND_Y - self.height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def off_screen(self):
        return self.rect.right < 0
