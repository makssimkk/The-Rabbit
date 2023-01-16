from os import path

import pygame
from pygame import *
import pyganim  # для анимации нескольких картинок движения кролика

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


# DIE_EVENT = pygame.USEREVENT + 1

def show_go_screen():
    # поле game over
    background = pygame.image.load('game over/game over3 500-800.jpg.png')
    screen = pygame.display.set_mode(WINDOW)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        #pygame.time.Clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False




class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_movement_speed = 0  # x_movement - скорость горизонтального перемещения. 0 - стоять на месте
        self.startX = x  # Начальная точка кролика Х, возвращение после смерти ####НА ПЕРСПЕКТИВУ###
        self.startY = y  # Начальная точка кролика Y, возвращение после смерти
        self.y_movement_speed = 0  # скорость вертикального перемещения
        self.onGround = False  # по умолчанию кролик не знает а есть ли поверхность чтоб оттолкнуться
        self.image = Surface((WIDTH, HEIGHT))  # параметры квадрата кролика
        self.image.fill(Color(COLOR))  # заливаем фон цветом
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        self.lives = 3

        # Анимация движения вправо
        rabbit_anim = []
        for anim in ANIMATION_RIGHT:
            rabbit_anim.append((anim, ANIMATION_SPEED))  # кортеж добавляется один “кадр” анимации и количество
            # миллисекунд, в течение которых оно отображается перед отображением следующего кадра
        self.rabbit_animRight = pyganim.PygAnimation(
            rabbit_anim)  # передаем кортедж изображений и время задержки анимации
        self.rabbit_animRight.play()  # проигрываем получившеюся последовательность

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

        # счетчик
        self.n_carrot = 0

        self.winner = False  # пока не дошел до пня

    def update(self, left, right, up, blocks):  # обновляем право, лево, вверх, блоки

        if up:  # движение вверх
            if self.onGround:  # если есть поверхность от которой можно оттолкнуться прыгает
                self.y_movement_speed = -JUMP_POWER  # скорость вертикального  перемещения =силе прыжка жвижется вверх
            self.image.fill(Color(COLOR))  # заливаем
            self.rabbit_animJump.blit(self.image, (0, 0))  # накладываем картинку прыжка на поверхность на которой
            # отрисовываем и координаты левого верхнего угла

        if left:  # движение влево
            self.x_movement_speed = -MOVE_SPEED  # Лево  скорость горизонтального перемещения = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево
                self.rabbit_animJumpLeft.blit(self.image, (0, 0))
            else:
                self.rabbit_animLeft.blit(self.image, (0, 0))

        if right:  # движение враво
            self.x_movement_speed = MOVE_SPEED  # Скорость горизонтального перемещения тк вправо  = x + n
            self.image.fill(Color(COLOR))
            if up:  # если добавляется прыжок
                self.rabbit_animJumpRight.blit(self.image, (0, 0))
            else:
                self.rabbit_animRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти прааво или лево
            self.x_movement_speed = 0  # скорость горизонтального перемещения 0
            if not up:
                self.image.fill(Color(COLOR))
                self.rabbit_animStay.blit(self.image, (0, 0))

        if not self.onGround:  # если поверхности нет
            self.y_movement_speed += GRAVITY  # к вертикальной координате перемещения добавляю гравитацию

        self.onGround = False  # не известно когда есть поверхность для отталкивания
        self.rect.y += self.y_movement_speed
        self.collide(0, self.y_movement_speed, blocks)

        self.rect.x += self.x_movement_speed  # переносим свои положение на скорость перемещения по горизонтали
        self.collide(self.x_movement_speed, 0, blocks)

    def collide(self, x_movement_speed, y_movement_speed,
                blocks):  # проверка на пересечение координат героя и платформ,
        # если таковое имеется, то  происходит действие.
        for p in blocks:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, BlockDie) or isinstance(p, Monster):  # если пересакаемый блок - blocks.BlockDie или Monster
                    # isinstance() в Python используется для проверки, является ли объект экземпляром указанного класса или нет.
                    self.die()  # смерть
                    self.lives -= 1


                elif isinstance(p, Nora):  # если коснулись норы
                    self.winner = True
                    # победили!!!
                    show_winning()
                    self.delete() # убираю героя иначе при перезапуски будет наложение картинки


                elif isinstance(p, BlockCarrot):  # если пересакаемый блок - шипы
                    self.n_carrot += 1
                    blocks.remove(p)
                    p.delete()


                else:
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

    def die(self):
        time.wait(500)  # сейчас стоит задержка по времени, может музыку прописать на смерть?!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def delete(self):
        self.kill()


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))  # прозрачный слой
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.x_movement_speed = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.y_movement_speed = up  # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, blocks):  # по принципу героя

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.y_movement_speed
        self.rect.x += self.x_movement_speed

        self.collide(blocks)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.x_movement_speed = -self.x_movement_speed  # если прошли максимальное растояние, то идеи в обратную сторону горизонталь
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.y_movement_speed = -self.y_movement_speed  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, blocks):
        for p in blocks:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.x_movement_speed = - self.x_movement_speed  # то поворачиваем в обратную сторону
                self.y_movement_speed = - self.y_movement_speed


class Block(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image = image.load("blocks/ground1-5.png")
        self.image.set_colorkey(Color(BLOCK_COLOR))  # делаем фон прозрачным
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)  # область для отслеживания пересечений блоков


class BlockDie(Block):  # кристал-смерти
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/Red Crystal Cluster-1.png')


class BlockCarrot(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load('blocks/carrot.png')

    def delete(self):
        self.kill()


class Nora(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)
        self.image = image.load("Finish/TREE_HOUSE5-1.png")


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # начальное конфигурирование камеры
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WINDOW_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WINDOW_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open('levels/1.txt')
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды

                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])

                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    all_objects.add(mn)
                    blocks.append(mn)
                    monsters.add(mn)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def main():
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(WINDOW)  # Создаем окошко
    pygame.display.set_caption("Crazy Rabbit")  # Пишем название в шапку
    background = pygame.image.load('blocks/background_3-1.jpg')
    pygame.mixer.music.load('Music/Jungle trail bpm90 C Example Background.wav')  # мелодия игры
    pygame.mixer.music.set_volume(0.4)  # громкость мелодии
    pygame.mixer.music.play(loops=-1)  # зациклила мелодию

    # hero = Player(40, 550)  # начальная создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False
    hero = Player(playerX, playerY)  # создаем героя по (x,y) координатам
    all_objects.add(hero)

    # создаем уменьшенное изображение для отображения жизней
    player_img = pygame.image.load(path.join('img/r4-1.png')).convert()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(Color(0, 0, 0))  # Black

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Block(x, y)
                all_objects.add(pf)
                blocks.append(pf)
            if col == 'd':
                bd = BlockDie(x, y)
                all_objects.add(bd)
                blocks.append(bd)
            if col == 'N':
                bn = Nora(x, y)
                all_objects.add(bn)
                blocks.append(bn)
            if col == "c":
                bc = BlockCarrot(x, y)
                all_objects.add(bc)
                blocks.append(bc)

            x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
        y += BLOCK_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с

    total_level_width = len(level[0]) * BLOCK_WIDTH  # Создаем большой прямоугольник уровня. Это дляя камеры Высчитываем
    # фактическую  ширину уровня
    total_level_height = len(level) * BLOCK_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    timer = pygame.time.Clock()

    game_over = False
    running = True
    while running:  # Основной цикл программы
        if game_over: #если игра закончилась
            show_go_screen() #подключаем функцию ожидания для этого состояния или крестик и выход или перезапуск
            game_over = False
            pygame.event.clear()
            up = False
            left = right = False
            hero = Player(playerX, playerY)  # создаем героя по (x,y) координатам
            hero.update(left, right, up, blocks)  # передвижение
            all_objects.add(hero) # добавляем героя
            monsters.update(blocks) #обновляем переносим блоки
            camera.update(hero)  # центризируем камеру относительно персонажа
            pygame.display.update()

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
        monsters.update(blocks)  # передвигаем всех монстров
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, blocks)  # передвижение
        for e in all_objects:
            screen.blit(e.image, camera.apply(e))

        draw_lives(screen, WINDOW_WIDTH - 100, 5, hero.lives, player_mini_img)  # прорисовка колличства жизни кроликами

        draw_text(screen, str(hero.n_carrot), 36, 10, 10) # прорисовка колиичества морковок на экране
        img = pygame.image.load("blocks/carrot.png") # значек морковка
        carrot(screen, img, 36, 0) # расположение значка морковки на экране игры

        # Если игрок умер, игра окончена
        if hero.lives == 0:
            game_over = True
            hero.delete()

        # Если игрок дошел до норы игра окончена
        if hero.winner:
            game_over = True

        pygame.display.update()  # обновление и вывод всех изменений на экран


def draw_text(surf, text, size, x, y):
    # работа со счетчиком морковок цифры
    f1 = pygame.font.Font(None, size)
    text1 = f1.render(text, True, (255, 255, 255))
    text_rect = text1.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text1, text_rect)


def carrot(surf, img, x1, y1):
    # картинка морковки рядом с счетчиком
    img_rect = img.get_rect()
    img_rect.midtop = (x1, y1)
    surf.blit(img, img_rect)

def show_winning():
    # win/continue
    bg = pygame.image.load('you win/заставка800-500.png')
    screen = pygame.display.set_mode(WINDOW)
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

level = []
all_objects = pygame.sprite.Group()  # Все объекты
monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
blocks = []  # то, во что мы будем врезаться или опираться

if __name__ == "__main__":
    main()