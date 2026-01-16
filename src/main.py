import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS, WHITE
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

    while running:
        clock.tick(FPS)

        # ========= EVENTS =========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    cat.jump()

                if event.key == pygame.K_s:
                    cat.drop_down(platforms)

        cat.update()

        # ========= PLATFORMS =========
        platform_timer += 1
        if platform_timer > 140:
            platforms.append(Platform())
            platform_timer = 0

        for platform in platforms[:]:
            platform.update()
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
            obstacle.update()
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
