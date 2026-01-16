# ---------- SCREEN ----------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TITLE = "Cat Runner"

# ---------- FPS ----------
FPS = 60

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------- CAT ----------
CAT_SIZE = (50, 50)

# ---------- GROUND ----------
GROUND_Y = SCREEN_HEIGHT - 60

# ---------- OBSTACLES ----------
OBSTACLE_SIZE = (40, 60)
OBSTACLE_SPEED = 5

# ---------- PLATFORMS ----------
PLATFORM_HEIGHT = 20

PLATFORM_MIN_WIDTH = SCREEN_WIDTH // 3
PLATFORM_MAX_WIDTH = SCREEN_WIDTH * 2

# Расстояние между уровнями (больше кота)
LEVEL_GAP = CAT_SIZE[1] + 60

# Уровни (снизу вверх, НИКОГДА ниже пола)
PLATFORM_LEVELS = [
    GROUND_Y - LEVEL_GAP * 1,
    GROUND_Y - LEVEL_GAP * 2,
    GROUND_Y - LEVEL_GAP * 3,
]

# ---------- PHYSICS ----------
GRAVITY = 1
JUMP_FORCE = 18
