import pygame
import random

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TITLE,
    FPS,
    WHITE,
    BASE_SPEED,
    SPEED_INCREASE,
    SPEED_INTERVAL,
    PLATFORM_LEVELS,
)

from entities.cat import Cat
from entities.obstacle import Obstacle
from entities.platform import Platform


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    running = True

    cat = Cat()

    obstacles = []
    obstacle_timer = 0

    platforms = []
    platform_timer = 0

    game_speed = BASE_SPEED
    speed_timer = 0

    last_platform_level_index = 0  # 0 — базовый уровень

    while running:
        clock.tick(FPS)

        # ========= SPEED UPDATE =========
        speed_timer += 1
        if speed_timer >= FPS * SPEED_INTERVAL:
            game_speed += SPEED_INCREASE
            speed_timer = 0

        # ========= EVENTS =========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    cat.jump()

                if event.key == pygame.K_s:
                    cat.drop_down(platforms)

        # ========= UPDATE CAT =========
        cat.update()

        # ========= PLATFORMS (SMART + SAFE SPAWN) =========
        platform_timer += 1
        if platform_timer > 140:

            possible_starts = []
            weights = []

            for i in range(len(PLATFORM_LEVELS)):
                if abs(i - last_platform_level_index) <= 1:
                    possible_starts.append(i)

                    if i == 0:
                        weights.append(6)   # базовый уровень — чаще всего
                    elif i == 1:
                        weights.append(3)
                    else:
                        weights.append(1)   # верхний — редко

            start_level = random.choices(possible_starts, weights=weights)[0]

            # ограничиваем размер связки для высоких уровней
            if start_level >= 2:
                level_count = random.choices([1, 2], weights=[4, 1])[0]
            else:
                level_count = random.choices([1, 2, 3], weights=[1, 4, 4])[0]

            used_levels = []
            for offset in range(level_count):
                level_index = start_level + offset
                if level_index < len(PLATFORM_LEVELS):
                    used_levels.append(level_index)

            for level_index in used_levels:
                platforms.append(
                    Platform(PLATFORM_LEVELS[level_index])
                )

            last_platform_level_index = used_levels[-1]
            platform_timer = 0

        # ========= PLATFORM UPDATE & COLLISIONS =========
        for platform in platforms[:]:
            platform.update(game_speed)
            if platform.off_screen():
                platforms.remove(platform)

        for platform in platforms:
            if cat.ignore_platform and platform is not cat.target_platform:
                continue

            if cat.rect.colliderect(platform.rect):
                if cat.prev_rect.bottom <= platform.rect.top and cat.velocity_y >= 0:
                    cat.y = platform.rect.top - cat.height
                    cat.velocity_y = 0
                    cat.on_ground = True
                    cat.ignore_platform = False
                    cat.target_platform = None
                    cat.rect.y = cat.y

        # ========= OBSTACLES =========
        obstacle_timer += 1
        if obstacle_timer > 90:
            obstacles.append(Obstacle())
            obstacle_timer = 0

        for obstacle in obstacles[:]:
            obstacle.update(game_speed)
            if obstacle.off_screen():
                obstacles.remove(obstacle)

        for obstacle in obstacles:
            if cat.rect.colliderect(obstacle.rect):
                if cat.prev_rect.bottom <= obstacle.rect.top:
                    cat.y = obstacle.rect.top - cat.height
                    cat.velocity_y = 0
                    cat.on_ground = True
                    cat.rect.y = cat.y
                else:
                    print("GAME OVER")
                    running = False

        # ========= DRAW =========
        screen.fill(WHITE)

        for platform in platforms:
            platform.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        cat.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
