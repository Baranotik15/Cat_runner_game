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
    GROUND_Y,
)

from entities.cat import Cat
from entities.obstacle import Obstacle
from entities.platform import Platform


# ===== TUNING =====
DROP_HOLD_DELAY = 200

GROUND_OBSTACLE_CHANCE = 0.9
GROUND_OBSTACLE_TIMER = 60

PLATFORM_OBSTACLE_CHANCE = 0.6
OBSTACLE_PADDING = 40

MAX_JUMP_DISTANCE = 260


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    running = True

    cat = Cat()

    platforms = []
    obstacles = []

    game_speed = BASE_SPEED
    speed_timer = 0

    platform_timer = 0
    ground_obstacle_timer = 0

    last_platform_level = 0
    last_platform_x = {i: -9999 for i in range(len(PLATFORM_LEVELS))}

    s_pressed_time = None

    while running:
        clock.tick(FPS)

        # ===== SPEED UPDATE =====
        speed_timer += 1
        if speed_timer >= FPS * SPEED_INTERVAL:
            game_speed += SPEED_INCREASE
            speed_timer = 0

        # ===== EVENTS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    cat.jump()

                if event.key == pygame.K_s:
                    s_pressed_time = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s and s_pressed_time is not None:
                    held = pygame.time.get_ticks() - s_pressed_time
                    if held < DROP_HOLD_DELAY:
                        cat.drop_once(platforms)
                    cat.drop_hold_end()
                    s_pressed_time = None

        if s_pressed_time is not None and not cat.drop_hold:
            if pygame.time.get_ticks() - s_pressed_time >= DROP_HOLD_DELAY:
                cat.drop_hold_start()

        # ===== UPDATE CAT =====
        cat.update()

        # ===== GROUND OBSTACLES =====
        ground_obstacle_timer += 1
        if ground_obstacle_timer >= GROUND_OBSTACLE_TIMER:
            ground_obstacle_timer = 0
            if random.random() < GROUND_OBSTACLE_CHANCE:
                obstacles.append(
                    Obstacle(SCREEN_WIDTH, GROUND_Y)
                )

        # ===== PLATFORM SPAWN (SAFE) =====
        platform_timer += 1
        if platform_timer >= 140:
            possible_levels = []
            weights = []

            for i, y in enumerate(PLATFORM_LEVELS):
                if abs(i - last_platform_level) <= 1:
                    if i == 0:
                        can_jump = True
                    else:
                        can_jump = (
                            SCREEN_WIDTH - last_platform_x[i - 1]
                            <= MAX_JUMP_DISTANCE
                        )

                    if can_jump:
                        possible_levels.append(i)
                        weights.append(4 if i == 0 else 2)

            if not possible_levels:
                possible_levels = [0]
                weights = [1]

            start_level = random.choices(possible_levels, weights)[0]

            max_chain = min(3, len(PLATFORM_LEVELS) - start_level)
            chain_len = random.randint(1, max_chain)

            for offset in range(chain_len):
                idx = start_level + offset
                platform = Platform(PLATFORM_LEVELS[idx])
                platforms.append(platform)
                last_platform_x[idx] = platform.x

                if random.random() < PLATFORM_OBSTACLE_CHANCE:
                    if platform.width > OBSTACLE_PADDING * 2 + 40:
                        ox = random.randint(
                            platform.x + OBSTACLE_PADDING,
                            platform.x + platform.width - OBSTACLE_PADDING - 40
                        )
                        obstacles.append(
                            Obstacle(ox, platform.y)
                        )

            last_platform_level = start_level
            platform_timer = 0

        # ===== UPDATE PLATFORMS =====
        for platform in platforms[:]:
            platform.update(game_speed)
            if platform.off_screen():
                platforms.remove(platform)

        # ===== PLATFORM COLLISIONS =====
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

        # ===== UPDATE OBSTACLES =====
        for obstacle in obstacles[:]:
            obstacle.update(game_speed)
            if obstacle.off_screen():
                obstacles.remove(obstacle)

        # ===== OBSTACLE COLLISIONS =====
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

        # ===== DRAW =====
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
