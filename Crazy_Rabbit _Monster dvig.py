from os import path

import pygame
from pygame import *
from monster import Monster
from camera import Camera, camera_configure
from block import BlockDie, BlockCarrot, Block, Nora
from player import Player
from config import *


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



def loadLevel(num_level):
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open(f'levels/{num_level}.txt')
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
    loadLevel('1')
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
    waiting_win = False
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
    waiting_win = False

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

        if waiting_win:
            show_winning()
            waiting_win = False
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
            if event.type == WIN_EVENT:
                waiting_win = True
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
            if event.type == KEYUP and event.key == K_SPACE:
                waiting_win = False

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
        #if hero.winner:
            #game_over = True

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