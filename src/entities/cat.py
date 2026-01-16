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
        self.drop_hold = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prev_rect = self.rect.copy()

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_FORCE
            self.on_ground = False

    def drop_once(self, platforms):
        lower = [p for p in platforms if p.rect.top > self.rect.bottom]
        self.target_platform = min(lower, key=lambda p: p.rect.top) if lower else None

        self.ignore_platform = True
        self.drop_hold = False
        self.on_ground = False
        self.velocity_y = max(self.velocity_y, 5)

    def drop_hold_start(self):
        self.ignore_platform = True
        self.target_platform = None
        self.drop_hold = True
        self.on_ground = False
        self.velocity_y = max(self.velocity_y, 5)

    def drop_hold_end(self):
        self.drop_hold = False

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
            self.drop_hold = False

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
