''' Constant Values used across the program.

Purpose: 
- Screen settings 
- Physics tuning 
- Gameplay balance values 
- UI layout constants 
- Character defintiions '''

# Screen settings 
WIDTH = 900
HEIGHT = 550
FPS = 60

# colors (black and white theme)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (140, 140, 140)
DARK_GRAY = (80, 80, 80)
OFF_WHITE = (235, 235, 235)

# physics 
GRAVITY = 0.18          # how fast things fall
VELOCITY_SCALE = 0.65   # converts power into speed
WIND_FACTOR = 0.012     # how much wind pushes the projectile
MAX_POWER = 18          # maximum charge power

# world layout 
GROUND_Y = HEIGHT - 80              # where the ground is

FENCE_X = WIDTH // 2                # fence in the middle
FENCE_HEIGHT = 120                  # how tall the fence is

# player spawn positions
PLAYER1_X = 160
PLAYER1_Y = GROUND_Y - 28

PLAYER2_X = WIDTH - 160
PLAYER2_Y = GROUND_Y - 32

# combat system 
HIT_RADIUS = 30         # how close a throw needs to be to count as a hit
DAMAGE_MIN = 25         # minimum damage per hit
DAMAGE_MAX = 40         # maximum damage per hit
MAX_HP = 100            # starting health
CRIT_CHANCE = 0.2       # 20%
CRIT_MULTIPLIER = 2

# log system layout 
LEFT_X = 20
RIGHT_X = WIDTH - 220

TOP_Y = 10

LOG_W = 220
LOG_H = 220
LOG_X = WIDTH - LOG_W - 20
LOG_Y = 120

BOTTOM_Y = HEIGHT - 120

LOG_LINE_H = 16



# XP system (used for healing only)
XP_HEAL_COST = 100     # XP needed to unlock one heal


# character stats 
CHARACTERS = {
    "Cat": {
        "hp": 100,
        "atk": 12,
        "def": 8,
        "special_bonus": 1.0,
    },
    "Dog": {
        "hp": 110,
        "atk": 10,
        "def": 10,
        "special_bonus": 1.1,
    },
    "Wolf": {
        "hp": 90,
        "atk": 18,
        "def": 6,
        "special_bonus": 1.3,
    },
    "Elephant": {
        "hp": 140,
        "atk": 8,
        "def": 14,
        "special_bonus": 0.9,
    }
}


# UI
UI_GROUND_OFFSET = 45  # distance below ground line
UI_BAR_Y = min(GROUND_Y + UI_GROUND_OFFSET, HEIGHT - 40)

UI_BUTTON_W = 90
UI_BUTTON_H = 26
UI_BUTTON_GAP = 10

UI_CENTER_X = WIDTH // 2

UI_HEAL_X = UI_CENTER_X - (UI_BUTTON_W * 1.5 + UI_BUTTON_GAP)
UI_SPECIAL_X = UI_CENTER_X - (UI_BUTTON_W / 2)
UI_SHIELD_X = UI_CENTER_X + (UI_BUTTON_W / 2 + UI_BUTTON_GAP)


# player UI anchor 
P1_UI_X = UI_HEAL_X
P2_UI_X = UI_SHIELD_X + UI_BUTTON_W  # right-side anchor

TURN_TEXT_Y_OFFSET = 35
DAMAGE_TEXT_Y_OFFSET = 15