import pygame
from pygame import *
import pyganim # для анимации нескольких картинок движения кролика

#Окно параметры
WINDOW_WIDTH = 800 # Ширина создаваемого окна
WINDOW_HEIGHT = 500 # Высота
WINDOW = (WINDOW_WIDTH, WINDOW_HEIGHT) # Параметры окна  ширину и высоту
BACKGROUND_COLOR = "#095795" # цвет окна синий

#Блоки параметры
BLOCK_WIDTH = 32 # размер блока "-" преобразованного в картинку ширина
BLOCK_HEIGHT = 32 # размер блока "-" преобразованного в картинку высота
BLOCK_COLOR = "#3b444b" # цвет квадрата блока зеленый мышьяковый

#Кролик параметры
MOVE_SPEED = 6 #скорость кролика
WIDTH = 45 #размеры отображаемой картинки кролика высота
HEIGHT = 45 #размеры отображаемой картинки кролика высота
COLOR = "#707770" #серо-зеленый
JUMP_POWER = 10 # сила прыжка кролика
GRAVITY = 0.35 # Сила, которая будет тянуть кролика вниз
#Прописываю последовательность картинок анимации для разных положений кролика
ANIMATION_SPEED = 1 # задержка анимации
ANIMATION_RIGHT = [('rabbit/r1-1.png'), #последовательность кадров при движение вправо
            ('rabbit/r7-1.png')]
ANIMATION_LEFT = [('rabbit/l1-1.png'), #последовательность кадров при движение влево
            ('rabbit/l7-1.png')]
ANIMATION_JUMP_LEFT = [('rabbit/j1l-1.png'), #последовательность кадров при движение вверх и в лево
            ('rabbit/j1l-2.png')]
ANIMATION_JUMP_RIGHT = [('rabbit/j1r-1.png'), ('rabbit/j1r-2.png')] #последовательность кадров при движение вверх и вправо
ANIMATION_JUMP = [('rabbit/j2-1.png', 1)] #кадр при прыжке вверх на месте
ANIMATION_STAY = [('rabbit/r4-1.png', 1)] #кадр если кролик стоит на месте


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_movement_speed = 0  # x_movement - скорость горизонтального перемещения. 0 - стоять на месте
        self.startX = x  # Начальная точка кролика Х, возвращение после смерти ####НА ПЕРСПЕКТИВУ###
        self.startY = y # Начальная точка кролика Y, возвращение после смерти
        self.y_movement_speed = 0  # скорость вертикального перемещения
        self.onGround = False  # по умолчанию кролик не знает а есть ли поверхность чтоб оттолкнуться
        self.image = Surface((WIDTH, HEIGHT)) # параметры квадрата кролика
        self.image.fill(Color(COLOR)) #заливаем фон цветом
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным

        # Анимация движения вправо
        rabbit_anim = []
        for anim in ANIMATION_RIGHT:
            rabbit_anim.append((anim, ANIMATION_SPEED)) # кортеж добавляется один “кадр” анимации и количество
            # миллисекунд, в течение которых оно отображается перед отображением следующего кадра
        self.rabbit_animRight = pyganim.PygAnimation(rabbit_anim) #передаем кортедж изображений и время задержки анимации
        self.rabbit_animRight.play() #проигрываем получившеюся последовательность

        # Анимация движения влево
        rabbit_anim = []
        for anim in ANIMATION_LEFT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animLeft = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animLeft.play()

        # Анимация стоящегог кролика
        self.rabbit_animStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.rabbit_animStay.play()
        self.rabbit_animStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        # Анимация кролика прыжка при нажатии лево вверх
        rabbit_anim = []
        for anim in ANIMATION_JUMP_LEFT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animJumpLeft = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animJumpLeft.play()

        # Анимация кролика прыжка при нажатии право вверх
        rabbit_anim = []
        for anim in ANIMATION_JUMP_RIGHT:
            rabbit_anim.append((anim, ANIMATION_SPEED))
        self.rabbit_animJumpRight = pyganim.PygAnimation(rabbit_anim)
        self.rabbit_animJumpRight.play()

        # Анимация кролика прыжок на месте
        self.rabbit_animJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.rabbit_animJump.play()

    def update(self, left, right, up, blocks): #обновляем право, лево, вверх, блоки

        if up: #движение вверх
            if self.onGround:  # если есть поверхность от которой можно оттолкнуться прыгает
                self.y_movement_speed = -JUMP_POWER #скорость вертикального  перемещения =силе прыжка жвижется вверх
            self.image.fill(Color(COLOR)) #заливаем
            self.rabbit_animJump.blit(self.image, (0, 0)) #накладываем картинку прыжка на поверхность на которой
            # отрисовываем и координаты левого верхнего угла

        if left: # движение влево
            self.x_movement_speed = -MOVE_SPEED  # Лево  скорость горизонтального перемещения = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево
                self.rabbit_animJumpLeft.blit(self.image, (0, 0))
            else:
                self.rabbit_animLeft.blit(self.image, (0, 0))

        if right: # движение враво
            self.x_movement_speed = MOVE_SPEED  # Скорость горизонтального перемещения тк вправо  = x + n
            self.image.fill(Color(COLOR))
            if up: # если добавляется прыжок
                self.rabbit_animJumpRight.blit(self.image, (0, 0))
            else:
                self.rabbit_animRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти прааво или лево
            self.x_movement_speed = 0 # скорость горизонтального перемещения 0
            if not up:
                self.image.fill(Color(COLOR))
                self.rabbit_animStay.blit(self.image, (0, 0))

        if not self.onGround: # если поверхности нет
            self.y_movement_speed += GRAVITY # к вертикальной координате перемещения добавляю гравитацию

        self.onGround = False  # не известно когда есть поверхность для отталкивания
        self.rect.y += self.y_movement_speed
        self.collide(0, self.y_movement_speed, blocks)

        self.rect.x += self.x_movement_speed  # переносим свои положение на скорость перемещения по горизонтали
        self.collide(self.x_movement_speed, 0, blocks)

    def collide(self, x_movement_speed, y_movement_speed, blocks): #проверка на пересечение координат героя и платформ,
# если таковое имеется, то  происходит действие.
        for p in blocks:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if x_movement_speed > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # пеерсечение правой стороны игрока и платформы слева - не движится
                    # вправо

                if x_movement_speed < 0:  # если движется влево
                    self.rect.left = p.rect.right  # пеерсечение левой стороны игрока и платформы справа - не движится
                    # влево

                if y_movement_speed > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # пеерсечение нижней стороны игрока и платформы сверху
                    self.onGround = True  # и становится на что-то твердое
                    self.y_movement_speed = 0  # и энергия падения пропадает

                if y_movement_speed < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # пеерсечение верхней стороны игрока и платформы снизу
                    self.y_movement_speed = 0  # и энергия прыжка пропадает


class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image = image.load("blocks/ground1-5.png")
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT) #область для отслеживания пересечений блоков


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect): # начальное конфигурирование камеры
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WINDOW_WIDTH / 2, -t+WINDOW_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WINDOW_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WINDOW_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(WINDOW)  # Создаем окошко
    pygame.display.set_caption("Crazy Rabbit")  # Пишем название в шапку
    background = pygame.image.load('blocks/background_3-1.jpg')

    hero = Player(40, 630)  # начальная создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    all_objects = pygame.sprite.Group()  # Все объекты
    blocks = []  # то, во что мы будем врезаться или опираться

    all_objects.add(hero)

    level = [
        "--------------------------------------------------------------------",
        "-                                                                  -",
        "-                                                                  -",
        "-                                                                  -",
        "-                                                                  -",
        "-      ---                                              --         -",
        "-                                                                  -",
        "-                                --                                -",
        "-                                                                  -",
        "-    -------         ----                   -----                  -",
        "-                                                                  -",
        "-                                                                  -",
        "-                                                                  -",
        "-            ---          -      --                                -",
        "-                                                      --          -",
        "-                  --                                              -",
        "-                             --  -               ---              -",
        "-                                                                  -",
        "-       ---                       -      -                         -",
        "-                                                           --     -",
        "-                                                                  -",
        "--------------------------------------------------------------------"]


    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Block(x, y)
                all_objects.add(pf)
                blocks.append(pf)

            x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
        y += BLOCK_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * BLOCK_WIDTH  # Создаем большой прямоугольник уровня. Это дляя камеры Высчитываем
    # фактическую  ширину уровня
    total_level_height = len(level) * BLOCK_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    running = True
    while running:  # Основной цикл программы
        timer.tick(60)
        for event in pygame.event.get():  # Обрабатываем события кнопок
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

        screen.blit(background, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, blocks)  # передвижение
        # all_objects.draw(screen) # отображение
        for event in all_objects: #меньший прямоугольник  равны размеру окна цетрирующийся относительно главного героя и
            # где прорисовываются все объекты
            screen.blit(event.image, camera.apply(event)) #  Каждую итерацию необходимо всё перерисовывать под положение
            # камеры относительно главного героя

        pygame.display.update()  # обновление и вывод всех изменений на экранн


if __name__ == '__main__':
    main()
