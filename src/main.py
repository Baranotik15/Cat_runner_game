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


DROP_HOLD_DELAY = 200  # ms


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

    last_platform_level_index = 0
    s_pressed_time = None

    last_platform_x = {0: 0, 1: -9999, 2: -9999}
    max_jump_distance = 260

    while running:
        clock.tick(FPS)

        speed_timer += 1
        if speed_timer >= FPS * SPEED_INTERVAL:
            game_speed += SPEED_INCREASE
            speed_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    cat.jump()

                if event.key == pygame.K_s:
                    s_pressed_time = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    if s_pressed_time is not None:
                        held_time = pygame.time.get_ticks() - s_pressed_time

                        if held_time < DROP_HOLD_DELAY:
                            cat.drop_once(platforms)

                        cat.drop_hold_end()
                        s_pressed_time = None

        if s_pressed_time is not None and not cat.drop_hold:
            held_time = pygame.time.get_ticks() - s_pressed_time
            if held_time >= DROP_HOLD_DELAY:
                cat.drop_hold_start()

        cat.update()

        platform_timer += 1
        if platform_timer > 140:
            possible_starts = [0]
            weights = [8]

            for i in range(1, len(PLATFORM_LEVELS)):
                if abs(i - last_platform_level_index) <= 1:
                    lower_level = i - 1
                    if SCREEN_WIDTH - last_platform_x[lower_level] < max_jump_distance:
                        possible_starts.append(i)
                        weights.append(2 if i == 1 else 1)

            start_level = random.choices(possible_starts, weights=weights)[0]

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
                platform = Platform(PLATFORM_LEVELS[level_index])
                platforms.append(platform)
                last_platform_x[level_index] = platform.x

            last_platform_level_index = start_level
            platform_timer = 0

        for platform in platforms[:]:
            platform.update(game_speed)
            if platform.off_screen():
                platforms.remove(platform)

        for platform in platforms:
            if cat.ignore_platform:
                if cat.drop_hold:
                    continue
                if platform is not cat.target_platform:
                    continue

            if cat.rect.colliderect(platform.rect):
                if cat.prev_rect.bottom <= platform.rect.top and cat.velocity_y >= 0:
                    cat.y = platform.rect.top - cat.height
                    cat.velocity_y = 0
                    cat.on_ground = True
                    cat.ignore_platform = False
                    cat.target_platform = None
                    cat.rect.y = cat.y

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
