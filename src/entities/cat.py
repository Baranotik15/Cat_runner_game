import pygame
from settings import (
    GROUND_Y,
    CAT_SIZE,
    BLACK,
    GRAVITY,
    JUMP_FORCE,
    FLOAT_GRAVITY,
    LEVEL_GAP,
)


class Cat:
    def __init__(self):
        self.width, self.height = CAT_SIZE

        self.x = 100
        self.y = GROUND_Y - self.height

        self.velocity_y = 0
        self.on_ground = True

        self.float_mode = False

        self.ignore_platform = False
        self.current_platform = None
        self.target_platform = None
        self.drop_hold = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prev_rect = self.rect.copy()

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_FORCE
            self.on_ground = False
            self.current_platform = None

    def start_float(self):
        if not self.on_ground:
            self.float_mode = True

    def stop_float(self):
        self.float_mode = False

    def drop_once(self, platforms):
        if not self.on_ground:
            return

        current_y = self.y + self.height
        target_y = current_y + LEVEL_GAP
        tolerance = LEVEL_GAP // 3
        below = [
            p for p in platforms
            if abs(p.rect.top - target_y) <= tolerance
        ]

        if not below:
            return

        self.target_platform = min(below, key=lambda p: abs(p.rect.centerx - self.rect.centerx))

        self.ignore_platform = True
        self.on_ground = False
        self.current_platform = None
        self.velocity_y = 6

    def drop_hold_start(self):
        self.drop_hold = True
        self.ignore_platform = True
        self.current_platform = None

    def drop_hold_end(self):
        self.drop_hold = False
        self.ignore_platform = False
        self.target_platform = None

    def update(self):
        self.prev_rect = self.rect.copy()

        if self.float_mode and self.velocity_y > 0:
            self.velocity_y += FLOAT_GRAVITY
        else:
            self.velocity_y += GRAVITY

        self.y += self.velocity_y

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.on_ground = True
            self.float_mode = False
            self.ignore_platform = False
            self.current_platform = None
            self.target_platform = None

        self.rect.x = self.x
        self.rect.y = self.y


    def land_on_platform(self, platform):
        self.y = platform.rect.top - self.height
        self.velocity_y = 0
        self.on_ground = True
        self.float_mode = False
        self.ignore_platform = False
        self.current_platform = platform
        self.target_platform = None
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
