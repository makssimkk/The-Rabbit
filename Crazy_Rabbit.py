import pygame
from pygame import *
from level_config import LEVEL
from config import *
from player import Player
from camera import Camera, camera_configure
from block import Block


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

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in LEVEL:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Block(x, y)
                all_objects.add(pf)
                blocks.append(pf)

            x += BLOCK_WIDTH  # блоки платформы ставятся на ширине блоков
        y += BLOCK_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(LEVEL[0]) * BLOCK_WIDTH  # Создаем большой прямоугольник уровня. Это дляя камеры Высчитываем
    # фактическую  ширину уровня
    total_level_height = len(LEVEL) * BLOCK_HEIGHT  # высоту

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
