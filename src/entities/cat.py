import pygame
from settings import GROUND_Y, CAT_SIZE, BLACK, GRAVITY, JUMP_FORCE


class Cat:
    def __init__(self):
        self.width, self.height = CAT_SIZE
        self.x = 100
        self.y = GROUND_Y - self.height

        self.velocity_y = 0
        self.on_ground = True

        self.ignore_platform = False
        self.target_platform = None

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prev_rect = self.rect.copy()

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_FORCE
            self.on_ground = False

    def drop_down(self, platforms):
        lower_platforms = [
            p for p in platforms
            if p.rect.top > self.rect.bottom
        ]

        if lower_platforms:
            self.target_platform = min(lower_platforms, key=lambda p: p.rect.top)
        else:
            self.target_platform = None

        self.ignore_platform = True
        self.on_ground = False
        self.velocity_y = max(self.velocity_y, 5)

    def update(self):
        self.prev_rect = self.rect.copy()

        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.on_ground = True
            self.ignore_platform = False
            self.target_platform = None

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
