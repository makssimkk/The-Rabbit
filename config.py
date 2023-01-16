import pygame

# количество уровней
MAX_LEVEL = 3

# Окно параметры
WINDOW_WIDTH = 800  # Ширина создаваемого окна
WINDOW_HEIGHT = 500  # Высота
WINDOW = (WINDOW_WIDTH, WINDOW_HEIGHT)  # Параметры окна  ширину и высоту
BACKGROUND_COLOR = "#095795"  # цвет окна синий

# Блоки параметры
BLOCK_WIDTH = 32  # размер блока "-" преобразованного в картинку ширина
BLOCK_HEIGHT = 32  # размер блока "-" преобразованного в картинку высота
BLOCK_COLOR = "#3b444b"  # цвет квадрата блока зеленый мышьяковый

# Змеи-монстры параметры
MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
ANIMATION_MONSTERHORYSONTAL = [('Snake/snake_1.png'),
                               ('Snake/snake_2.png')]

# Нора
ANIMATION_NORA = [('Finish/TREE_HOUSES-1.pgn', 1)]

# Кролик параметры
MOVE_SPEED = 6  # скорость кролика
WIDTH = 45  # размеры отображаемой картинки кролика высота
HEIGHT = 45  # размеры отображаемой картинки кролика высота
COLOR = "#707770"  # серо-зеленый
JUMP_POWER = 10  # сила прыжка кролика
GRAVITY = 0.35  # Сила, которая будет тянуть кролика вниз
# Прописываю последовательность картинок анимации для разных положений кролика
ANIMATION_SPEED = 1  # задержка анимации
ANIMATION_RIGHT = [('rabbit/r1-1.png'),  # последовательность кадров при движение вправо
                   ('rabbit/r7-1.png')]
ANIMATION_LEFT = [('rabbit/l1-1.png'),  # последовательность кадров при движение влево
                  ('rabbit/l7-1.png')]
ANIMATION_JUMP_LEFT = [('rabbit/j1l-1.png'),  # последовательность кадров при движение вверх и в лево
                       ('rabbit/j1l-2.png')]
ANIMATION_JUMP_RIGHT = [('rabbit/j1r-1.png'),
                        ('rabbit/j1r-2.png')]  # последовательность кадров при движение вверх и вправо
ANIMATION_JUMP = [('rabbit/j2-1.png', 1)]  # кадр при прыжке вверх на месте
ANIMATION_STAY = [('rabbit/r4-1.png', 1)]  # кадр если кролик стоит на месте

DIE_EVENT = pygame.USEREVENT + 1
WIN_EVENT = pygame.USEREVENT + 2
GAME_OVER_EVENT = pygame.USEREVENT + 3

UPDATE_LOADING = pygame.USEREVENT + 0