NS_TO_MS: int = 1000000
ROBOT_COLOR = "green"
DEAD_ROBOT_COLOR = "red"
ROBOT_SPEED_COLOR = "yellow"
# board size 
BOUNDS_WIDTH: int = 1000
MAX_X: float = BOUNDS_WIDTH /2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 600
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20


TURTLE_SPEED_INDICATOR_CONSTANT = 10
TURTLE_ACCELERATION_INDICATOR_CONSTANT = 10

GENOME_SIZE = 200
ROBOTS_COUNT = 250
ROBOT_RADIUS = 15
TARGET_RADIUS = 30

DIRECTION_CHANGE_TICKS = 5
ACCELERATION_CONSTANT = 0.2
SPEED_CONSTANT = 1
INITIAL_SPEED = 0

MUTATION_PROBABILITY = 0.002
LOW_MUTATION_PROBABILITY = 0.0005

GENERATIONS_MAX = 300000

GENERATION_PRINT_RATE = 50
TICKS_PER_SCREEN_UPDATE = 2

NO_MUTATION_ON_PRINTED_GENERATION = True
PRINT_BEST_ONLY = False
KEEP_BEST = False
DONT_MUTATE_FRACTION = 0.5

PRINT_FIRST_N_GENERATIONS = 0







